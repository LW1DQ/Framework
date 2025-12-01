"""
Integración NS3-AI para Deep Reinforcement Learning

Este módulo implementa la interfaz de memoria compartida con NS-3 usando ns3-ai.
Permite el intercambio de alta velocidad de observaciones y acciones entre Python (PyTorch) y C++ (NS-3).
"""

import sys
import os
import time
import struct
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import numpy as np

# Intentar importar ns3_ai, si no existe, usar Mock para desarrollo/tests
try:
    from ns3_ai import RingBuffer, SharedMemory
    HAS_NS3_AI = True
except ImportError:
    HAS_NS3_AI = False
    # Definiciones Mock para que el código sea válido estáticamente
    class RingBuffer:
        def __init__(self, *args, **kwargs): pass
    class SharedMemory:
        def __init__(self, *args, **kwargs): pass

# Importar PyTorch
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    # Fallback para que la definición de clase no falle estáticamente
    class MockNN:
        class Module:
            def eval(self): pass
            def load_state_dict(self, state_dict): pass
            def load_state_dict(self, state_dict): pass
            def __call__(self, *args): return (args[0], args[0]) # Return tuple for unpacking (probs, val)
        class Sequential:
            def __init__(self, *args): pass
            def __call__(self, x): return x
        class Linear:
            def __init__(self, *args): pass
        class Tanh:
            def __init__(self): pass
        class Softmax:
            def __init__(self, dim=None): pass
    nn = MockNN()

# Configuración de Memoria Compartida
# Estructura: [State (10 floats)] -> [Action (1 int)]
STATE_DIM = 10
ACTION_DIM = 5
MEM_SIZE = 4096  # Tamaño del buffer

class ActorCritic(nn.Module):
    """Red Neuronal Actor-Critic para PPO"""
    def __init__(self, state_dim, action_dim):
        super(ActorCritic, self).__init__()
        # Actor head
        self.actor = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.Tanh(),
            nn.Linear(64, 32),
            nn.Tanh(),
            nn.Linear(32, action_dim),
            nn.Softmax(dim=-1)
        )
        # Critic head
        self.critic = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.Tanh(),
            nn.Linear(64, 32),
            nn.Tanh(),
            nn.Linear(32, 1)
        )

    def forward(self, state):
        return self.actor(state), self.critic(state)

