"""
Integración NS3-AI para Deep Reinforcement Learning

Este módulo proporciona funciones para integrar ns3-ai con el sistema A2A,
permitiendo la optimización de protocolos de enrutamiento mediante DRL.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, List, Tuple
import numpy as np


def generate_ns3_ai_code(protocol: str, nodes: int, area_size: int) -> str:
    """
    Genera código Python para NS-3 con integración ns3-ai y PPO Agent (PyTorch)
    
    Args:
        protocol: Protocolo de enrutamiento (AODV, OLSR, etc.)
        nodes: Número de nodos
        area_size: Tamaño del área de simulación
        
    Returns:
        Código Python completo con ns3-ai y PPO
    """
    
    code = f'''#!/usr/bin/env python3
"""
Simulación NS-3 con PPO DRL Agent (PyTorch)
Protocolo: {protocol}
Nodos: {nodes}
Área: {area_size}x{area_size}m
"""

import sys
import os
sys.path.insert(0, 'build/lib/python3')

import ns.core
import ns.network
import ns.internet
import ns.wifi
import ns.mobility
import ns.applications
import ns.flow_monitor
import ns.{protocol.lower()}

# Importar PyTorch y utilidades
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    import numpy as np
    import json
    HAS_TORCH = True
except ImportError:
    print("⚠️  PyTorch no encontrado. Ejecutando en modo fallback (sin IA).")
    HAS_TORCH = False

# Configuración del entorno
STATE_DIM = 10
ACTION_DIM = 5  # 0: Default, 1: Alt Route, 2: Power+, 3: Power-, 4: Priority

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

class PPOAgent:
    """Agente PPO para inferencia y recolección de datos"""
    def __init__(self, state_dim, action_dim, model_path=None):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.policy = ActorCritic(state_dim, action_dim)
        self.memory = []  # Store trajectories: (state, action, log_prob, reward, val, done)
        
        if model_path and os.path.exists(model_path):
            try:
                self.policy.load_state_dict(torch.load(model_path))
                print(f"🤖 Modelo cargado desde {{model_path}}")
            except Exception as e:
                print(f"⚠️  Error cargando modelo: {{e}}")
        
        self.policy.eval()  # Inference mode

    def select_action(self, state):
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            probs, val = self.policy(state_tensor)
            dist = torch.distributions.Categorical(probs)
            action = dist.sample()
            log_prob = dist.log_prob(action)
            
        return action.item(), log_prob.item(), val.item()

    def store_transition(self, state, action, log_prob, reward, val, done):
        self.memory.append({{
            'state': state.tolist(),
            'action': action,
            'log_prob': log_prob,
            'reward': reward,
            'val': val,
            'done': done
        }})

    def save_memory(self, filename='ppo_experiences.json'):
        with open(filename, 'w') as f:
            json.dump(self.memory, f)
        print(f"💾 Experiencias guardadas en {{filename}}")

def get_network_state(node_id):
    """
    Obtiene el estado real del nodo desde NS-3
    Retorna vector normalizado de 10 dimensiones
    """
    # Placeholder: En producción conectar con Tracing de NS-3
    # Simulación de estado para demostración
    return np.random.rand(STATE_DIM)

def calculate_reward(pdr, delay, overhead):
    """R = w1*PDR - w2*Delay - w3*Overhead"""
    return 1.0 * pdr - 0.1 * delay - 0.5 * overhead

def main():
    print("="*80)
    print("Simulación NS-3 con PPO (PyTorch)")
    print("="*80)
    
    # 1. Configuración Semilla
    simulation_seed = 12345
    ns.core.RngSeedManager.SetSeed(simulation_seed)
    ns.core.RngSeedManager.SetRun(1)
    
    # 2. Configuración Red
    num_nodes = {nodes}
    simulation_time = 200.0
    
    nodes_container = ns.network.NodeContainer()
    nodes_container.Create(num_nodes)
    
    # WiFi, Movilidad, Internet Stack (Configuración estándar)
    wifi = ns.wifi.WifiHelper()
    wifi.SetStandard(ns.wifi.WIFI_STANDARD_80211a)
    phy = ns.wifi.YansWifiPhyHelper()
    channel = ns.wifi.YansWifiChannelHelper.Default()
    phy.SetChannel(channel.Create())
    mac = ns.wifi.WifiMacHelper()
    mac.SetType("ns3::AdhocWifiMac")
    devices = wifi.Install(phy, mac, nodes_container)
    
    mobility = ns.mobility.MobilityHelper()
    mobility.SetPositionAllocator("ns3::RandomRectanglePositionAllocator",
        "X", ns.core.StringValue("ns3::UniformRandomVariable[Min=0.0|Max={area_size}.0]"),
        "Y", ns.core.StringValue("ns3::UniformRandomVariable[Min=0.0|Max={area_size}.0]"))
    mobility.SetMobilityModel("ns3::RandomWaypointMobilityModel",
        "Speed", ns.core.StringValue("ns3::UniformRandomVariable[Min=5.0|Max=20.0]"),
        "Pause", ns.core.StringValue("ns3::ConstantRandomVariable[Constant=2.0]"))
    mobility.Install(nodes_container)
    
    internet = ns.internet.InternetStackHelper()
    routing = ns.{protocol.lower()}.{protocol}Helper()
    internet.SetRoutingHelper(routing)
    internet.Install(nodes_container)
    
    ipv4 = ns.internet.Ipv4AddressHelper()
    ipv4.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
    ipv4.Assign(devices)
    
    # 3. Inicializar PPO Agent
    agent = None
    if HAS_TORCH:
        model_path = "models/ppo_model.pth"
        agent = PPOAgent(STATE_DIM, ACTION_DIM, model_path)
        print("✅ Agente PPO inicializado")
    
    # 4. Tráfico
    port = 9
    server = ns.applications.UdpEchoServerHelper(port)
    server.Install(nodes_container.Get(0)).Start(ns.core.Seconds(1.0))
    
    client = ns.applications.UdpEchoClientHelper(ipv4.Assign(devices).GetAddress(0), port)
    client.SetAttribute("MaxPackets", ns.core.UintegerValue(1000))
    client.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(0.1)))
    client.SetAttribute("PacketSize", ns.core.UintegerValue(1024))
    for i in range(1, num_nodes):
        client.Install(nodes_container.Get(i)).Start(ns.core.Seconds(2.0))

    # 5. Loop de Control (Simulado)
    # En NS-3 real, esto se haría con eventos programados (Simulator::Schedule)
    # Aquí simulamos la interacción periódica
    
    step_time = 1.0
    current_time = 0.0
    
    print("🚀 Iniciando simulación...")
    
    # FlowMonitor
    flowmon = ns.flow_monitor.FlowMonitorHelper()
    monitor = flowmon.InstallAll()
    
    # Ejecutar simulación
    ns.core.Simulator.Stop(ns.core.Seconds(simulation_time))
    
    # NOTA: En una integración real profunda, usaríamos ns3-ai shared memory.
    # Aquí usamos un enfoque episódico simplificado para la tesis.
    ns.core.Simulator.Run()
    
    # Recolección de métricas post-simulación para entrenamiento
    monitor.CheckForLostPackets()
    classifier = flowmon.GetClassifier()
    stats = monitor.GetFlowStats()
    
    total_tx = 0
    total_rx = 0
    delay_sum = 0
    
    for flow_id, flow_stats in stats:
        total_tx += flow_stats.txPackets
        total_rx += flow_stats.rxPackets
        delay_sum += flow_stats.delaySum.GetSeconds()
        
    pdr = (total_rx / total_tx) * 100 if total_tx > 0 else 0
    avg_delay = (delay_sum / total_rx) if total_rx > 0 else 0
    overhead = 0.1 # Simulado
    
    print(f"📊 Resultados: PDR={{pdr:.2f}}%, Delay={{avg_delay:.4f}}s")
    
    # Guardar experiencia (Episodic update)
    if agent:
        # Asumimos un estado promedio del episodio
        state = get_network_state(0)
        action, log_prob, val = agent.select_action(state)
        reward = calculate_reward(pdr, avg_delay, overhead)
        
        agent.store_transition(state, action, log_prob, reward, val, done=True)
        agent.save_memory()

    ns.core.Simulator.Destroy()

if __name__ == "__main__":
    main()
'''
    return code


def generate_drl_training_code(protocol: str) -> str:
    """
    Genera código Python para entrenar el modelo PPO con PyTorch
    
    Args:
        protocol: Protocolo de enrutamiento
        
    Returns:
        Código Python para entrenamiento
    """
    
    code = f'''#!/usr/bin/env python3
"""
Entrenamiento PPO (Proximal Policy Optimization) para {protocol}
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import json
import numpy as np
import os

