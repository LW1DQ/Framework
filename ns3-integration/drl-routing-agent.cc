/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2025 Sistema A2A
 *
 * Implementación del DRL Routing Agent
 */

#include "drl-routing-agent.h"
#include "ns3/log.h"
#include "ns3/simulator.h"
#include "ns3/mobility-model.h"
#include "ns3/ipv4.h"
#include "ns3/ipv4-routing-protocol.h"

namespace ns3 {

NS_LOG_COMPONENT_DEFINE ("DrlRoutingAgent");

NS_OBJECT_ENSURE_REGISTERED (DrlRoutingAgent);

TypeId
DrlRoutingAgent::GetTypeId (void)
{
    static TypeId tid = TypeId ("ns3::DrlRoutingAgent")
        .SetParent<Object> ()
        .SetGroupName ("DrlRouting")
        .AddConstructor<DrlRoutingAgent> ()
        .AddAttribute ("HistorySize",
                       "Tamaño del historial para estadísticas",
                       UintegerValue (100),
                       MakeUintegerAccessor (&DrlRoutingAgent::m_historySize),
                       MakeUintegerChecker<uint32_t> ())
        .AddAttribute ("Enabled",
                       "Si el agente DRL está habilitado",
                       BooleanValue (true),
                       MakeBooleanAccessor (&DrlRoutingAgent::m_enabled),
                       MakeBooleanChecker ())
    ;
    return tid;
}

DrlRoutingAgent::DrlRoutingAgent ()
    : m_node (nullptr),
      m_enabled (true),
      m_packetsSent (0),
      m_packetsReceived (0),
      m_totalDelay (0.0),
      m_historySize (100)
{
    NS_LOG_FUNCTION (this);
    
    // Inicializar estado
    m_currentState.buffer_occupancy = 0.0;
    m_currentState.num_neighbors = 0.0;
    m_currentState.recent_pdr = 1.0;
    m_currentState.recent_delay = 0.0;
    m_currentState.distance_to_dest = 0.0;
    m_currentState.hops_to_dest = 0.0;
    m_currentState.energy_level = 1.0;
    m_currentState.avg_neighbor_load = 0.0;
    m_currentState.packet_priority = 0.0;
    m_currentState.time_in_queue = 0.0;
    
    // Inicializar acción
    m_lastAction.next_hop_id = -1;
    m_lastAction.tx_power = 1.0;
    m_lastAction.priority = 0;
}

DrlRoutingAgent::~DrlRoutingAgent ()
{
    NS_LOG_FUNCTION (this);
}

void
DrlRoutingAgent::Initialize (Ptr<Node> node)
{
    NS_LOG_FUNCTION (this << node);
    m_node = node;
    UpdateState ();
}

int
DrlRoutingAgent::SelectNextHop (Ptr<const Packet> packet, Ipv4Address dest)
{
    NS_LOG_FUNCTION (this << packet << dest);
    
    if (!m_enabled)
    {
        NS_LOG_DEBUG ("Agente DRL deshabilitado");
        return -1;
    }
    
    // Actualizar estado antes de tomar decisión
    UpdateState ();
    
    // Obtener vecinos activos
    std::vector<uint32_t> neighbors = GetActiveNeighbors ();
    
    if (neighbors.empty ())
    {
        NS_LOG_WARN ("No hay vecinos disponibles");
        return -1;
    }
    
    // AQUÍ SE INTEGRARÍA CON ns3-ai PARA OBTENER ACCIÓN DESDE PYTHON
    // Por ahora, selección simple basada en distancia
    
    // Seleccionar vecino más cercano al destino (heurística simple)
    int bestNeighbor = -1;
    double minDistance = std::numeric_limits<double>::max ();
    
    for (uint32_t neighborId : neighbors)
    {
        // Obtener posición del vecino
        Ptr<Node> neighborNode = NodeList::GetNode (neighborId);
        Ptr<MobilityModel> neighborMobility = neighborNode->GetObject<MobilityModel> ();
        
        if (neighborMobility)
        {
            Vector neighborPos = neighborMobility->GetPosition ();
            
            // Calcular distancia al destino (simplificado)
            // En implementación real, buscaríamos el nodo con la IP destino
            double distance = neighborPos.GetLength ();
            
            if (distance < minDistance)
            {
                minDistance = distance;
                bestNeighbor = neighborId;
            }
        }
    }
    
    // Guardar acción tomada
    m_lastAction.next_hop_id = bestNeighbor;
    m_lastAction.tx_power = 1.0;
    m_lastAction.priority = 0;
    
    NS_LOG_DEBUG ("Seleccionado vecino " << bestNeighbor << " como siguiente salto");
    
    return bestNeighbor;
}

void
DrlRoutingAgent::UpdateStatistics (bool success, double delay)
{
    NS_LOG_FUNCTION (this << success << delay);
    
    if (success)
    {
        m_packetsReceived++;
        m_totalDelay += delay;
    }
    m_packetsSent++;
    
    // Actualizar historial reciente
    m_recentResults.push_back (success);
    m_recentDelays.push_back (delay);
    
    // Mantener tamaño del historial
    if (m_recentResults.size () > m_historySize)
    {
        m_recentResults.erase (m_recentResults.begin ());
        m_recentDelays.erase (m_recentDelays.begin ());
    }
    
    // Actualizar estado
    UpdateState ();
}

EnvState
DrlRoutingAgent::GetCurrentState () const
{
    return m_currentState;
}

void
DrlRoutingAgent::SetEnabled (bool enable)
{
    NS_LOG_FUNCTION (this << enable);
    m_enabled = enable;
}

bool
DrlRoutingAgent::IsEnabled () const
{
    return m_enabled;
}

void
DrlRoutingAgent::UpdateState ()
{
    NS_LOG_FUNCTION (this);
    
    if (!m_node)
    {
        return;
    }
    
    // Actualizar número de vecinos
    std::vector<uint32_t> neighbors = GetActiveNeighbors ();
    m_currentState.num_neighbors = static_cast<float> (neighbors.size ());
    
    // Actualizar PDR reciente
    m_currentState.recent_pdr = CalculateRecentPDR ();
    
    // Actualizar delay reciente
    m_currentState.recent_delay = CalculateRecentDelay ();
    
    // Actualizar ocupación de buffer (simplificado)
    // En implementación real, consultaríamos la cola del dispositivo
    m_currentState.buffer_occupancy = 0.5f; // Placeholder
    
    // Actualizar nivel de energía (si aplica)
    // En implementación real, consultaríamos el modelo de energía
    m_currentState.energy_level = 1.0f; // Placeholder
    
    NS_LOG_DEBUG ("Estado actualizado: neighbors=" << m_currentState.num_neighbors
                  << " pdr=" << m_currentState.recent_pdr
                  << " delay=" << m_currentState.recent_delay);
}

double
DrlRoutingAgent::CalculateDistanceToDestination (Ipv4Address dest) const
{
    NS_LOG_FUNCTION (this << dest);
    
    if (!m_node)
    {
        return 0.0;
    }
    
    Ptr<MobilityModel> mobility = m_node->GetObject<MobilityModel> ();
    if (!mobility)
    {
        return 0.0;
    }
    
    Vector myPos = mobility->GetPosition ();
    
    // En implementación real, buscaríamos el nodo con la IP destino
    // y calcularíamos la distancia euclidiana
    // Por ahora, retornamos un valor placeholder
    
    return 100.0; // Placeholder
}

std::vector<uint32_t>
DrlRoutingAgent::GetActiveNeighbors () const
{
    NS_LOG_FUNCTION (this);
    
    std::vector<uint32_t> neighbors;
    
    if (!m_node)
    {
        return neighbors;
    }
    
    // En implementación real, consultaríamos la tabla de vecinos
    // del protocolo de enrutamiento (AODV, OLSR, etc.)
    
    // Por ahora, retornamos vecinos simulados
    // Esto debería integrarse con el protocolo de enrutamiento real
    
    uint32_t nodeId = m_node->GetId ();
    uint32_t nNodes = NodeList::GetNNodes ();
    
    // Considerar todos los nodos excepto el propio como vecinos potenciales
    // En implementación real, solo incluiríamos vecinos en rango de comunicación
    for (uint32_t i = 0; i < nNodes; i++)
    {
        if (i != nodeId)
        {
            neighbors.push_back (i);
        }
    }
    
    return neighbors;
}

float
DrlRoutingAgent::CalculateRecentPDR () const
{
    NS_LOG_FUNCTION (this);
    
    if (m_recentResults.empty ())
    {
        return 1.0f;
    }
    
    uint32_t successes = 0;
    for (bool result : m_recentResults)
    {
        if (result)
        {
            successes++;
        }
    }
    
    return static_cast<float> (successes) / static_cast<float> (m_recentResults.size ());
}

float
DrlRoutingAgent::CalculateRecentDelay () const
{
    NS_LOG_FUNCTION (this);
    
    if (m_recentDelays.empty ())
    {
        return 0.0f;
    }
    
    double sum = 0.0;
    for (double delay : m_recentDelays)
    {
        sum += delay;
    }
    
    return static_cast<float> (sum / m_recentDelays.size ());
}

} // namespace ns3
