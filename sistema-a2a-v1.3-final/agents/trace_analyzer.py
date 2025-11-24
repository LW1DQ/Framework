"""
Agente Analizador de Trazas (Trace Analyzer)

Responsable de analizar archivos PCAP generados por NS-3 usando Wireshark/tshark
para extraer información detallada del tráfico de paquetes que no está disponible
directamente en FlowMonitor.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, List, Optional
import subprocess
import json
import pandas as pd
from langchain_ollama import ChatOllama

from config.settings import OLLAMA_BASE_URL, MODEL_REASONING, SIMULATIONS_DIR
from utils.state import AgentState, add_audit_entry


def check_tshark_available() -> bool:
    """
    Verifica si tshark está disponible en el sistema
    
    Returns:
        True si tshark está disponible
    """
    try:
        result = subprocess.run(
            ['tshark', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def analyze_pcap_basic_stats(pcap_file: str) -> Dict:
    """
    Extrae estadísticas básicas del archivo PCAP usando tshark
    
    Args:
        pcap_file: Ruta al archivo PCAP
        
    Returns:
        Diccionario con estadísticas básicas
    """
    try:
        # Comando tshark para estadísticas básicas
        cmd = [
            'tshark',
            '-r', pcap_file,
            '-q',  # Modo silencioso
            '-z', 'io,stat,0'  # Estadísticas de I/O
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            return {'error': result.stderr}
        
        # Parsear salida
        output = result.stdout
        
        # Extraer información básica
        stats = {
            'total_packets': 0,
            'total_bytes': 0,
            'duration': 0.0
        }
        
        # Parsear líneas de estadísticas
        for line in output.split('\n'):
            if 'Packets:' in line:
                try:
                    stats['total_packets'] = int(line.split(':')[1].strip())
                except:
                    pass
            elif 'Bytes:' in line:
                try:
                    stats['total_bytes'] = int(line.split(':')[1].strip())
                except:
                    pass
        
        return stats
        
    except subprocess.TimeoutExpired:
        return {'error': 'Timeout al analizar PCAP'}
    except Exception as e:
        return {'error': str(e)}


def analyze_pcap_protocols(pcap_file: str) -> Dict:
    """
    Analiza distribución de protocolos en el PCAP
    
    Args:
        pcap_file: Ruta al archivo PCAP
        
    Returns:
        Diccionario con distribución de protocolos
    """
    try:
        # Comando para jerarquía de protocolos
        cmd = [
            'tshark',
            '-r', pcap_file,
            '-q',
            '-z', 'io,phs'  # Protocol Hierarchy Statistics
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            return {'error': result.stderr}
        
        # Parsear jerarquía de protocolos
        protocols = {}
        for line in result.stdout.split('\n'):
            # Buscar líneas con protocolos y porcentajes
            if '%' in line and 'frames' in line.lower():
                parts = line.split()
                for i, part in enumerate(parts):
                    if part.endswith('%'):
                        try:
                            protocol = parts[i-1] if i > 0 else 'unknown'
                            percentage = float(part.rstrip('%'))
                            protocols[protocol] = percentage
                        except:
                            pass
        
        return protocols
        
    except subprocess.TimeoutExpired:
        return {'error': 'Timeout al analizar protocolos'}
    except Exception as e:
        return {'error': str(e)}


def analyze_pcap_conversations(pcap_file: str) -> List[Dict]:
    """
    Analiza conversaciones (flujos) en el PCAP
    
    Args:
        pcap_file: Ruta al archivo PCAP
        
    Returns:
        Lista de conversaciones con estadísticas
    """
    try:
        # Comando para conversaciones IP
        cmd = [
            'tshark',
            '-r', pcap_file,
            '-q',
            '-z', 'conv,ip'  # IP conversations
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            return []
        
        # Parsear conversaciones
        conversations = []
        lines = result.stdout.split('\n')
        
        for line in lines:
            # Buscar líneas con formato: IP1 <-> IP2
            if '<->' in line:
                parts = line.split()
                if len(parts) >= 6:
                    try:
                        conv = {
                            'src': parts[0],
                            'dst': parts[2],
                            'packets': int(parts[3]),
                            'bytes': int(parts[4])
                        }
                        conversations.append(conv)
                    except:
                        pass
        
        return conversations
        
    except subprocess.TimeoutExpired:
        return []
    except Exception as e:
        print(f"Error analizando conversaciones: {e}")
        return []


def analyze_pcap_routing_packets(pcap_file: str, protocol: str = 'aodv') -> Dict:
    """
    Analiza paquetes de enrutamiento específicos del protocolo
    
    Args:
        pcap_file: Ruta al archivo PCAP
        protocol: Protocolo de enrutamiento (aodv, olsr, dsdv)
        
    Returns:
        Diccionario con análisis de paquetes de enrutamiento
    """
    try:
        # Filtro según protocolo
        filters = {
            'aodv': 'aodv',
            'olsr': 'olsr',
            'dsdv': 'dsdv'
        }
        
        filter_str = filters.get(protocol.lower(), 'aodv')
        
        # Contar paquetes de enrutamiento
        cmd = [
            'tshark',
            '-r', pcap_file,
            '-Y', filter_str,  # Display filter
            '-T', 'fields',
            '-e', 'frame.number',
            '-e', 'frame.len',
            '-e', f'{filter_str}.type'
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode != 0:
            return {'error': result.stderr}
        
        # Parsear paquetes
        routing_packets = []
        for line in result.stdout.split('\n'):
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 2:
                    try:
                        routing_packets.append({
                            'frame': int(parts[0]),
                            'length': int(parts[1]),
                            'type': parts[2] if len(parts) > 2 else 'unknown'
                        })
                    except:
                        pass
        
        # Calcular estadísticas
        if routing_packets:
            total_routing_packets = len(routing_packets)
            total_routing_bytes = sum(p['length'] for p in routing_packets)
            
            # Contar tipos de mensajes
            message_types = {}
            for p in routing_packets:
                msg_type = p.get('type', 'unknown')
                message_types[msg_type] = message_types.get(msg_type, 0) + 1
            
            return {
                'protocol': protocol,
                'total_routing_packets': total_routing_packets,
                'total_routing_bytes': total_routing_bytes,
                'message_types': message_types,
                'avg_packet_size': total_routing_bytes / total_routing_packets if total_routing_packets > 0 else 0
            }
        else:
            return {
                'protocol': protocol,
                'total_routing_packets': 0,
                'message_types': {}
            }
        
    except subprocess.TimeoutExpired:
        return {'error': 'Timeout al analizar paquetes de enrutamiento'}
    except Exception as e:
        return {'error': str(e)}


def analyze_pcap_retransmissions(pcap_file: str) -> Dict:
    """
    Analiza retransmisiones en el PCAP
    
    Args:
        pcap_file: Ruta al archivo PCAP
        
    Returns:
        Diccionario con análisis de retransmisiones
    """
    try:
        # Buscar retransmisiones TCP
        cmd = [
            'tshark',
            '-r', pcap_file,
            '-Y', 'tcp.analysis.retransmission',
            '-T', 'fields',
            '-e', 'frame.number'
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        retransmissions = len([l for l in result.stdout.split('\n') if l.strip()])
        
        return {
            'tcp_retransmissions': retransmissions
        }
        
    except Exception as e:
        return {'error': str(e)}


def generate_trace_analysis_report(pcap_file: str, protocol: str = 'aodv') -> str:
    """
    Genera un reporte completo del análisis de trazas usando LLM
    
    Args:
        pcap_file: Ruta al archivo PCAP
        protocol: Protocolo de enrutamiento usado
        
    Returns:
        Reporte en texto
    """
    try:
        llm = ChatOllama(
            model=MODEL_REASONING,
            temperature=0.2,
            base_url=OLLAMA_BASE_URL
        )
        
        # Recopilar todos los análisis
        basic_stats = analyze_pcap_basic_stats(pcap_file)
        protocols_dist = analyze_pcap_protocols(pcap_file)
        conversations = analyze_pcap_conversations(pcap_file)
        routing_analysis = analyze_pcap_routing_packets(pcap_file, protocol)
        retrans_analysis = analyze_pcap_retransmissions(pcap_file)
        
        # Preparar contexto para LLM
        context = f"""
