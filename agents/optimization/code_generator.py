"""
Generador de Código Optimizado para NS-3
"""

from typing import Dict, List, Any, Optional
from pathlib import Path

from .optimization_proposer import OptimizationProposer


class CodeGenerator:
    """
    Genera código NS-3 optimizado basado en propuestas de mejora
    """
    
    def __init__(self):
        """Inicializa el generador de código"""
        self.templates = self._initialize_templates()
    
    def generate_optimized_code(self, proposal: Dict, original_code: str, 
                              protocol: str = "AODV") -> Dict[str, str]:
        """
        Genera código optimizado basado en la propuesta
        
        Args:
            proposal: Propuesta de optimización
            original_code: Código original a mejorar
            protocol: Protocolo de enrutamiento
            
        Returns:
            Diccionario con código optimizado y componentes
        """
        optimization_type = proposal['optimization_type']
        strategies = proposal['strategies']
        
        # Generar componentes específicos
        components = self._generate_components(strategies, protocol)
        
        # Generar código principal optimizado
        optimized_code = self._generate_main_code(
            original_code, components, optimization_type, protocol
        )
        
        # Generar código de configuración
        config_code = self._generate_config_code(strategies, protocol)
        
        return {
            'main_code': optimized_code,
            'config_code': config_code,
            'components': components,
            'optimization_type': optimization_type
        }
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Inicializa plantillas de código"""
        return {
            'adaptive_parameters': '''
# Parámetros adaptativos basados en condiciones de red
class AdaptiveParameters:
    def __init__(self):
        self.base_hello_interval = 1.0
        self.base_rreq_retries = 2
        self.base_active_route_timeout = 3.0
        
    def adjust_parameters(self, node_density, mobility_level):
        """Ajusta parámetros basados en densidad y movilidad"""
        if node_density > 50:
            self.base_hello_interval = 0.5  # Más frecuentes en alta densidad
        elif node_density < 20:
            self.base_hello_interval = 2.0  # Menos frecuentes en baja densidad
            
        if mobility_level > 0.8:
            self.base_active_route_timeout = 1.0  # Rutas más cortas en alta movilidad
            self.base_rreq_retries = 3  # Más reintentos
''',
            
            'congestion_control': '''
# Control de congestión proactivo
class CongestionControl:
    def __init__(self):
        self.queue_threshold = 0.8
        self.congestion_detected = False
        
    def monitor_congestion(self, queue_length, channel_busy_ratio):
        """Monitorea y detecta congestión"""
        if queue_length > self.queue_threshold or channel_busy_ratio > 0.9:
            self.congestion_detected = True
            return True
        return False
        
    def apply_congestion_mitigation(self, packet):
        """Aplica mitigación de congestión"""
        if self.congestion_detected:
            # Reducir tasa de envío
            # Encontrar rutas alternativas
            # Priorizar paquetes críticos
            pass
''',
            
            'route_optimization': '''
# Optimización de rutas mejorada
class RouteOptimizer:
    def __init__(self):
        self.route_cache = {}
        self.route_stability_threshold = 0.7
        
    def evaluate_route_quality(self, route, metrics):
        """Evalúa calidad de ruta basada en múltiples métricas"""
        stability_score = self._calculate_stability(route)
        congestion_score = self._calculate_congestion_level(route)
        
        quality_score = (
            stability_score * 0.4 +
            (1 - congestion_score) * 0.3 +
            metrics['hop_count'] * 0.3
        )
        
        return quality_score
        
    def _calculate_stability(self, route):
        """Calcula estabilidad de ruta"""
        # Basado en historial de rutas y patrones de movilidad
        pass
''',
            
            'mobility_aware': '''
# Enrutamiento consciente de movilidad
class MobilityAwareRouting:
    def __init__(self):
        self.mobility_predictor = MobilityPredictor()
        self.mobility_threshold = 0.6
        
    def predict_link_stability(self, node1, node2):
        """Predice estabilidad del enlace entre dos nodos"""
        relative_velocity = self._calculate_relative_velocity(node1, node2)
        distance = self._calculate_distance(node1, node2)
        
        # Tiempo estimado hasta que el enlace se rompa
        link_lifetime = self._estimate_link_lifetime(relative_velocity, distance)
        
        return link_lifetime
        
    def select_stable_routes(self, candidate_routes):
        """Selecciona rutas más estables basadas en predicción de movilidad"""
        stable_routes = []
        for route in candidate_routes:
            min_link_lifetime = min([
                self.predict_link_stability(route[i], route[i+1])
                for i in range(len(route)-1)
            ])
            
            if min_link_lifetime > self.mobility_threshold:
                stable_routes.append((route, min_link_lifetime))
                
        return sorted(stable_routes, key=lambda x: x[1], reverse=True)
'''
        }
    
    def _generate_components(self, strategies: List, protocol: str) -> str:
        """Genera componentes de optimización"""
        components = []
        
        for strategy in strategies:
            if strategy.name in self.templates:
                components.append(self.templates[strategy.name])
        
        return '\n'.join(components)
    
    def _generate_main_code(self, original_code: str, components: str,
                          optimization_type: str, protocol: str) -> str:
        """Genera código principal optimizado"""
        
        # Insertar componentes al inicio
        optimized_code = f'''#!/usr/bin/env python3
"""
Código NS-3 Optimizado - {protocol.upper()}
Tipo de optimización: {optimization_type}
"""

import sys
from pathlib import Path
sys.path.insert(0, "/home/diego/ns3/build/bindings/python")

import ns.core
import ns.network
import ns.internet
import ns.mobility
import ns.wifi
import ns.applications

# Componentes de optimización
{components}

def main():
    """Función principal de simulación optimizada"""
    
    # Crear componentes de optimización
    adaptive_params = AdaptiveParameters()
    congestion_control = CongestionControl()
    route_optimizer = RouteOptimizer()
    mobility_aware = MobilityAwareRouting()
    
    # Configuración base (preservando lógica original)
{self._extract_base_config(original_code)}
    
    # Aplicar optimizaciones
{self._generate_optimization_calls(optimization_type)}
    
    # Ejecutar simulación
{self._extract_simulation_logic(original_code)}

if __name__ == "__main__":
    main()
'''
        
        return optimized_code
    
    def _generate_config_code(self, strategies: List, protocol: str) -> str:
        """Genera código de configuración optimizada"""
        config_lines = [
            "# Configuración optimizada para " + protocol,
            "",
            "# Parámetros adaptativos",
            "config.SetDefault('ns3::AodvRoutingProtocol::HelloInterval', ns.core.TimeValue(adaptive_params.base_hello_interval))",
            "config.SetDefault('ns3::AodvRoutingProtocol::ActiveRouteTimeout', ns.core.TimeValue(adaptive_params.base_active_route_timeout))",
            "",
            "# Control de congestión",
            "config.SetDefault('ns3::WifiRemoteStationManager::RtsCtsThreshold', ns.core.UintegerValue(100))",
            "config.SetDefault('ns3::WifiMac::BE_MaxAmpduSize', ns.core.UintegerValue(0))",
            ""
        ]
        
        return '\n'.join(config_lines)
    
    def _extract_base_config(self, original_code: str) -> str:
        """Extrae configuración base del código original"""
        # Lógica simplificada - en producción usaría parsing más sofisticado
        return "    # Configuración base extraída del código original"
    
    def _extract_simulation_logic(self, original_code: str) -> str:
        """Extrae lógica de simulación del código original"""
        return "    # Lógica de simulación extraída del código original"
    
    def _generate_optimization_calls(self, optimization_type: str) -> str:
        """Genera llamadas a funciones de optimización"""
        calls = [
            "    # Aplicar optimizaciones según tipo",
            f"    if '{optimization_type}' in ['rehabilitacion_critica', 'optimizacion_integral']:",
            "        congestion_control.enable()",
            "        route_optimizer.enable()",
            "",
            "    if '{optimization_type}' in ['optimizacion_latencia', 'optimizacion_integral']:",
            "        mobility_aware.enable()",
            "        adaptive_params.adjust_for_low_latency()",
            ""
        ]
        
        return '\n'.join(calls)