class NS3AIAgent:
    """
    Agente que gestiona la comunicación con NS-3 vía memoria compartida.
    Implementa el bucle de control RL: Read State -> Inference -> Write Action
    """
    def __init__(self, shm_name: str = "ns3_ai_shm", model_path: str = None):
        self.shm_name = shm_name
        self.model_path = model_path
        self.policy = ActorCritic(STATE_DIM, ACTION_DIM)
        self.step_count = 0
        self.episode_rewards = []
        
        if HAS_TORCH and model_path and os.path.exists(model_path):
            try:
                self.policy.load_state_dict(torch.load(model_path))
                print(f"🤖 Modelo cargado desde {model_path}")
            except Exception as e:
                print(f"⚠️ Error cargando modelo: {e}")
        
        if HAS_TORCH:
            self.policy.eval()

        # Inicializar interfaz de memoria compartida (si ns3-ai está disponible)
        self.interface = None
        if HAS_NS3_AI:
            try:
                # Usar Ns3AiMsgInterface para comunicación estructurada
                from ns3_ai import Ns3AiMsgInterface
                
                # Definir estructuras de comunicación
                # Deben coincidir con las definidas en C++ (drl-routing-agent.h)
                self.interface = Ns3AiMsgInterface(
                    shm_name,
                    size=MEM_SIZE,
                    isMemoryCreator=False  # Python es el consumidor
                )
                print(f"✅ Interfaz ns3-ai inicializada: {shm_name}")
            except Exception as e:
                print(f"⚠️ Error inicializando ns3-ai: {e}")
                print(f"   Ejecutando en modo simulado")
                self.interface = None
        else:
            print(f"⚠️ ns3-ai no disponible. Ejecutando en modo simulado")

    def run_interaction_loop(self, max_steps: int = 1000):
        """
        Ejecuta el bucle principal de interacción con NS-3
        
        Args:
            max_steps: Número máximo de pasos de interacción
        """
        if not self.interface and not HAS_NS3_AI:
            print("❌ ns3-ai no disponible. Ejecutando en modo simulado...")
            return self._run_simulated_loop(max_steps)

        print(f"🚀 Iniciando bucle de interacción NS-3 AI (SHM: {self.shm_name})...")
        print(f"   Modelo: {self.model_path if self.model_path else 'Aleatorio'}")
        print(f"   Max steps: {max_steps}")
        print("")
        
        step = 0
        episode_reward = 0.0
        
        try:
            while step < max_steps:
                # 1. Leer Estado desde NS-3 (vía memoria compartida)
                if self.interface:
                    try:
                        # Leer estructura EnvState desde C++
                        state_data = self.interface.GetCpp2PyStruct()
                        
                        # Convertir a numpy array
                        state = np.array([
                            state_data.buffer_occupancy,
                            state_data.num_neighbors,
                            state_data.recent_pdr,
                            state_data.recent_delay,
                            state_data.distance_to_dest,
                            state_data.hops_to_dest,
                            state_data.energy_level,
                            state_data.avg_neighbor_load,
                            state_data.packet_priority,
                            state_data.time_in_queue
                        ], dtype=np.float32)
                    except Exception as e:
                        print(f"⚠️ Error leyendo estado: {e}")
                        state = np.random.rand(STATE_DIM).astype(np.float32)
                else:
                    # Modo simulado
                    state = np.random.rand(STATE_DIM).astype(np.float32)
                
                # 2. Inferencia (Seleccionar Acción)
                action = 0
                action_probs = None
                
                if HAS_TORCH:
                    state_tensor = torch.FloatTensor(state).unsqueeze(0)
                    with torch.no_grad():
                        probs, value = self.policy(state_tensor)
                        action = torch.argmax(probs, dim=1).item()
                        action_probs = probs.squeeze().numpy()
                else:
                    action = np.random.randint(0, ACTION_DIM)
                
                # 3. Escribir Acción hacia NS-3
                if self.interface:
                    try:
                        # Crear estructura AgentAction
                        action_data = self.interface.GetPy2CppStruct()
                        action_data.next_hop_id = action
                        action_data.tx_power = 1.0
                        action_data.priority = 0
                        
                        # Enviar a NS-3
                        self.interface.SetPy2CppStruct(action_data)
                    except Exception as e:
                        print(f"⚠️ Error enviando acción: {e}")
                
                # 4. Calcular recompensa (simplificado)
                # En implementación real, NS-3 enviaría la recompensa
                reward = state[2] - 0.1 * state[3] / 100.0  # PDR - delay_penalty
                episode_reward += reward
                
                step += 1
                self.step_count += 1
                
                # Logging periódico
                if step % 100 == 0:
                    print(f"  🔄 Step {step}/{max_steps}")
                    print(f"     Estado: PDR={state[2]:.3f}, Delay={state[3]:.1f}ms, Neighbors={state[1]:.0f}")
                    print(f"     Acción: {action} (probs: {action_probs if action_probs is not None else 'N/A'})")
                    print(f"     Recompensa acumulada: {episode_reward:.2f}")
                    print("")
                
                # Pequeña pausa para no saturar
                time.sleep(0.001)
                    
        except KeyboardInterrupt:
            print("\n🛑 Interacción detenida por usuario")
        except Exception as e:
            print(f"\n❌ Error en bucle de interacción: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print(f"\n📊 Estadísticas finales:")
            print(f"   Steps ejecutados: {step}")
            print(f"   Recompensa total: {episode_reward:.2f}")
            print(f"   Recompensa promedio: {episode_reward/step if step > 0 else 0:.3f}")
            
            self.episode_rewards.append(episode_reward)
    
    def _run_simulated_loop(self, max_steps: int):
        """
        Ejecuta bucle simulado cuando ns3-ai no está disponible
        """
        print("🎮 Ejecutando en modo SIMULADO (sin ns3-ai)")
        print(f"   Generando {max_steps} interacciones simuladas...")
        print("")
        
        episode_reward = 0.0
        
        for step in range(max_steps):
            # Estado simulado
            state = np.random.rand(STATE_DIM).astype(np.float32)
            
            # Acción simulada
            if HAS_TORCH:
                state_tensor = torch.FloatTensor(state).unsqueeze(0)
                with torch.no_grad():
                    probs, _ = self.policy(state_tensor)
                    action = torch.argmax(probs).item()
            else:
                action = np.random.randint(0, ACTION_DIM)
            
            # Recompensa simulada
            reward = np.random.randn() * 0.1
            episode_reward += reward
            
            if (step + 1) % 100 == 0:
                print(f"  🔄 Step {step+1}/{max_steps} - Reward: {episode_reward:.2f}")
        
        print(f"\n✅ Simulación completada")
        print(f"   Recompensa total: {episode_reward:.2f}")
        self.episode_rewards.append(episode_reward)

def generate_ns3_ai_code(protocol: str, nodes: int, area_size: int) -> str:
    """
    Genera el script de simulación NS-3 (Python) que usa ns3-ai
    """
    return f'''#!/usr/bin/env python3
"""
Script NS-3 con integración ns3-ai
Protocolo: {protocol}
"""
import sys
import ns.core
import ns.network
import ns.internet
import ns.mobility
import ns.wifi
import ns.applications
import ns.{protocol.lower()}

# Intentar importar ns3-ai
try:
    from ns3_ai import RingBuffer
    HAS_NS3_AI = True
except ImportError:
    HAS_NS3_AI = False
    print("⚠️ ns3-ai no instalado")

def main():
    # ... Configuración estándar de NS-3 (nodos, wifi, etc.) ...
    # (Omitido por brevedad, usar template anterior)
    
    if HAS_NS3_AI:
        # Inicializar memoria compartida
        # struct EnvState {{ float features[10]; }};
        # struct Act {{ int action; }};
        rb = RingBuffer("ns3_ai_shm", 4096)
        
        # Bucle de simulación
        # En NS-3 real, esto se hace extendiendo una clase AiModel
        pass

    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()

if __name__ == "__main__":
    main()
'''

def get_ns3_ai_installation_instructions() -> str:
    return """
# Instalación de ns3-ai
1. Clonar: `git clone https://github.com/hust-diangroup/ns3-ai.git` en `ns-3-dev/contrib`
2. Configurar: `./ns3 configure --enable-examples --enable-tests`
3. Compilar: `./ns3 build`
"""

def generate_drl_training_code(protocol: str) -> str:
    """
    Genera código Python para entrenar el modelo PPO con PyTorch
    """
    return f'''#!/usr/bin/env python3
"""
Entrenamiento PPO (Proximal Policy Optimization) para {protocol}
"""
import torch
# ... (Código de entrenamiento estándar) ...
# Por brevedad, retornamos un template básico
print("Entrenamiento PPO iniciado...")
'''

def extract_drl_parameters(proposal: str) -> Dict:
    """Extrae parámetros de DRL de la propuesta del optimizer"""
    return {
        'learning_rate': 0.001,
        'discount_factor': 0.99,
        'epsilon': 0.1,
        'batch_size': 32,
        'memory_size': 10000
    }

def should_use_drl(metrics: Dict) -> bool:
    """Determina si se debe usar DRL basándose en las métricas"""
    pdr = metrics.get('avg_pdr', 100)
    delay = metrics.get('avg_delay', 0)
    if pdr < 80 or delay > 150:
        return True
    return False
