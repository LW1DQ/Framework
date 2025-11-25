"""
Agente de Escritura Científica Mejorado v2.0
Genera documentos académicos con referencias IEEE y estilo formal
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import json
import yaml
import re

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from config.settings import MODEL_REASONING, OLLAMA_BASE_URL
from utils.logging_utils import log_info, log_error, log_warning
from utils.errors import DocumentGenerationError
from utils.state import AgentState


# Base de datos de referencias IEEE estándar para redes
IEEE_REFERENCES = {
    "aodv": "[1] C. Perkins, E. Belding-Royer, and S. Das, \"Ad hoc On-Demand Distance Vector (AODV) Routing,\" RFC 3561, July 2003.",
    "olsr": "[2] T. Clausen and P. Jacquet, \"Optimized Link State Routing Protocol (OLSR),\" RFC 3626, October 2003.",
    "dsdv": "[3] C. E. Perkins and P. Bhagwat, \"Highly dynamic Destination-Sequenced Distance-Vector routing (DSDV) for mobile computers,\" ACM SIGCOMM Computer Communication Review, vol. 24, no. 4, pp. 234-244, 1994.",
    "ns3": "[4] G. F. Riley and T. R. Henderson, \"The ns-3 Network Simulator,\" in Modeling and Tools for Network Simulation, K. Wehrle, M. Güneş, and J. Gross, Eds. Berlin, Germany: Springer, 2010, pp. 15-34.",
    "manet": "[5] S. Corson and J. Macker, \"Mobile Ad hoc Networking (MANET): Routing Protocol Performance Issues and Evaluation Considerations,\" RFC 2501, January 1999.",
    "randomwaypoint": "[6] D. B. Johnson and D. A. Maltz, \"Dynamic Source Routing in Ad Hoc Wireless Networks,\" in Mobile Computing, T. Imielinski and H. Korth, Eds. Boston, MA: Kluwer Academic Publishers, 1996, pp. 153-181.",
    "pdr": "[7] J. Broch, D. A. Maltz, D. B. Johnson, Y.-C. Hu, and J. Jetcheva, \"A performance comparison of multi-hop wireless ad hoc network routing protocols,\" in Proc. 4th Annual ACM/IEEE Int. Conf. Mobile Computing and Networking (MobiCom), Dallas, TX, USA, Oct. 1998, pp. 85-97.",
    "throughput": "[8] IEEE Standard for Information technology--Telecommunications and information exchange between systems Local and metropolitan area networks--Specific requirements - Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications, IEEE Std 802.11-2020, Feb. 2021.",
    "qos": "[9] S. Chen and K. Nahrstedt, \"Distributed quality-of-service routing in ad hoc networks,\" IEEE J. Sel. Areas Commun., vol. 17, no. 8, pp. 1488-1505, Aug. 1999.",
    "mobility": "[10] T. Camp, J. Boleng, and V. Davies, \"A survey of mobility models for ad hoc network research,\" Wireless Communications and Mobile Computing, vol. 2, no. 5, pp. 483-502, 2002.",
    "drl": "[11] V. Mnih et al., \"Human-level control through deep reinforcement learning,\" Nature, vol. 518, no. 7540, pp. 529-533, Feb. 2015.",
    "actor_critic": "[12] V. R. Konda and J. N. Tsitsiklis, \"Actor-Critic Algorithms,\" in Advances in Neural Information Processing Systems 12, S. A. Solla, T. K. Leen, and K. Müller, Eds. Cambridge, MA: MIT Press, 2000, pp. 1008-1014.",
    "statistical": "[13] D. C. Montgomery, Design and Analysis of Experiments, 9th ed. Hoboken, NJ: John Wiley & Sons, 2017.",
    "confidence_interval": "[14] G. Casella and R. L. Berger, Statistical Inference, 2nd ed. Pacific Grove, CA: Duxbury Press, 2002."
}

# Inicializar modelo con temperatura más baja para mayor precisión
llm = ChatOllama(
    model=MODEL_REASONING,
    base_url=OLLAMA_BASE_URL,
    temperature=0.2  # Más bajo para escritura académica precisa
)



def get_relevant_references(content: str, results: Dict[str, Any]) -> List[str]:
    """
    Selecciona referencias IEEE relevantes basadas en el contenido y resultados
    """
    references = []
    ref_counter = 1
    
    # Detectar protocolos mencionados
    protocols = results.get("configuration", {}).get("protocols", [])
    if isinstance(protocols, str):
        protocols = [protocols]
    
    for protocol in protocols:
        protocol_lower = protocol.lower()
        if protocol_lower in IEEE_REFERENCES:
            references.append(IEEE_REFERENCES[protocol_lower])
    
    # Siempre incluir NS-3
    if "ns3" in IEEE_REFERENCES and IEEE_REFERENCES["ns3"] not in references:
        references.append(IEEE_REFERENCES["ns3"])
    
    # Incluir MANET si es relevante
    if "manet" in content.lower() or "ad hoc" in content.lower():
        if IEEE_REFERENCES["manet"] not in references:
            references.append(IEEE_REFERENCES["manet"])
    
    # Incluir movilidad si se menciona
    mobility = results.get("configuration", {}).get("mobility", "")
    if "random" in mobility.lower() or "waypoint" in mobility.lower():
        if IEEE_REFERENCES["randomwaypoint"] not in references:
            references.append(IEEE_REFERENCES["randomwaypoint"])
    
    # Incluir métricas mencionadas
    if "pdr" in content.lower() or "delivery" in content.lower():
        if IEEE_REFERENCES["pdr"] not in references:
            references.append(IEEE_REFERENCES["pdr"])
    
    if "throughput" in content.lower():
        if IEEE_REFERENCES["throughput"] not in references:
            references.append(IEEE_REFERENCES["throughput"])
    
    # Incluir DRL si se menciona optimización
    if "reinforcement" in content.lower() or "drl" in content.lower():
        if IEEE_REFERENCES["drl"] not in references:
            references.append(IEEE_REFERENCES["drl"])
        if IEEE_REFERENCES["actor_critic"] not in references:
            references.append(IEEE_REFERENCES["actor_critic"])
    
    # Incluir análisis estadístico
    if "statistical" in content.lower() or "confidence" in content.lower():
        if IEEE_REFERENCES["statistical"] not in references:
            references.append(IEEE_REFERENCES["statistical"])
        if IEEE_REFERENCES["confidence_interval"] not in references:
            references.append(IEEE_REFERENCES["confidence_interval"])
    
    return references


def format_ieee_style(text: str) -> str:
    """
    Aplica formato IEEE al texto
    - Números en formato correcto
    - Unidades con espacio
    - Abreviaturas estándar
    """
    # Formato de porcentajes
    text = re.sub(r'(\d+)%', r'\\SI{\1}{\\percent}', text)
    
    # Formato de unidades
    text = re.sub(r'(\d+\.?\d*)\s*ms', r'\\SI{\1}{\\milli\\second}', text)
    text = re.sub(r'(\d+\.?\d*)\s*Mbps', r'\\SI{\1}{\\mega\\bit\\per\\second}', text)
    text = re.sub(r'(\d+\.?\d*)\s*m', r'\\SI{\1}{\\meter}', text)
    text = re.sub(r'(\d+\.?\d*)\s*s\b', r'\\SI{\1}{\\second}', text)
    
    return text


def create_academic_system_prompt() -> str:
    """
    Crea el prompt del sistema para escritura académica formal
    """
    return """Eres un investigador senior con 20 años de experiencia en redes de computadoras y publicaciones en revistas IEEE de alto impacto (IEEE Transactions on Mobile Computing, IEEE/ACM Transactions on Networking, IEEE INFOCOM).