**ANÁLISIS DE TRAZAS PCAP**

Archivo: {Path(pcap_file).name}
Protocolo de Enrutamiento: {protocol.upper()}

**ESTADÍSTICAS BÁSICAS:**
- Total de paquetes: {basic_stats.get('total_packets', 0):,}
- Total de bytes: {basic_stats.get('total_bytes', 0):,}
- Duración: {basic_stats.get('duration', 0):.2f}s

**DISTRIBUCIÓN DE PROTOCOLOS:**
{json.dumps(protocols_dist, indent=2)}

**CONVERSACIONES (Top 10):**
{json.dumps(conversations[:10], indent=2)}

**ANÁLISIS DE PAQUETES DE ENRUTAMIENTO:**
{json.dumps(routing_analysis, indent=2)}

**RETRANSMISIONES:**
{json.dumps(retrans_analysis, indent=2)}
"""
        
        prompt = f"""
Eres un experto en análisis de tráfico de redes y protocolos de enrutamiento.

{context}

**ANÁLISIS REQUERIDO:**

1. **Comportamiento del Protocolo de Enrutamiento**:
   - ¿Cuánto overhead genera el protocolo?
   - ¿Qué tipos de mensajes son más frecuentes?
   - ¿Es eficiente el uso del ancho de banda?

