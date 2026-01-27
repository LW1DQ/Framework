"""
Generador de Reportes de Análisis
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Genera reportes detallados del análisis de simulaciones
    """
    
    def __init__(self):
        """Inicializa el generador de reportes"""
        self.templates = self._initialize_templates()
    
    def generate_comprehensive_report(self, 
                                    metrics_summary: Dict,
                                    performance_analysis: Dict,
                                    trace_analysis: Dict,
                                    anomalies: Dict,
                                    simulation_context: Dict) -> Dict:
        """
        Genera un reporte comprensivo del análisis
        
        Args:
            metrics_summary: Resumen de métricas
            performance_analysis: Análisis de rendimiento
            trace_analysis: Análisis de trazas
            anomalies: Anomalías detectadas
            simulation_context: Contexto de la simulación
            
        Returns:
            Reporte completo estructurado
        """
        report = {
            'metadata': self._generate_metadata(simulation_context),
            'executive_summary': self._generate_executive_summary(metrics_summary),
            'performance_analysis': self._generate_performance_section(metrics_summary),
            'network_analysis': self._generate_network_section(trace_analysis),
            'anomaly_detection': self._generate_anomaly_section(anomalies),
            'recommendations': self._generate_recommendations(metrics_summary, anomalies),
            'appendices': self._generate_appendices(metrics_summary, performance_analysis)
        }
        
        return report
    
    def _generate_metadata(self, simulation_context: Dict) -> Dict:
        """Genera metadatos del reporte"""
        return {
            'report_type': 'Simulation Analysis Report',
            'generated_at': datetime.now().isoformat(),
            'simulation_task': simulation_context.get('task', 'Unknown'),
            'simulation_id': simulation_context.get('simulation_id', 'N/A'),
            'analysis_version': '2.0',
            'analysis_duration': simulation_context.get('analysis_duration', 'N/A')
        }
    
    def _generate_executive_summary(self, metrics_summary: Dict) -> Dict:
        """Genera resumen ejecutivo"""
        summary = {
            'overall_performance_grade': self._calculate_overall_grade(metrics_summary),
            'key_findings': [],
            'critical_issues': [],
            'performance_highlights': []
        }
        
        # Analizar métricas clave
        if metrics_summary:
            for metric, stats in metrics_summary.items():
                if metric == 'pdr':
                    avg_pdr = stats.get('mean', 0)
                    if avg_pdr < 70:
                        summary['critical_issues'].append(
                            f"Packet Delivery Ratio bajo: {avg_pdr:.1f}%"
                        )
                    elif avg_pdr > 90:
                        summary['performance_highlights'].append(
                            f"PDR excelente: {avg_pdr:.1f}%"
                        )
                
                elif metric == 'avg_delay_ms':
                    avg_delay = stats.get('mean', 0)
                    if avg_delay > 100:
                        summary['critical_issues'].append(
                            f"Latencia alta: {avg_delay:.1f}ms"
                        )
                    elif avg_delay < 50:
                        summary['performance_highlights'].append(
                            f"Latencia baja: {avg_delay:.1f}ms"
                        )
                
                elif metric == 'throughput_mbps':
                    avg_throughput = stats.get('mean', 0)
                    if avg_throughput < 1.0:
                        summary['critical_issues'].append(
                            f"Throughput bajo: {avg_throughput:.2f}Mbps"
                        )
                    elif avg_throughput > 5.0:
                        summary['performance_highlights'].append(
                            f"Throughput alto: {avg_throughput:.2f}Mbps"
                        )
        
        # Generar hallazgos clave
        summary['key_findings'] = (
            summary['critical_issues'] + summary['performance_highlights']
        )
        
        return summary
    
    def _calculate_overall_grade(self, metrics_summary: Dict) -> str:
        """Calcula calificación general del rendimiento"""
        if not metrics_summary:
            return "N/A"
        
        scores = []
        
        # Evaluar PDR
        if 'pdr' in metrics_summary:
            avg_pdr = metrics_summary['pdr'].get('mean', 0)
            scores.append(min(avg_pdr / 100, 1.0))
        
        # Evaluar Delay
        if 'avg_delay_ms' in metrics_summary:
            avg_delay = metrics_summary['avg_delay_ms'].get('mean', 100)
            scores.append(max(1 - (avg_delay / 200), 0.0))  # 100% si delay=0, 0% si delay>=200ms
        
        # Evaluar Throughput
        if 'throughput_mbps' in metrics_summary:
            avg_throughput = metrics_summary['throughput_mbps'].get('mean', 0)
            scores.append(min(avg_throughput / 5.0, 1.0))  # 100% si throughput>=5Mbps
        
        # Evaluar QoS Score si existe
        if 'qos_score' in metrics_summary:
            avg_qos = metrics_summary['qos_score'].get('mean', 0)
            scores.append(avg_qos)
        
        if not scores:
            return "N/A"
        
        overall_score = sum(scores) / len(scores)
        
        if overall_score >= 0.9:
            return "Excelente"
        elif overall_score >= 0.8:
            return "Bueno"
        elif overall_score >= 0.7:
            return "Aceptable"
        elif overall_score >= 0.6:
            return "Regular"
        elif overall_score >= 0.4:
            return "Pobre"
        else:
            return "Crítico"
    
    def _generate_performance_section(self, metrics_summary: Dict) -> Dict:
        """Genera sección de análisis de rendimiento"""
        section = {
            'metrics_overview': {},
            'detailed_statistics': {},
            'performance_trends': {}
        }
        
        for metric, stats in metrics_summary.items():
            # Formatear para overview
            section['metrics_overview'][metric] = {
                'average': round(stats.get('mean', 0), 3),
                'standard_deviation': round(stats.get('std', 0), 3),
                'range': {
                    'minimum': round(stats.get('min', 0), 3),
                    'maximum': round(stats.get('max', 0), 3)
                },
                'percentiles': {
                    '25th': round(stats.get('q25', 0), 3),
                    'median': round(stats.get('median', 0), 3),
                    '75th': round(stats.get('q75', 0), 3)
                }
            }
            
            # Estadísticas detalladas
            section['detailed_statistics'][metric] = {
                'sample_size': stats.get('count', 0),
                'coefficient_of_variation': self._calculate_cv(stats),
                'distribution_characteristics': self._analyze_distribution(stats)
            }
        
        return section
    
    def _calculate_cv(self, stats: Dict) -> float:
        """Calcula coeficiente de variación"""
        mean = stats.get('mean', 0)
        std = stats.get('std', 0)
        return (std / mean) if mean != 0 else 0
    
    def _analyze_distribution(self, stats: Dict) -> str:
        """Analiza características de la distribución"""
        cv = self._calculate_cv(stats)
        
        if cv < 0.1:
            return "muy_estable"
        elif cv < 0.3:
            return "estable"
        elif cv < 0.5:
            return "moderada"
        else:
            return "alta_variabilidad"
    
    def _generate_network_section(self, trace_analysis: Dict) -> Dict:
        """Genera sección de análisis de red"""
        section = {
            'traffic_analysis': {},
            'protocol_distribution': {},
            'packet_characteristics': {},
            'timing_analysis': {}
        }
        
        if trace_analysis:
            # Análisis de tráfico
            section['traffic_analysis'] = {
                'total_packets': trace_analysis.get('total_packets', 0),
                'communication_patterns': self._analyze_communication_patterns(trace_analysis)
            }
            
            # Distribución de protocolos
            protocols = trace_analysis.get('protocols', {})
            if protocols:
                total = sum(protocols.values())
                section['protocol_distribution'] = {
                    protocol: {
                        'count': count,
                        'percentage': round((count / total) * 100, 2)
                    }
                    for protocol, count in protocols.items()
                }
            
            # Características de paquetes
            packet_sizes = trace_analysis.get('packet_sizes', [])
            if packet_sizes:
                section['packet_characteristics'] = {
                    'size_distribution': self._analyze_packet_sizes(packet_sizes),
                    'average_size': round(sum(packet_sizes) / len(packet_sizes), 2)
                }
            
            # Análisis de timing
            timing = trace_analysis.get('timing_analysis', {})
            if timing:
                section['timing_analysis'] = timing
        
        return section
    
    def _analyze_communication_patterns(self, trace_analysis: Dict) -> str:
        """Analiza patrones de comunicación"""
        total_packets = trace_analysis.get('total_packets', 0)
        
        if total_packets == 0:
            return "sin_tráfico"
        elif total_packets < 100:
            return "tráfico_ligero"
        elif total_packets < 1000:
            return "tráfico_moderado"
        elif total_packets < 10000:
            return "tráfico_pesado"
        else:
            return "tráfico_intenso"
    
    def _analyze_packet_sizes(self, packet_sizes: List) -> Dict:
        """Analiza distribución de tamaños de paquetes"""
        if not packet_sizes:
            return {}
        
        return {
            'minimum': min(packet_sizes),
            'maximum': max(packet_sizes),
            'average': round(sum(packet_sizes) / len(packet_sizes), 2),
            'median': sorted(packet_sizes)[len(packet_sizes) // 2]
        }
    
    def _generate_anomaly_section(self, anomalies: Dict) -> Dict:
        """Genera sección de detección de anomalías"""
        section = {
            'outlier_analysis': {},
            'performance_issues': {},
            'statistical_anomalies': {}
        }
        
        # Análisis de outliers
        outliers = anomalies.get('statistical_outliers', {})
        for metric, outlier_data in outliers.items():
            section['outlier_analysis'][metric] = {
                'outlier_count': outlier_data.get('count', 0),
                'outlier_percentage': round(
                    (outlier_data.get('count', 0) / len(outlier_data.get('values', []))) * 100, 2
                ) if outlier_data.get('values') else 0,
                'severity': self._assess_outlier_severity(outlier_data)
            }
        
        # Problemas de rendimiento
        issues = anomalies.get('performance_issues', {})
        for issue_type, issue_data in issues.items():
            section['performance_issues'][issue_type] = {
                'affected_flows': issue_data.get('count', 0),
                'severity': self._assess_performance_severity(issue_type, issue_data)
            }
        
        return section
    
    def _assess_outlier_severity(self, outlier_data: Dict) -> str:
        """Evalúa severidad de outliers"""
        count = outlier_data.get('count', 0)
        total_values = len(outlier_data.get('values', []))
        
        if total_values == 0:
            return "sin_datos"
        
        percentage = (count / total_values) * 100
        
        if percentage < 5:
            return "baja"
        elif percentage < 15:
            return "moderada"
        else:
            return "alta"
    
    def _assess_performance_severity(self, issue_type: str, issue_data: Dict) -> str:
        """Evalúa severidad de problemas de rendimiento"""
        count = issue_data.get('count', 0)
        
        if issue_type == 'low_pdr':
            return "alta" if count > 5 else "moderada"
        elif issue_type == 'high_delay':
            return "alta" if count > 3 else "moderada"
        elif issue_type == 'low_throughput':
            return "alta" if count > 5 else "moderada"
        else:
            return "desconocida"
    
    def _generate_recommendations(self, metrics_summary: Dict, anomalies: Dict) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        # Recomendaciones basadas en métricas
        if metrics_summary:
            pdr_mean = metrics_summary.get('pdr', {}).get('mean', 0)
            delay_mean = metrics_summary.get('avg_delay_ms', {}).get('mean', 0)
            throughput_mean = metrics_summary.get('throughput_mbps', {}).get('mean', 0)
            
            if pdr_mean < 80:
                recommendations.append(
                    "Implementar control de congestión para mejorar PDR por debajo del 80%"
                )
            
            if delay_mean > 100:
                recommendations.append(
                    "Optimizar rutas y reducir saltos para disminuir latencia alta"
                )
            
            if throughput_mean < 2.0:
                recommendations.append(
                    "Aumentar capacidad del canal o optimizar gestión de ancho de banda"
                )
        
        # Recomendaciones basadas en anomalías
        performance_issues = anomalies.get('performance_issues', {})
        
        if 'low_pdr' in performance_issues:
            recommendations.append(
                "Investigar causas de pérdida de paquetes y aplicar mecanismos de recuperación"
            )
        
        if 'high_delay' in performance_issues:
            recommendations.append(
                "Implementar QoS y priorización de tráfico para reducir latencia"
            )
        
        if not recommendations:
            recommendations.append(
                "Rendimiento general aceptable. Monitorear continuamente para detectar degradaciones."
            )
        
        return recommendations
    
    def _generate_appendices(self, metrics_summary: Dict, performance_analysis: Dict) -> Dict:
        """Genera apéndices del reporte"""
        appendices = {
            'raw_data_summary': {},
            'statistical_tests': {},
            'methodology': {
                'analysis_tools': ['NS-3 FlowMonitor', 'PCAP Analysis', 'Statistical Methods'],
                'metrics_calculated': [
                    'Packet Delivery Ratio (PDR)',
                    'Average Delay',
                    'Throughput',
                    'Jitter',
                    'Packet Loss Rate',
                    'QoS Score'
                ],
                'outlier_detection': 'IQR Method (Interquartile Range)'
            }
        }
        
        # Resumen de datos brutos
        for metric, stats in metrics_summary.items():
            appendices['raw_data_summary'][metric] = {
                'data_points': stats.get('count', 0),
                'completeness': '100%' if stats.get('count', 0) > 0 else '0%'
            }
        
        return appendices
    
    def save_report(self, report: Dict, output_path: str) -> bool:
        """
        Guarda el reporte en formato JSON
        
        Args:
            report: Reporte generado
            output_path: Ruta de salida
            
        Returns:
            True si se guardó exitosamente
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Reporte guardado en: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error guardando reporte: {e}")
            return False
    
    def _initialize_templates(self) -> Dict:
        """Inicializa plantillas para reportes"""
        return {
            'html_template': '''
            <!DOCTYPE html>
            <html>
            <head><title>Simulation Analysis Report</title></head>
            <body>{{content}}</body>
            </html>
            ''',
            'markdown_template': '''
            # Simulation Analysis Report
            
            ## Executive Summary
            {executive_summary}
            
            ## Performance Analysis
            {performance_analysis}
            
            ## Recommendations
            {recommendations}
            '''
        }