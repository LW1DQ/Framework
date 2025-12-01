/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2025 Sistema A2A
 *
 * DRL Routing Agent - Agente de enrutamiento con Deep Reinforcement Learning
 * Integración con ns3-ai para comunicación Python-C++
 */

#ifndef DRL_ROUTING_AGENT_H
#define DRL_ROUTING_AGENT_H

#include "ns3/object.h"
#include "ns3/node.h"
#include "ns3/ipv4-routing-protocol.h"
#include "ns3/ipv4-address.h"
#include "ns3/packet.h"
#include "ns3/vector.h"
#include <vector>

namespace ns3 {

/**
 * \brief Estructura de estado del entorno para el agente DRL
 * 
 * Esta estructura se comparte con Python vía memoria compartida (ns3-ai)
 */
struct EnvState {
    float buffer_occupancy;      // Ocupación del buffer (0-1)
    float num_neighbors;         // Número de vecinos activos
    float recent_pdr;            // PDR reciente (últimos N paquetes)
    float recent_delay;          // Delay promedio reciente (ms)
    float distance_to_dest;      // Distancia euclidiana al destino (m)
    float hops_to_dest;          // Número de saltos estimado
    float energy_level;          // Nivel de energía (0-1, si aplica)
    float avg_neighbor_load;     // Carga promedio de vecinos
    float packet_priority;       // Prioridad del paquete actual
    float time_in_queue;         // Tiempo en cola (ms)
};

/**
 * \brief Estructura de acción del agente DRL
 * 
 * Esta estructura se recibe desde Python vía memoria compartida
 */
struct AgentAction {
    int next_hop_id;            // ID del vecino seleccionado como siguiente salto
    float tx_power;             // Potencia de transmisión (0.1-1.0)
    int priority;               // Prioridad asignada al paquete (0-2)
};

/**
 * \brief Agente de enrutamiento con Deep Reinforcement Learning
 * 
 * Este agente se integra con el protocolo de enrutamiento existente
 * y usa DRL para tomar decisiones de enrutamiento optimizadas.
 */
class DrlRoutingAgent : public Object
{
public:
    /**
     * \brief Get the type ID.
     * \return the object TypeId
     */
    static TypeId GetTypeId (void);

    /**
     * Constructor
     */
    DrlRoutingAgent ();

    /**
     * Destructor
     */
    virtual ~DrlRoutingAgent ();

    /**
     * \brief Inicializa el agente con un nodo
     * \param node Puntero al nodo NS-3
     */
    void Initialize (Ptr<Node> node);

    /**
     * \brief Selecciona el siguiente salto usando DRL
     * \param packet Paquete a enrutar
     * \param dest Dirección IP de destino
     * \return ID del vecino seleccionado (-1 si falla)
     */
    int SelectNextHop (Ptr<const Packet> packet, Ipv4Address dest);

    /**
     * \brief Actualiza estadísticas tras envío de paquete
     * \param success Si el envío fue exitoso
     * \param delay Delay experimentado (ms)
     */
    void UpdateStatistics (bool success, double delay);

    /**
     * \brief Obtiene el estado actual del entorno
     * \return Estructura EnvState con el estado
     */
    EnvState GetCurrentState () const;

    /**
     * \brief Habilita/deshabilita el agente DRL
     * \param enable True para habilitar
     */
    void SetEnabled (bool enable);

    /**
     * \brief Verifica si el agente está habilitado
     * \return True si está habilitado
     */
    bool IsEnabled () const;

private:
    /**
     * \brief Actualiza el estado interno del agente
     */
    void UpdateState ();

    /**
     * \brief Calcula la distancia a un destino
     * \param dest Dirección IP de destino
     * \return Distancia en metros
     */
    double CalculateDistanceToDestination (Ipv4Address dest) const;

    /**
     * \brief Obtiene la lista de vecinos activos
     * \return Vector de IDs de vecinos
     */
    std::vector<uint32_t> GetActiveNeighbors () const;

    /**
     * \brief Calcula el PDR reciente
     * \return PDR (0-1)
     */
    float CalculateRecentPDR () const;

    /**
     * \brief Calcula el delay promedio reciente
     * \return Delay en ms
     */
    float CalculateRecentDelay () const;

    // Miembros privados
    Ptr<Node> m_node;                    ///< Nodo asociado
    bool m_enabled;                      ///< Si el agente está habilitado
    EnvState m_currentState;             ///< Estado actual
    AgentAction m_lastAction;            ///< Última acción tomada

    // Estadísticas
    uint32_t m_packetsSent;              ///< Paquetes enviados
    uint32_t m_packetsReceived;          ///< Paquetes recibidos
    double m_totalDelay;                 ///< Delay acumulado
    std::vector<bool> m_recentResults;   ///< Resultados recientes (para PDR)
    std::vector<double> m_recentDelays;  ///< Delays recientes

    // Configuración
    uint32_t m_historySize;              ///< Tamaño del historial para estadísticas
};

} // namespace ns3

#endif /* DRL_ROUTING_AGENT_H */