# Hiperparámetros PPO
LR = 0.0003
GAMMA = 0.99
EPS_CLIP = 0.2
K_EPOCHS = 4
BATCH_SIZE = 32

class ActorCritic(nn.Module):
    """Red Neuronal Actor-Critic (Debe coincidir con la de simulación)"""
    def __init__(self, state_dim, action_dim):
        super(ActorCritic, self).__init__()
        self.actor = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.Tanh(),
            nn.Linear(64, 32),
            nn.Tanh(),
            nn.Linear(32, action_dim),
            nn.Softmax(dim=-1)
        )
        self.critic = nn.Sequential(
            nn.Linear(state_dim, 64),
            nn.Tanh(),
            nn.Linear(64, 32),
            nn.Tanh(),
            nn.Linear(32, 1)
        )

    def forward(self, state):
        return self.actor(state), self.critic(state)
    
    def evaluate(self, state, action):
        probs, val = self.forward(state)
        dist = torch.distributions.Categorical(probs)
        action_logprobs = dist.log_prob(action)
        dist_entropy = dist.entropy()
        return action_logprobs, val, dist_entropy

class PPOTrainer:
    def __init__(self, state_dim, action_dim):
        self.policy = ActorCritic(state_dim, action_dim)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=LR)
        self.policy_old = ActorCritic(state_dim, action_dim)
        self.policy_old.load_state_dict(self.policy.state_dict())
        self.mse_loss = nn.MSELoss()
        
        # Cargar modelo previo si existe
        if os.path.exists("models/ppo_model.pth"):
            self.policy.load_state_dict(torch.load("models/ppo_model.pth"))
            self.policy_old.load_state_dict(self.policy.state_dict())
            print("🔄 Modelo previo cargado")

    def update(self, memory):
        # Convertir lista de dicts a tensores
        states = torch.tensor([m['state'] for m in memory], dtype=torch.float32)
        actions = torch.tensor([m['action'] for m in memory], dtype=torch.float32)
        old_log_probs = torch.tensor([m['log_prob'] for m in memory], dtype=torch.float32)
        rewards = torch.tensor([m['reward'] for m in memory], dtype=torch.float32)
        
        # Normalizar rewards (opcional pero recomendado)
        rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-5)
        
        # PPO Update Loop
        for _ in range(K_EPOCHS):
            # Evaluar acciones antiguas
            logprobs, state_values, dist_entropy = self.policy.evaluate(states, actions)
            
            # Calcular ratios
            ratios = torch.exp(logprobs - old_log_probs)
            
            # Calcular ventajas (Advantages)
            advantages = rewards - state_values.detach().squeeze()
            
            # Surrogate Loss
            surr1 = ratios * advantages
            surr2 = torch.clamp(ratios, 1-EPS_CLIP, 1+EPS_CLIP) * advantages
            
            # Loss total: Actor loss + Critic loss - Entropy bonus
            loss = -torch.min(surr1, surr2) + 0.5*self.mse_loss(state_values.squeeze(), rewards) - 0.01*dist_entropy
            
            # Backpropagation
            self.optimizer.zero_grad()
            loss.mean().backward()
            self.optimizer.step()
            
        # Actualizar policy antigua
        self.policy_old.load_state_dict(self.policy.state_dict())
        
        return loss.mean().item()

    def save(self, path="models/ppo_model.pth"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save(self.policy.state_dict(), path)
        print(f"💾 Modelo guardado en {{path}}")

def main():
    print("🏋️  Iniciando entrenamiento PPO...")
    
    # Cargar datos
    try:
        with open('ppo_experiences.json', 'r') as f:
            memory = json.load(f)
    except FileNotFoundError:
        print("❌ No se encontraron experiencias (ppo_experiences.json)")
        return
        
    if not memory:
        print("⚠️  Memoria vacía")
        return

    # Configurar Trainer
    state_dim = 10
    action_dim = 5
    trainer = PPOTrainer(state_dim, action_dim)
    
    # Entrenar
    loss = trainer.update(memory)
    print(f"✅ Entrenamiento completado. Loss final: {{loss:.4f}}")
    
    # Guardar
    trainer.save()

if __name__ == "__main__":
    main()
'''
    return code


def get_ns3_ai_installation_instructions() -> str:
    """
    Retorna instrucciones para instalar ns3-ai
    
    Returns:
        Instrucciones en formato Markdown
    """
    
    instructions = """
# Instalación de ns3-ai

## Requisitos Previos

- NS-3 3.36 o superior
- Python 3.8+
- PyTorch o TensorFlow

## Pasos de Instalación

### 1. Clonar ns3-ai

```bash
cd ~/ns-3-dev/contrib
git clone https://github.com/hust-diangroup/ns3-ai.git
```

### 2. Configurar NS-3 con ns3-ai

```bash
cd ~/ns-3-dev
./ns3 configure --enable-examples --enable-tests
./ns3 build
```

### 3. Verificar Instalación

```bash
./ns3 run "ns3-ai-gym-test"
```

Si la prueba pasa, ns3-ai está correctamente instalado.

## Uso con Sistema A2A

El sistema A2A detectará automáticamente si ns3-ai está disponible y
generará código compatible.

Para habilitar DRL:

```python
# En main.py o al ejecutar
python main.py --enable-drl
```

## Referencias

- [ns3-ai GitHub](https://github.com/hust-diangroup/ns3-ai)
- [ns3-ai Documentation](https://github.com/hust-diangroup/ns3-ai/wiki)
"""
    
    return instructions


# Funciones auxiliares para el optimizer

def extract_drl_parameters(optimization_proposal: str) -> Dict:
    """
    Extrae parámetros de DRL de la propuesta del optimizer
    
    Args:
        optimization_proposal: Texto de la propuesta
        
    Returns:
        Diccionario con parámetros
    """
    params = {
        'learning_rate': 0.001,
        'discount_factor': 0.99,
        'epsilon': 0.1,
        'batch_size': 32,
        'memory_size': 10000
    }
    
    # TODO: Parsear propuesta y extraer parámetros
    
    return params


def should_use_drl(metrics: Dict) -> bool:
    """
    Determina si se debe usar DRL basándose en las métricas
    
    Args:
        metrics: Métricas de la simulación
        
    Returns:
        True si se recomienda DRL
    """
    # Usar DRL si:
    # - PDR < 80%
    # - Delay > 150ms
    # - Success rate < 70%
    
    pdr = metrics.get('avg_pdr', 100)
    delay = metrics.get('avg_delay', 0)
    success_rate = metrics.get('success_rate', 100)
    
    if pdr < 80 or delay > 150 or success_rate < 70:
        return True
    
    return False
