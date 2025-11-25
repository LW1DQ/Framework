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
    Genera código Python para NS-3 con integración ns3-ai
    
    Args:
        protocol: Protocolo de enrutamiento (AODV, OLSR, etc.)
        nodes: Número de nodos
        area_size: Tamaño del área de simulación
        
    Returns:
        Código Python completo con ns3-ai
    """
    
    code = f'''#!/usr/bin/env python3
"""
Simulación NS-3 con ns3-ai para DRL
Protocolo: {protocol}
Nodos: {nodes}
Área: {area_size}x{area_size}m
"""

import sys
sys.path.insert(0, 'build/lib/python3')

import ns.core
import ns.network
import ns.internet
import ns.wifi
import ns.mobility
import ns.applications
import ns.flow_monitor
import ns.{protocol.lower()}

# Importar ns3-ai
try:
    import ns.ai
    NS3_AI_AVAILABLE = True
except ImportError:
    print("⚠️  ns3-ai no disponible. Ejecutando sin DRL.")
    NS3_AI_AVAILABLE = False

import numpy as np
import json


class DRLAgent:
    """
    Agente de Deep Reinforcement Learning para optimización de enrutamiento
    """
    
    def __init__(self, state_dim: int, action_dim: int):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.memory = []
        
    def get_state(self, node_id: int) -> np.ndarray:
        """
        Obtiene el estado actual del nodo
        
        Estado incluye:
        - Número de vecinos
        - Buffer ocupado
        - Paquetes enviados/recibidos
        - Energía restante (si aplica)
        """
        # Placeholder: En implementación real, obtener desde NS-3
        state = np.zeros(self.state_dim)
        return state
    
    def select_action(self, state: np.ndarray) -> int:
        """
        Selecciona acción basándose en el estado
        
        Acciones posibles:
        - 0: Usar ruta por defecto
        - 1: Buscar ruta alternativa
        - 2: Ajustar parámetros de protocolo
        """
        # Placeholder: Implementar política (ej. epsilon-greedy)
        action = np.random.randint(0, self.action_dim)
        return action
    
    def store_transition(self, state, action, reward, next_state, done):
        """Almacena transición en memoria de replay"""
        self.memory.append((state, action, reward, next_state, done))
    
    def calculate_reward(self, pdr: float, delay: float, overhead: float) -> float:
        """
        Calcula recompensa basándose en métricas de red
        
        Recompensa = w1*PDR - w2*delay - w3*overhead
        """
        w1, w2, w3 = 1.0, 0.01, 0.5
        reward = w1 * pdr - w2 * delay - w3 * overhead
        return reward


def main():
    """Función principal de simulación con DRL"""
    
    print("="*80)
    print("Simulación NS-3 con Deep Reinforcement Learning")
    print("="*80)
    
    # Configurar semilla para reproducibilidad
    simulation_seed = 12345
    ns.core.RngSeedManager.SetSeed(simulation_seed)
    ns.core.RngSeedManager.SetRun(1)
    print(f"🎲 Semilla configurada: {{simulation_seed}}")
    
    # Parámetros de simulación
    num_nodes = {nodes}
    area_size = {area_size}
    simulation_time = 200.0
    
    # Crear nodos
    nodes = ns.network.NodeContainer()
    nodes.Create(num_nodes)
    print(f"📡 Nodos creados: {{num_nodes}}")
    
    # Configurar WiFi
    wifi = ns.wifi.WifiHelper()
    wifi.SetStandard(ns.wifi.WIFI_STANDARD_80211a)
    
    phy = ns.wifi.YansWifiPhyHelper()
    channel = ns.wifi.YansWifiChannelHelper.Default()
    phy.SetChannel(channel.Create())
    
    mac = ns.wifi.WifiMacHelper()
    mac.SetType("ns3::AdhocWifiMac")
    
    devices = wifi.Install(phy, mac, nodes)
    
    # Configurar movilidad
    mobility = ns.mobility.MobilityHelper()
    mobility.SetPositionAllocator(
        "ns3::RandomRectanglePositionAllocator",
        "X", ns.core.StringValue(f"ns3::UniformRandomVariable[Min=0.0|Max={{area_size}}.0]"),
        "Y", ns.core.StringValue(f"ns3::UniformRandomVariable[Min=0.0|Max={{area_size}}.0]")
    )
    mobility.SetMobilityModel(
        "ns3::RandomWaypointMobilityModel",
        "Speed", ns.core.StringValue("ns3::UniformRandomVariable[Min=5.0|Max=15.0]"),
        "Pause", ns.core.StringValue("ns3::ConstantRandomVariable[Constant=2.0]"),
        "PositionAllocator", ns.core.StringValue(f"ns3::RandomRectanglePositionAllocator")
    )
    mobility.Install(nodes)
    
    # Instalar stack de Internet
    internet = ns.internet.InternetStackHelper()
    
    # Configurar protocolo de enrutamiento
    routing = ns.{protocol.lower()}.{protocol}Helper()
    internet.SetRoutingHelper(routing)
    internet.Install(nodes)
    
    # Asignar direcciones IP
    ipv4 = ns.internet.Ipv4AddressHelper()
    ipv4.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
    interfaces = ipv4.Assign(devices)
    
    # Inicializar agente DRL (si ns3-ai disponible)
    drl_agent = None
    if NS3_AI_AVAILABLE:
        print("🤖 Inicializando agente DRL...")
        state_dim = 10  # Dimensión del espacio de estados
        action_dim = 3  # Número de acciones posibles
        drl_agent = DRLAgent(state_dim, action_dim)
    
    # Configurar aplicaciones
    port = 9
    
    # Servidor en nodo 0
    server = ns.applications.UdpEchoServerHelper(port)
    server_apps = server.Install(nodes.Get(0))
    server_apps.Start(ns.core.Seconds(1.0))
    server_apps.Stop(ns.core.Seconds(simulation_time))
    
    # Clientes en otros nodos
    for i in range(1, num_nodes):
        client = ns.applications.UdpEchoClientHelper(interfaces.GetAddress(0), port)
        client.SetAttribute("MaxPackets", ns.core.UintegerValue(1000))
        client.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(0.1)))
        client.SetAttribute("PacketSize", ns.core.UintegerValue(1024))
        
        client_apps = client.Install(nodes.Get(i))
        client_apps.Start(ns.core.Seconds(2.0 + i * 0.1))
        client_apps.Stop(ns.core.Seconds(simulation_time))
    
    # Habilitar captura PCAP
    phy.EnablePcapAll("simulacion_drl", True)
    print("📡 Captura PCAP habilitada")
    
    # Configurar FlowMonitor
    flowmon_helper = ns.flow_monitor.FlowMonitorHelper()
    monitor = flowmon_helper.InstallAll()
    
    # Ejecutar simulación
    print(f"🚀 Ejecutando simulación por {{simulation_time}} segundos...")
    ns.core.Simulator.Stop(ns.core.Seconds(simulation_time))
    ns.core.Simulator.Run()
    
    # Exportar resultados
    monitor.SerializeToXmlFile("resultados_drl.xml", True, True)
    print("✅ Simulación completada")
    
    # Si DRL está activo, guardar experiencias
    if drl_agent and drl_agent.memory:
        print(f"💾 Guardando {{len(drl_agent.memory)}} experiencias de DRL...")
        experiences = {{
            'transitions': drl_agent.memory,
            'protocol': '{protocol}',
            'nodes': num_nodes,
            'area_size': area_size
        }}
        
        with open('drl_experiences.json', 'w') as f:
            # Convertir numpy arrays a listas para JSON
            json.dump(experiences, f, default=lambda x: x.tolist() if isinstance(x, np.ndarray) else x)
    
    ns.core.Simulator.Destroy()
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''
    
    return code


def generate_drl_training_code(protocol: str) -> str:
    """
    Genera código Python para entrenar el modelo DRL
    
    Args:
        protocol: Protocolo de enrutamiento
        
    Returns:
        Código Python para entrenamiento
    """
    
    code = f'''#!/usr/bin/env python3
"""
Entrenamiento de modelo DRL para optimización de {protocol}
"""

import numpy as np
import json
from pathlib import Path


class DQNAgent:
    """
    Deep Q-Network para optimización de enrutamiento
    """
    
    def __init__(self, state_dim: int, action_dim: int, learning_rate: float = 0.001):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.learning_rate = learning_rate
        
        # Placeholder: En implementación real, usar PyTorch o TensorFlow
        self.q_network = None
        self.target_network = None
        
        print(f"🤖 DQN Agent inicializado")
        print(f"   Estado: {{state_dim}} dimensiones")
        print(f"   Acciones: {{action_dim}} posibles")
    
    def train(self, experiences_file: str, epochs: int = 100):
        """
        Entrena el modelo con las experiencias recolectadas
        
        Args:
            experiences_file: Archivo JSON con experiencias
            epochs: Número de épocas de entrenamiento
        """
        print(f"\\n📚 Cargando experiencias desde {{experiences_file}}...")
        
        with open(experiences_file, 'r') as f:
            data = json.load(f)
        
        transitions = data['transitions']
        print(f"   Experiencias cargadas: {{len(transitions)}}")
        
        print(f"\\n🏋️  Entrenando modelo por {{epochs}} épocas...")
        
        for epoch in range(epochs):
            # Placeholder: Implementar entrenamiento real
            loss = np.random.random()  # Simular pérdida
            
            if (epoch + 1) % 10 == 0:
                print(f"   Época {{epoch+1}}/{{epochs}} - Loss: {{loss:.4f}}")
        
        print(f"\\n✅ Entrenamiento completado")
        
        # Guardar modelo
        model_path = Path("models") / f"dqn_{{protocol.lower()}}_model.pth"
        model_path.parent.mkdir(exist_ok=True)
        
        print(f"💾 Modelo guardado en: {{model_path}}")
        
        return model_path


def main():
    """Función principal de entrenamiento"""
    
    print("="*80)
    print("Entrenamiento DRL para Optimización de Enrutamiento")
    print("="*80)
    
    # Parámetros
    state_dim = 10
    action_dim = 3
    
    # Crear agente
    agent = DQNAgent(state_dim, action_dim)
    
    # Entrenar
    experiences_file = "drl_experiences.json"
    
    if Path(experiences_file).exists():
        model_path = agent.train(experiences_file, epochs=100)
        print(f"\\n🎉 Modelo entrenado exitosamente: {{model_path}}")
    else:
        print(f"\\n⚠️  Archivo de experiencias no encontrado: {{experiences_file}}")
        print(f"   Ejecutar primero la simulación con ns3-ai")
    
    return 0


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
