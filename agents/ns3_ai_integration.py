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
import ctypes

# Configuration constants
SHM_NAME = "ns3_ai_shm"
SHM_SIZE = 4096
STATE_DIM = 10
ACTION_DIM = 5

# --- NS-3 AI IMPOSRT ---
try:
    from ns3_ai import RingBuffer, SharedMemory, Ns3AiMsgInterface
    HAS_NS3_AI = True
except ImportError:
    HAS_NS3_AI = False

# --- PYTORCH IMPORT ---
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

# --- DATA STRUCTURES (Must match C++ side) ---
class EnvState(ctypes.Structure):
    _fields_ = [
        ("buffer_occupancy", ctypes.c_float),
        ("num_neighbors", ctypes.c_float),
        ("recent_pdr", ctypes.c_float),
        ("recent_delay", ctypes.c_float),
        ("distance_to_dest", ctypes.c_float),
        ("hops_to_dest", ctypes.c_float),
        ("energy_level", ctypes.c_float),
        ("avg_neighbor_load", ctypes.c_float),
        ("packet_priority", ctypes.c_float),
        ("time_in_queue", ctypes.c_float)
    ]

class AgentAction(ctypes.Structure):
    _fields_ = [
        ("next_hop_id", ctypes.c_int),
        ("tx_power", ctypes.c_float),
        ("priority", ctypes.c_int)
    ]

# --- NEURAL NETWORK ---
if HAS_TORCH:
    class ActorCritic(nn.Module):
        """Standard Actor-Critic Network for PPO"""
        def __init__(self, state_dim, action_dim):
            super(ActorCritic, self).__init__()
            # Shared features
            self.features = nn.Sequential(
                nn.Linear(state_dim, 64),
                nn.Tanh(),
                nn.Linear(64, 64),
                nn.Tanh()
            )
            # Actor head
            self.actor = nn.Sequential(
                nn.Linear(64, 32),
                nn.Tanh(),
                nn.Linear(32, action_dim),
                nn.Softmax(dim=-1)
            )
            # Critic head
            self.critic = nn.Sequential(
                nn.Linear(64, 32),
                nn.Tanh(),
                nn.Linear(32, 1)
            )

        def forward(self, state):
            x = self.features(state)
            return self.actor(x), self.critic(x)
else:
    # Dummy class for static analysis
    class ActorCritic:
        def __init__(self, *args): pass


class NS3AIAgent:
    """
    Agente que gestiona la comunicación con NS-3 vía memoria compartida.
    Implementa el bucle de control RL: Read State -> Inference -> Write Action
    """
    def __init__(self, shm_name: str = SHM_NAME, model_path: str = None):
        self.shm_name = shm_name
        self.model_path = model_path
        self.policy = None
        self.step_count = 0
        self.episode_rewards = []
        
        # Initialize Model
        if HAS_TORCH:
            self.policy = ActorCritic(STATE_DIM, ACTION_DIM)
            if model_path and os.path.exists(model_path):
                try:
                    self.policy.load_state_dict(torch.load(model_path))
                    print(f"🤖 Modelo cargado desde {model_path}")
                except Exception as e:
                    print(f"⚠️ Error cargando modelo: {e}. Iniciando con pesos aleatorios.")
            self.policy.eval() # Inference mode by default
        
        # Initialize Shared Memory Interface
        self.interface = None
        if HAS_NS3_AI:
            try:
                # Use Ns3AiMsgInterface for structured communication
                # It handles the ring buffer synchronization logic
                self.interface = Ns3AiMsgInterface(
                    shm_name,
                    size=SHM_SIZE,
                    isMemoryCreator=False # NS-3 (C++) creates the memory
                )
                print(f"✅ Interfaz ns3-ai inicializada: {shm_name}")
            except Exception as e:
                print(f"⚠️ Error inicializando ns3-ai: {e}")
                print(f"   Asegúrate de que la simulación NS-3 esté corriendo primero.")
        else:
            print(f"⚠️ Módulo ns3_ai no encontrado.")

    def run_interaction_loop(self, max_steps: int = 1000):
        """
        Ejecuta el bucle principal de interacción con NS-3
        """
        if not self.interface:
            print("❌ No hay interfaz ns3-ai válida. Ejecutando en modo fallback (simulado).")
            return self._run_simulated_loop(max_steps)

        print(f"🚀 Iniciando bucle de control (PID: {os.getpid()})...")
        print("   Esperando conexión con NS-3...")
        
        # Wait for simulation to start writing
        # (Ns3AiMsgInterface internally handles wait on receive)
        
        step = 0
        episode_reward = 0.0
        
        try:
            while step < max_steps:
                # 1. READ STATE from NS-3
                # GetCpp2PyStruct returns the struct defined in C++
                # In Python we assume it matches EnvState layout
                # Note: Ns3AiMsgInterface.GetCpp2PyStruct might return raw bytes or specialized object
                # We map it to our EnvState ctypes structure
                
                # Using lower-level access if high-level is opaque, but let's assume high-level usage
                # For robustness, we wrap the specific read call
                
                uid = self.interface.Recv() # Wait for message
                if uid < 0:
                    # End of simulation or error
                    break
                    
                raw_data = self.interface.GetCpp2PyStruct(EnvState)
                
                # Convert to Tensor
                state_np = np.array([
                    raw_data.buffer_occupancy,
                    raw_data.num_neighbors,
                    raw_data.recent_pdr,
                    raw_data.recent_delay,
                    raw_data.distance_to_dest,
                    raw_data.hops_to_dest,
                    raw_data.energy_level,
                    raw_data.avg_neighbor_load,
                    raw_data.packet_priority,
                    raw_data.time_in_queue
                ], dtype=np.float32)
                
                # 2. INFERENCE
                action_idx = 0
                if self.policy and HAS_TORCH:
                    with torch.no_grad():
                        state_tensor = torch.FloatTensor(state_np).unsqueeze(0)
                        probs, _ = self.policy(state_tensor)
                        action_idx = torch.argmax(probs, dim=1).item()
                else:
                    action_idx = np.random.randint(0, ACTION_DIM)
                
                # 3. WRITE ACTION to NS-3
                action_struct = AgentAction()
                action_struct.next_hop_id = action_idx
                action_struct.tx_power = 20.0 # dBm
                action_struct.priority = 0
                
                self.interface.SetPy2CppStruct(action_struct)
                self.interface.Send(uid) # Reply with same UID
                
                # 4. Optional: Calculate pseudo-reward for logging
                r = state_np[2] - (state_np[3] / 1000.0)
                episode_reward += r
                
                step += 1
                if step % 100 == 0:
                    print(f"   Step {step}: Action={action_idx}, PDR={state_np[2]:.2f}")
                    
        except KeyboardInterrupt:
            print("🛑 Interrupción de usuario.")
        except Exception as e:
            print(f"❌ Error en bucle: {e}")
        finally:
            # Cleanup is handled by ns3-ai destructor usually
            print("✅ Bucle finalizado.")

    def _run_simulated_loop(self, max_steps: int):
        """Loop de simulación para desarrollo sin NS-3"""
        print("🎮 DEBUG: Ejecutando bucle simulado...")
        for i in range(min(max_steps, 100)):
            time.sleep(0.05) # Simulate processing time
            if i % 20 == 0:
                print(f"   Simulated Step {i}: Action={np.random.randint(0, 5)}")
        print("✅ Simulación DEBUG finalizada.")

def main():
    agent = NS3AIAgent()
    agent.run_interaction_loop()

if __name__ == "__main__":
    main()