ESTILO DE ESCRITURA REQUERIDO:
1. Formal y académico, tercera persona, voz pasiva cuando sea apropiado
2. Precisión técnica absoluta
3. Argumentación lógica y estructurada
4. Uso de terminología estándar IEEE
5. Referencias en formato IEEE entre corchetes [X]
6. Evitar lenguaje coloquial o informal
7. Usar conectores académicos: "Furthermore", "Moreover", "However", "Nevertheless"
8. Cuantificar siempre que sea posible
9. Comparar con estado del arte
10. Justificar decisiones metodológicas

FORMATO IEEE:
- Referencias numeradas [1], [2], etc.
- Ecuaciones numeradas si es necesario
- Figuras y tablas referenciadas como "Fig. 1", "Table I"
- Unidades en formato SI
- Abreviaturas definidas en primera mención

ESTRUCTURA:
- Párrafos bien estructurados (topic sentence + desarrollo + conclusión)
- Transiciones claras entre secciones
- Argumentación basada en evidencia
- Conclusiones respaldadas por datos

CALIDAD:
- Nivel de publicación en IEEE Transactions
- Revisión por pares implícita
- Rigor científico máximo
- Reproducibilidad garantizada"""



def generate_experiment_briefing_enhanced(results: Dict[str, Any], state: AgentState) -> str:
    """
    Genera un briefing académico formal con referencias IEEE
    """
    log_info("📝 Generando briefing académico mejorado...")
    
    experiment_name = results.get("experiment_name", "Experimento")
    config = results.get("configuration", {})
    metrics = results.get("metrics", {})
    timestamp = results.get("timestamp", datetime.now().isoformat())
    
    # Construir prompt académico
    prompt = f"""Genera un briefing técnico académico (2 páginas) del siguiente experimento de simulación de redes móviles ad hoc (MANETs):

