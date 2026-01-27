"""
Componentes de Análisis de Rendimiento para el Agente Optimizador
"""

from typing import Dict, List, Tuple


class PerformanceAnalyzer:
    """
    Analiza métricas de rendimiento para identificar cuellos de botella
    """
    
    @staticmethod
    def analyze_bottlenecks(metrics: Dict) -> Dict:
        """
        Identifica cuellos de botella basados en KPIs
        
        Args:
            metrics: Diccionario con métricas de simulación
            
        Returns:
            Diccionario con cuellos de botella clasificados por severidad
        """
        bottlenecks = {
            'critical': [],
            'moderate': [],
            'minor': []
        }
        
        # Analizar PDR
        PerformanceAnalyzer._analyze_pdr(metrics, bottlenecks)
        
        # Analizar Delay
        PerformanceAnalyzer._analyze_delay(metrics, bottlenecks)
        
        # Analizar Throughput
        PerformanceAnalyzer._analyze_throughput(metrics, bottlenecks)
        
        # Analizar Success Rate
        PerformanceAnalyzer._analyze_success_rate(metrics, bottlenecks)
        
        # Analizar Jitter si existe
        PerformanceAnalyzer._analyze_jitter(metrics, bottlenecks)
        
        return bottlenecks
    
    @staticmethod
    def _analyze_pdr(metrics: Dict, bottlenecks: Dict):
        """Analiza Packet Delivery Ratio"""
        pdr = metrics.get('avg_pdr', 100)
        
        if pdr < 70:
            bottlenecks['critical'].append({
                'metric': 'PDR',
                'value': pdr,
                'issue': 'PDR muy bajo - pérdida excesiva de paquetes',
                'causes': [
                    'Congestión de red',
                    'Colisiones frecuentes',
                    'Rutas inestables',
                    'Overhead del protocolo'
                ],
                'priority': 1
            })
        elif pdr < 85:
            bottlenecks['moderate'].append({
                'metric': 'PDR',
                'value': pdr,
                'issue': 'PDR subóptimo',
                'causes': ['Rutas no óptimas', 'Movilidad alta'],
                'priority': 2
            })
        elif pdr < 95:
            bottlenecks['minor'].append({
                'metric': 'PDR',
                'value': pdr,
                'issue': 'PDR podría mejorar',
                'causes': ['Optimización de rutas posible'],
                'priority': 3
            })
    
    @staticmethod
    def _analyze_delay(metrics: Dict, bottlenecks: Dict):
        """Analiza latencia"""
        delay = metrics.get('avg_delay', 0)
        
        if delay > 200:
            bottlenecks['critical'].append({
                'metric': 'Delay',
                'value': delay,
                'issue': 'Latencia excesiva',
                'causes': [
                    'Rutas largas',
                    'Congestión',
                    'Retransmisiones',
                    'Procesamiento lento'
                ],
                'priority': 1
            })
        elif delay > 100:
            bottlenecks['moderate'].append({
                'metric': 'Delay',
                'value': delay,
                'issue': 'Latencia alta',
                'causes': ['Rutas no óptimas', 'Colas largas'],
                'priority': 2
            })
        elif delay > 50:
            bottlenecks['minor'].append({
                'metric': 'Delay',
                'value': delay,
                'issue': 'Latencia moderada',
                'causes': ['Optimización posible'],
                'priority': 3
            })
    
    @staticmethod
    def _analyze_throughput(metrics: Dict, bottlenecks: Dict):
        """Analiza throughput"""
        throughput = metrics.get('avg_throughput', 0)
        
        if throughput < 0.5:
            bottlenecks['critical'].append({
                'metric': 'Throughput',
                'value': throughput,
                'issue': 'Throughput muy bajo',
                'causes': [
                    'Ancho de banda limitado',
                    'Pérdida de paquetes',
                    'Congestión severa'
                ],
                'priority': 1
            })
        elif throughput < 1.0:
            bottlenecks['moderate'].append({
                'metric': 'Throughput',
                'value': throughput,
                'issue': 'Throughput subóptimo',
                'causes': ['Ineficiencia del protocolo'],
                'priority': 2
            })
    
    @staticmethod
    def _analyze_success_rate(metrics: Dict, bottlenecks: Dict):
        """Analiza tasa de éxito"""
        success_rate = metrics.get('success_rate', 100)
        
        if success_rate < 75:
            bottlenecks['critical'].append({
                'metric': 'Success Rate',
                'value': success_rate,
                'issue': 'Tasa de éxito muy baja',
                'causes': ['Fallas en enrutamiento', 'Problemas de conectividad'],
                'priority': 1
            })
        elif success_rate < 85:
            bottlenecks['moderate'].append({
                'metric': 'Success Rate',
                'value': success_rate,
                'issue': 'Tasa de éxito mejorable',
                'causes': ['Estabilidad de rutas'],
                'priority': 2
            })
    
    @staticmethod
    def _analyze_jitter(metrics: Dict, bottlenecks: Dict):
        """Analiza jitter si está disponible"""
        jitter = metrics.get('avg_jitter')
        
        if jitter and jitter > 50:
            bottlenecks['moderate'].append({
                'metric': 'Jitter',
                'value': jitter,
                'issue': 'Variabilidad de retardo alta',
                'causes': ['Inestabilidad en la red'],
                'priority': 2
            })
    
    @staticmethod
    def get_performance_grade(bottlenecks: Dict) -> Tuple[str, float]:
        """
        Calcula calificación general de rendimiento
        
        Args:
            bottlenecks: Diccionario de cuellos de botella
            
        Returns:
            Tuple con (calificación, puntaje_numérico)
        """
        critical_count = len(bottlenecks['critical'])
        moderate_count = len(bottlenecks['moderate'])
        minor_count = len(bottlenecks['minor'])
        
        # Calcular puntaje (máximo 100)
        score = 100
        score -= critical_count * 25  # -25 por cada crítico
        score -= moderate_count * 10  # -10 por cada moderado
        score -= minor_count * 5      # -5 por cada menor
        
        score = max(0, score)  # No negativo
        
        # Asignar calificación
        if score >= 90:
            grade = "Excelente"
        elif score >= 80:
            grade = "Bueno"
        elif score >= 70:
            grade = "Aceptable"
        elif score >= 60:
            grade = "Regular"
        elif score >= 40:
            grade = "Pobre"
        else:
            grade = "Crítico"
        
        return grade, score