2. **Patrones de Tráfico**:
   - ¿Hay conversaciones dominantes?
   - ¿Cómo se distribuye el tráfico entre nodos?
   - ¿Hay indicios de congestión?

3. **Problemas Detectados**:
   - ¿Hay retransmisiones excesivas?
   - ¿Hay pérdida de paquetes evidente?
   - ¿Hay anomalías en el tráfico?

4. **Recomendaciones**:
   - ¿Qué se puede optimizar?
   - ¿Qué parámetros ajustar?

Proporciona un análisis técnico y específico basado en los datos.
"""
        
        response = llm.invoke(prompt)
        
        # Añadir datos crudos al final
        report = response.content
        report += "\n\n" + "="*80
        report += "\n**DATOS CRUDOS DEL ANÁLISIS:**\n"
        report += "="*80 + "\n\n"
        report += context
        
        return report
        
    except Exception as e:
        return f"Error generando reporte: {str(e)}"


def trace_analyzer_node(state: AgentState) -> Dict:
    """
    Nodo del agente analizador de trazas para LangGraph
    
    Args:
        state: Estado actual del sistema
        
    Returns:
        Diccionario con actualizaciones al estado
    """
    print("\n" + "="*80)
    print("📡 AGENTE ANALIZADOR DE TRAZAS ACTIVADO")
    print("="*80)
    
    # Verificar que haya archivos PCAP
    pcap_files = state.get('pcap_files', [])
    
    if not pcap_files:
        print("⚠️  No hay archivos PCAP para analizar")
        return {
            'messages': ['No hay archivos PCAP disponibles para análisis'],
            **add_audit_entry(state, "trace_analyzer", "no_pcap_files", {})
        }
    
    # Verificar que tshark esté disponible
    if not check_tshark_available():
        print("⚠️  tshark no está disponible en el sistema")
        print("   Instalar con: sudo apt install tshark (Linux)")
        print("   O descargar Wireshark desde: https://www.wireshark.org/")
        return {
            'messages': ['tshark no disponible - instalar Wireshark'],
            **add_audit_entry(state, "trace_analyzer", "tshark_not_available", {})
        }
    
    print(f"📊 Analizando {len(pcap_files)} archivo(s) PCAP...")
    print()
    
    # Determinar protocolo de enrutamiento
    task = state.get('task', '').lower()
    protocol = 'aodv'  # Default
    if 'olsr' in task:
        protocol = 'olsr'
    elif 'dsdv' in task:
        protocol = 'dsdv'
    elif 'dsr' in task:
        protocol = 'dsr'
    
    print(f"🔍 Protocolo detectado: {protocol.upper()}")
    print()
    
    all_analyses = []
    
    for pcap_file in pcap_files:
        if not Path(pcap_file).exists():
            print(f"⚠️  Archivo no encontrado: {pcap_file}")
            continue
        
        print(f"📁 Analizando: {Path(pcap_file).name}")
        
        # Análisis básico
        print("  🔍 Estadísticas básicas...")
        basic_stats = analyze_pcap_basic_stats(pcap_file)
        
        if 'error' not in basic_stats:
            print(f"     Paquetes: {basic_stats.get('total_packets', 0):,}")
            print(f"     Bytes: {basic_stats.get('total_bytes', 0):,}")
        
        # Análisis de protocolos
        print("  🔍 Distribución de protocolos...")
        protocols = analyze_pcap_protocols(pcap_file)
        
        if protocols and 'error' not in protocols:
            print(f"     Protocolos encontrados: {len(protocols)}")
        
        # Análisis de enrutamiento
        print(f"  🔍 Paquetes de enrutamiento ({protocol.upper()})...")
        routing = analyze_pcap_routing_packets(pcap_file, protocol)
        
        if 'error' not in routing:
            print(f"     Paquetes de enrutamiento: {routing.get('total_routing_packets', 0):,}")
            print(f"     Bytes de enrutamiento: {routing.get('total_routing_bytes', 0):,}")
        
        # Análisis de conversaciones
        print("  🔍 Conversaciones...")
        conversations = analyze_pcap_conversations(pcap_file)
        print(f"     Conversaciones detectadas: {len(conversations)}")
        
        # Análisis de retransmisiones
        print("  🔍 Retransmisiones...")
        retrans = analyze_pcap_retransmissions(pcap_file)
        print(f"     Retransmisiones TCP: {retrans.get('tcp_retransmissions', 0)}")
        
        # Compilar análisis
        analysis = {
            'pcap_file': pcap_file,
            'basic_stats': basic_stats,
            'protocols': protocols,
            'routing_analysis': routing,
            'conversations_count': len(conversations),
            'top_conversations': conversations[:10],
            'retransmissions': retrans
        }
        
        all_analyses.append(analysis)
        print()
    
    # Generar reporte con LLM
    if all_analyses:
        print("📝 Generando reporte de análisis con LLM...")
        
        # Usar el primer archivo PCAP para el reporte principal
        main_pcap = pcap_files[0]
        report = generate_trace_analysis_report(main_pcap, protocol)
        
        # Guardar reporte
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = SIMULATIONS_DIR / "traces" / f"trace_analysis_{timestamp}.md"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# Análisis de Trazas PCAP\n\n")
            f.write(f"**Fecha:** {timestamp}\n")
            f.write(f"**Protocolo:** {protocol.upper()}\n")
            f.write(f"**Archivos analizados:** {len(pcap_files)}\n\n")
            f.write(report)
        
        print(f"✅ Reporte guardado en: {report_file.name}")
    
    print(f"\n{'='*80}")
    print(f"✅ ANÁLISIS DE TRAZAS COMPLETADO")
    print(f"{'='*80}")
    print(f"Archivos analizados: {len(all_analyses)}")
    print(f"Protocolo: {protocol.upper()}")
    print(f"{'='*80}")
    
    return {
        'trace_analysis': all_analyses,
        'trace_analysis_report': report if all_analyses else None,
        'trace_report_file': str(report_file) if all_analyses else None,
        'messages': [f'Análisis de trazas completado: {len(all_analyses)} archivo(s)'],
        **add_audit_entry(state, "trace_analyzer", "analysis_completed", {
            'files_analyzed': len(all_analyses),
            'protocol': protocol,
            'report_file': str(report_file) if all_analyses else None
        })
    }


if __name__ == "__main__":
    # Prueba del agente
    from utils.state import create_initial_state
    
    print("Agente Analizador de Trazas - Prueba")
    print()
    
    # Verificar tshark
    if check_tshark_available():
        print("✅ tshark está disponible")
    else:
        print("❌ tshark NO está disponible")
        print("   Instalar Wireshark para habilitar análisis de trazas")
