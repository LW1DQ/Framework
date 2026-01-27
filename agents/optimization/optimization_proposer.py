"""
Generador de Propuestas de Optimización para Protocolos de Red
"""

from typing import Dict, List, Any
from dataclasses import dataclass

from .performance_analyzer import PerformanceAnalyzer


@dataclass
class OptimizationStrategy:
    """Estrategia de optimización específica"""
    name: str
    description: str
    target_metrics: List[str]
    implementation_complexity: str  # 'baja', 'media', 'alta'
    estimated_improvement: str


class OptimizationProposer:
    """
    Genera propuestas de optimización basadas en cuellos de botella detectados
    """
    
    def __init__(self):
        """Inicializa el proponente de optimizaciones"""
        self.strategies = self._initialize_strategies()
    
    def generate_proposal(self, bottlenecks: Dict, protocol: str = "AODV") -> Dict:
        """
        Genera propuesta de optimización completa
        
        Args:
            bottlenecks: Cuellos de botella detectados
            protocol: Protocolo de enrutamiento actual
            
        Returns:
            Diccionario con propuesta estructurada
        """
        critical_issues = bottlenecks['critical']
        moderate_issues = bottlenecks['moderate']
        
        # Determinar tipo de optimización principal
        optimization_type = self._determine_optimization_type(critical_issues + moderate_issues)
        
        # Seleccionar estrategias apropiadas
        selected_strategies = self._select_strategies(critical_issues + moderate_issues)
        
        # Generar propuesta detallada
        proposal = {
            'optimization_type': optimization_type,
            'primary_issues': [issue['metric'] for issue in critical_issues],
            'secondary_issues': [issue['metric'] for issue in moderate_issues],
            'strategies': selected_strategies,
            'implementation_order': self._prioritize_strategies(selected_strategies),
            'expected_improvements': self._estimate_improvements(selected_strategies),
            'complexity_assessment': self._assess_complexity(selected_strategies)
        }
        
        return proposal
    
    def _initialize_strategies(self) -> Dict[str, OptimizationStrategy]:
        """Inicializa catálogo de estrategias de optimización"""
        return {
            'adaptive_parameters': OptimizationStrategy(
                name="Parámetros Adaptativos",
                description="Ajuste dinámico de parámetros del protocolo basado en condiciones de red",
                target_metrics=['PDR', 'Delay', 'Throughput'],
                implementation_complexity='media',
                estimated_improvement='15-25%'
            ),
            'route_optimization': OptimizationStrategy(
                name="Optimización de Rutas",
                description="Mecanismos mejorados de selección y mantenimiento de rutas",
                target_metrics=['PDR', 'Delay'],
                implementation_complexity='alta',
                estimated_improvement='20-35%'
            ),
            'congestion_control': OptimizationStrategy(
                name="Control de Congestión",
                description="Detección y mitigación proactiva de congestión",
                target_metrics=['PDR', 'Throughput', 'Delay'],
                implementation_complexity='media',
                estimated_improvement='25-40%'
            ),
            'mobility_aware': OptimizationStrategy(
                name="Mobility-Aware Routing",
                description="Adaptación basada en patrones de movilidad",
                target_metrics=['PDR', 'Delay'],
                implementation_complexity='alta',
                estimated_improvement='30-45%'
            ),
            'load_balancing': OptimizationStrategy(
                name="Balance de Carga",
                description="Distribución inteligente de tráfico",
                target_metrics=['Throughput', 'Delay'],
                implementation_complexity='media',
                estimated_improvement='20-30%'
            ),
            'energy_efficient': OptimizationStrategy(
                name="Enrutamiento Energéticamente Eficiente",
                description="Optimización del consumo de energía",
                target_metrics=['PDR', 'Throughput'],
                implementation_complexity='alta',
                estimated_improvement='10-20%'
            ),
            'hybrid_approach': OptimizationStrategy(
                name="Enfoque Híbrido",
                description="Combinación de múltiples técnicas",
                target_metrics=['PDR', 'Delay', 'Throughput'],
                implementation_complexity='alta',
                estimated_improvement='35-50%'
            )
        }
    
    def _determine_optimization_type(self, issues: List[Dict]) -> str:
        """Determina el tipo principal de optimización necesaria"""
        if not issues:
            return "mantenimiento"
        
        metrics = [issue['metric'] for issue in issues]
        
        # Prioridades de optimización
        if 'PDR' in metrics and any(issue['value'] < 70 for issue in issues if issue['metric'] == 'PDR'):
            return "rehabilitacion_critica"
        elif 'Delay' in metrics and any(issue['value'] > 150 for issue in issues if issue['metric'] == 'Delay'):
            return "optimizacion_latencia"
        elif 'Throughput' in metrics and any(issue['value'] < 0.5 for issue in issues if issue['metric'] == 'Throughput'):
            return "optimizacion_capacidad"
        elif len(set(metrics)) >= 3:
            return "optimizacion_integral"
        else:
            return "mejora_general"
    
    def _select_strategies(self, issues: List[Dict]) -> List[OptimizationStrategy]:
        """Selecciona estrategias apropiadas basadas en problemas"""
        selected = []
        metrics = [issue['metric'] for issue in issues]
        
        # Lógica de selección
        if 'PDR' in metrics:
            if any(issue['value'] < 70 for issue in issues if issue['metric'] == 'PDR'):
                selected.extend([
                    self.strategies['congestion_control'],
                    self.strategies['route_optimization']
                ])
            else:
                selected.append(self.strategies['adaptive_parameters'])
        
        if 'Delay' in metrics:
            if any(issue['value'] > 150 for issue in issues if issue['metric'] == 'Delay'):
                selected.append(self.strategies['mobility_aware'])
        
        if 'Throughput' in metrics:
            selected.append(self.strategies['load_balancing'])
        
        # Si hay múltiples problemas, considerar enfoque híbrido
        if len(set(metrics)) >= 3:
            selected.append(self.strategies['hybrid_approach'])
        
        # Eliminar duplicados
        return list(set(selected))
    
    def _prioritize_strategies(self, strategies: List[OptimizationStrategy]) -> List[str]:
        """Prioriza estrategias por complejidad e impacto"""
        priority_map = {'baja': 1, 'media': 2, 'alta': 3}
        
        # Ordenar por complejidad (primero las más simples)
        sorted_strategies = sorted(
            strategies,
            key=lambda s: priority_map[s.implementation_complexity]
        )
        
        return [s.name for s in sorted_strategies]
    
    def _estimate_improvements(self, strategies: List[OptimizationStrategy]) -> Dict[str, str]:
        """Estima mejoras esperadas por métrica"""
        improvements = {}
        
        for strategy in strategies:
            for metric in strategy.target_metrics:
                if metric not in improvements:
                    improvements[metric] = strategy.estimated_improvement
        
        return improvements
    
    def _assess_complexity(self, strategies: List[OptimizationStrategy]) -> str:
        """Evalúa complejidad general de implementación"""
        if not strategies:
            return "baja"
        
        complexity_scores = []
        for strategy in strategies:
            if strategy.implementation_complexity == 'baja':
                complexity_scores.append(1)
            elif strategy.implementation_complexity == 'media':
                complexity_scores.append(2)
            else:
                complexity_scores.append(3)
        
        avg_complexity = sum(complexity_scores) / len(complexity_scores)
        
        if avg_complexity <= 1.5:
            return "baja"
        elif avg_complexity <= 2.5:
            return "media"
        else:
            return "alta"