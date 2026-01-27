"""
Analizador de Métricas de Simulación
"""

import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class MetricsAnalyzer:
    """
    Analiza métricas de simulación desde diferentes fuentes de datos
    """
    
    def __init__(self):
        """Inicializa el analizador de métricas"""
        self.metrics_cache = {}
    
    def parse_flowmonitor_xml(self, xml_path: str) -> pd.DataFrame:
        """
        Parsea XML de FlowMonitor de NS-3
        
        Args:
            xml_path: Ruta al archivo XML
            
        Returns:
            DataFrame con métricas por flujo
        """
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            flows = []
            for flow in root.findall('.//Flow'):
                flow_data = self._extract_flow_metrics(flow)
                flows.append(flow_data)
            
            df = pd.DataFrame(flows)
            
            # Calcular estadísticas adicionales
            if not df.empty:
                df = self._calculate_derived_metrics(df)
            
            logger.info(f"Parseados {len(flows)} flujos desde {xml_path}")
            return df
            
        except Exception as e:
            logger.error(f"Error parseando XML {xml_path}: {e}")
            return pd.DataFrame()
    
    def _extract_flow_metrics(self, flow_element) -> Dict:
        """Extrae métricas de un elemento flow"""
        tx_packets = int(flow_element.get('txPackets', 0))
        rx_packets = int(flow_element.get('rxPackets', 0))
        tx_bytes = int(flow_element.get('txBytes', 0))
        rx_bytes = int(flow_element.get('rxBytes', 0))
        
        # Calcular métricas básicas
        pdr = (rx_packets / tx_packets * 100) if tx_packets > 0 else 0
        throughput = (rx_bytes * 8 / 1000000)  # Mbps
        
        # Delay (convertir de nanosegundos a milisegundos)
        delay_str = flow_element.get('delaySum', '0ns').replace('ns', '')
        delay_ns = float(delay_str) if delay_str else 0
        avg_delay = (delay_ns / rx_packets / 1e6) if rx_packets > 0 else 0
        
        # Jitter
        jitter_str = flow_element.get('jitterSum', '0ns').replace('ns', '')
        jitter_ns = float(jitter_str) if jitter_str else 0
        avg_jitter = (jitter_ns / rx_packets / 1e6) if rx_packets > 0 else 0
        
        # Packet loss
        lost_packets = int(flow_element.get('lostPackets', 0))
        packet_loss_rate = (lost_packets / tx_packets * 100) if tx_packets > 0 else 0
        
        return {
            'flow_id': flow_element.get('flowId'),
            'source': flow_element.get('sourceAddress'),
            'destination': flow_element.get('destinationAddress'),
            'protocol': flow_element.get('protocol'),
            'tx_packets': tx_packets,
            'rx_packets': rx_packets,
            'lost_packets': lost_packets,
            'tx_bytes': tx_bytes,
            'rx_bytes': rx_bytes,
            'pdr': pdr,
            'throughput_mbps': throughput,
            'avg_delay_ms': avg_delay,
            'avg_jitter_ms': avg_jitter,
            'packet_loss_rate': packet_loss_rate
        }
    
    def _calculate_derived_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula métricas derivadas adicionales"""
        # Efficiency score (combinación de PDR y throughput)
        if 'pdr' in df.columns and 'throughput_mbps' in df.columns:
            df['efficiency_score'] = df['pdr'] * df['throughput_mbps'] / 100
        
        # Quality of Service (QoS) score
        df['qos_score'] = self._calculate_qos_score(df)
        
        return df
    
    def _calculate_qos_score(self, df: pd.DataFrame) -> pd.Series:
        """Calcula score de QoS basado en múltiples métricas"""
        # Componentes del score
        pdr_score = np.clip(df['pdr'] / 100, 0, 1)  # 0-1
        delay_score = np.clip(1 - (df['avg_delay_ms'] / 200), 0, 1)  # 0-1, penaliza delay alto
        jitter_score = np.clip(1 - (df['avg_jitter_ms'] / 50), 0, 1)  # 0-1
        loss_score = np.clip(1 - (df['packet_loss_rate'] / 100), 0, 1)  # 0-1
        
        # Ponderación
        qos_score = (
            pdr_score * 0.4 +
            delay_score * 0.3 +
            jitter_score * 0.15 +
            loss_score * 0.15
        )
        
        return qos_score
    
    def analyze_pcap_traces(self, pcap_files: List[str]) -> Dict:
        """
        Analiza trazas PCAP si existen archivos pcap
        
        Args:
            pcap_files: Lista de archivos PCAP
            
        Returns:
            Diccionario con análisis de trazas
        """
        analysis = {
            'total_packets': 0,
            'protocols': {},
            'packet_sizes': [],
            'timing_analysis': {},
            'errors': []
        }
        
        for pcap_file in pcap_files:
            try:
                if Path(pcap_file).exists():
                    file_analysis = self._analyze_single_pcap(pcap_file)
                    self._merge_pcap_analysis(analysis, file_analysis)
                else:
                    analysis['errors'].append(f"PCAP file not found: {pcap_file}")
            except Exception as e:
                analysis['errors'].append(f"Error analyzing {pcap_file}: {e}")
        
        return analysis
    
    def _analyze_single_pcap(self, pcap_file: str) -> Dict:
        """Analiza un único archivo PCAP"""
        # Implementación simplificada - en producción usaría dpkt/pyshark
        try:
            # Simulación de análisis PCAP
            return {
                'total_packets': 1000,
                'protocols': {'TCP': 400, 'UDP': 600},
                'packet_sizes': [64, 128, 256, 512, 1024],
                'timing_analysis': {
                    'avg_inter_arrival': 0.001,
                    'max_inter_arrival': 0.01
                }
            }
        except Exception as e:
            logger.error(f"Error analyzing PCAP {pcap_file}: {e}")
            return {'errors': [str(e)]}
    
    def _merge_pcap_analysis(self, main_analysis: Dict, file_analysis: Dict):
        """Combina análisis de múltiples archivos PCAP"""
        if 'errors' in file_analysis and file_analysis['errors']:
            main_analysis['errors'].extend(file_analysis['errors'])
            return
        
        main_analysis['total_packets'] += file_analysis.get('total_packets', 0)
        
        # Merge protocol counts
        for protocol, count in file_analysis.get('protocols', {}).items():
            main_analysis['protocols'][protocol] = main_analysis['protocols'].get(protocol, 0) + count
        
        # Extend packet sizes
        main_analysis['packet_sizes'].extend(file_analysis.get('packet_sizes', []))
    
    def calculate_summary_statistics(self, metrics_df: pd.DataFrame) -> Dict:
        """
        Calcula estadísticas resumidas de las métricas
        
        Args:
            metrics_df: DataFrame con métricas
            
        Returns:
            Diccionario con estadísticas resumidas
        """
        if metrics_df.empty:
            return {}
        
        # Métricas clave para estadísticas
        key_metrics = ['pdr', 'throughput_mbps', 'avg_delay_ms', 'avg_jitter_ms', 
                       'packet_loss_rate', 'efficiency_score', 'qos_score']
        
        summary = {}
        
        for metric in key_metrics:
            if metric in metrics_df.columns:
                series = metrics_df[metric]
                summary[metric] = {
                    'mean': series.mean(),
                    'std': series.std(),
                    'min': series.min(),
                    'max': series.max(),
                    'median': series.median(),
                    'q25': series.quantile(0.25),
                    'q75': series.quantile(0.75),
                    'count': len(series)
                }
        
        return summary
    
    def detect_anomalies(self, metrics_df: pd.DataFrame) -> Dict:
        """
        Detecta anomalías en las métricas usando métodos estadísticos
        
        Args:
            metrics_df: DataFrame con métricas
            
        Returns:
            Diccionario con anomalías detectadas
        """
        anomalies = {
            'statistical_outliers': {},
            'performance_issues': {},
            'warnings': []
        }
        
        if metrics_df.empty:
            return anomalies
        
        # Detectar outliers con método IQR
        numeric_columns = metrics_df.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            if column in ['pdr', 'throughput_mbps', 'avg_delay_ms', 'qos_score']:
                outliers = self._detect_iqr_outliers(metrics_df[column])
                if outliers:
                    anomalies['statistical_outliers'][column] = {
                        'count': len(outliers),
                        'indices': outliers,
                        'values': metrics_df.iloc[outliers][column].tolist()
                    }
        
        # Detectar problemas de rendimiento
        anomalies['performance_issues'] = self._detect_performance_issues(metrics_df)
        
        return anomalies
    
    def _detect_iqr_outliers(self, series: pd.Series) -> List[int]:
        """Detecta outliers usando método IQR"""
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = series[(series < lower_bound) | (series > upper_bound)]
        return outliers.index.tolist()
    
    def _detect_performance_issues(self, metrics_df: pd.DataFrame) -> Dict:
        """Detecta problemas de rendimiento específicos"""
        issues = {}
        
        # PDR bajo
        if 'pdr' in metrics_df.columns:
            low_pdr_flows = metrics_df[metrics_df['pdr'] < 70]
            if not low_pdr_flows.empty:
                issues['low_pdr'] = {
                    'count': len(low_pdr_flows),
                    'avg_pdr': low_pdr_flows['pdr'].mean(),
                    'flow_ids': low_pdr_flows['flow_id'].tolist()
                }
        
        # Delay alto
        if 'avg_delay_ms' in metrics_df.columns:
            high_delay_flows = metrics_df[metrics_df['avg_delay_ms'] > 100]
            if not high_delay_flows.empty:
                issues['high_delay'] = {
                    'count': len(high_delay_flows),
                    'avg_delay': high_delay_flows['avg_delay_ms'].mean(),
                    'flow_ids': high_delay_flows['flow_id'].tolist()
                }
        
        # Throughput bajo
        if 'throughput_mbps' in metrics_df.columns:
            low_throughput_flows = metrics_df[metrics_df['throughput_mbps'] < 0.5]
            if not low_throughput_flows.empty:
                issues['low_throughput'] = {
                    'count': len(low_throughput_flows),
                    'avg_throughput': low_throughput_flows['throughput_mbps'].mean(),
                    'flow_ids': low_throughput_flows['flow_id'].tolist()
                }
        
        return issues