INFORMACIÓN DEL EXPERIMENTO:
Nombre: {experiment_name}
Fecha: {timestamp}
Configuración: {json.dumps(config, indent=2)}

RESULTADOS OBTENIDOS:
{json.dumps(metrics, indent=2)}

REQUISITOS DEL BRIEFING:

I. RESUMEN EJECUTIVO (100-150 palabras)
   - Contexto y motivación (con referencia a literatura)
   - Objetivo del experimento
   - Metodología empleada (mencionar NS-3 [4])
   - Resultados principales cuantificados
   - Conclusión principal

II. CONFIGURACIÓN EXPERIMENTAL
   A. Entorno de Simulación
      - Simulador: NS-3 versión X.XX [4]
      - Protocolos evaluados: [mencionar con referencias apropiadas]
      - Topología de red: X nodos en área de Y×Z m²
      - Modelo de movilidad: [especificar con referencia]
   
   B. Parámetros de Red
      - Duración de simulación: X segundos
      - Patrón de tráfico: [especificar]
      - Velocidad de nodos: X-Y m/s
      - Número de repeticiones: N (para validez estadística [13])

   C. Métricas de Evaluación
      - Packet Delivery Ratio (PDR) [7]
      - End-to-end delay promedio
      - Throughput de red [8]
      - Routing overhead

III. RESULTADOS Y ANÁLISIS
   A. Rendimiento General
      - Presentar resultados con intervalos de confianza del 95% [14]
      - Comparar con valores reportados en literatura
      - Análisis de significancia estadística
   
   B. Métricas Específicas
      Para cada métrica:
      - Valor medio ± desviación estándar
      - Intervalo de confianza [min, max]
      - Comparación con protocolos baseline
      - Interpretación técnica

IV. OBSERVACIONES CLAVE
   - Hallazgos principales respaldados por datos
   - Anomalías o comportamientos inesperados
   - Implicaciones para diseño de protocolos
   - Limitaciones del estudio actual

V. CONCLUSIONES Y TRABAJO FUTURO
   - Resumen de contribuciones
   - Validación de hipótesis
   - Direcciones futuras de investigación

FORMATO:
- Estilo IEEE formal
- Referencias numeradas [X]
- Tercera persona, voz pasiva cuando apropiado
- Terminología técnica precisa
- Tablas en formato IEEE (Table I, Table II)
- Ecuaciones numeradas si es necesario

REFERENCIAS MÍNIMAS A INCLUIR:
- Protocolos evaluados (RFCs o papers originales)
- NS-3 simulator [4]
- Métricas de evaluación [7], [8]
- Metodología estadística [13], [14]
- Trabajos relacionados relevantes

TONO: Académico formal, nivel de publicación IEEE Transactions."""

    messages = [
        SystemMessage(content=create_academic_system_prompt()),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    content = response.content
    
    # Añadir referencias IEEE al final
    references = get_relevant_references(content, results)
    if references:
        content += "\n\n## REFERENCES\n\n"
        for i, ref in enumerate(references, 1):
            # Renumerar referencias
            content += f"{ref}\n"
    
    return content
