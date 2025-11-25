#!/usr/bin/env python3
"""
Simulación NS-3 con integración ns3-ai
Este script demuestra cómo conectar NS-3 con el agente Python PPO usando memoria compartida.
"""

import sys
import ns.core
import ns.network
import ns.internet
import ns.mobility
import ns.wifi
import ns.applications
import ns.flow_monitor
import ns.aodv

# Intentar importar ns3_ai
try:
    from ns3_ai import RingBuffer, SharedMemory
    HAS_NS3_AI = True
except ImportError:
    HAS_NS3_AI = False
    print("⚠️ ns3-ai no instalado. La simulación correrá sin IA.")

def main():
    # 1. Configuración Básica
    simulation_time = 100.0
    num_nodes = 20
    
    # 2. Configuración de Memoria Compartida (ns3-ai)
    rb = None
    if HAS_NS3_AI:
        # Crear RingBuffer: "ns3_ai_shm", tamaño 4096
        # Debe coincidir con el lado Python
        rb = RingBuffer("ns3_ai_shm", 4096)
        print("✅ ns3-ai RingBuffer inicializado")

    # 3. Crear Topología
    nodes = ns.network.NodeContainer()
    nodes.Create(num_nodes)
    
    wifi = ns.wifi.WifiHelper()
    wifi.SetStandard(ns.wifi.WIFI_STANDARD_80211a)
    
    phy = ns.wifi.YansWifiPhyHelper()
    channel = ns.wifi.YansWifiChannelHelper.Default()
    phy.SetChannel(channel.Create())
    
    mac = ns.wifi.WifiMacHelper()
    mac.SetType("ns3::AdhocWifiMac")
    
    devices = wifi.Install(phy, mac, nodes)
    
    # 4. Movilidad
    mobility = ns.mobility.MobilityHelper()
    mobility.SetPositionAllocator("ns3::RandomRectanglePositionAllocator",
        "X", ns.core.StringValue("ns3::UniformRandomVariable[Min=0.0|Max=500.0]"),
        "Y", ns.core.StringValue("ns3::UniformRandomVariable[Min=0.0|Max=500.0]"))
    mobility.SetMobilityModel("ns3::RandomWaypointMobilityModel",
        "Speed", ns.core.StringValue("ns3::UniformRandomVariable[Min=5.0|Max=20.0]"),
        "Pause", ns.core.StringValue("ns3::ConstantRandomVariable[Constant=2.0]"))
    mobility.Install(nodes)
    
    # 5. Internet Stack & Routing (AODV)
    internet = ns.internet.InternetStackHelper()
    aodv = ns.aodv.AodvHelper()
    internet.SetRoutingHelper(aodv)
    internet.Install(nodes)
    
    ipv4 = ns.internet.Ipv4AddressHelper()
    ipv4.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
    ipv4.Assign(devices)
    
    # 6. Tráfico
    udp_echo_server = ns.applications.UdpEchoServerHelper(9)
    server_apps = udp_echo_server.Install(nodes.Get(0))
    server_apps.Start(ns.core.Seconds(1.0))
    server_apps.Stop(ns.core.Seconds(simulation_time))
    
    udp_echo_client = ns.applications.UdpEchoClientHelper(
        ipv4.Assign(devices).GetAddress(0), 9)
    udp_echo_client.SetAttribute("MaxPackets", ns.core.UintegerValue(100))
    udp_echo_client.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(1.0)))
    udp_echo_client.SetAttribute("PacketSize", ns.core.UintegerValue(1024))
    
    client_apps = udp_echo_client.Install(nodes.Get(num_nodes - 1))
    client_apps.Start(ns.core.Seconds(2.0))
    client_apps.Stop(ns.core.Seconds(simulation_time))

    # 7. Bucle de Control IA (Simulado con eventos)
    # En una implementación real C++, esto sería un AiModel::GetAction()
    # Aquí usamos eventos de Python para simular la interacción periódica
    
    def interaction_step():
        if not HAS_NS3_AI or rb is None:
            return
            
        # Leer acción (si hay)
        # int action; rb.get(&action, sizeof(int));
        
        # Escribir estado
        # float state[10]; ... llenar state ...
        # rb.put(state, sizeof(float)*10);
        
        # Reprogramar
        ns.core.Simulator.Schedule(ns.core.Seconds(0.1), interaction_step)

    ns.core.Simulator.Schedule(ns.core.Seconds(0.1), interaction_step)

    # 8. Ejecutar
    print("🚀 Ejecutando simulación...")
    ns.core.Simulator.Stop(ns.core.Seconds(simulation_time))
    ns.core.Simulator.Run()
    
    if rb:
        # rb.free() # Liberar recursos si es necesario
        pass
        
    ns.core.Simulator.Destroy()
    print("✅ Simulación finalizada")

if __name__ == "__main__":
    main()
