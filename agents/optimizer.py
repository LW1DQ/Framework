"""
Agente Optimizador

Responsable de proponer y generar código optimizado basado en los resultados
de simulaciones previas. Usa técnicas de Deep Learning para mejorar protocolos.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, List
from langchain_ollama import ChatOllama

from config.settings import OLLAMA_BASE_URL, MODEL_REASONING, MODEL_CODING
from utils.state import AgentState, add_audit_entry
from agents.ns3_ai_integration import (
    generate_ns3_ai_code,
    generate_drl_training_code,
    should_use_drl
)


def analyze_performance_bottlenecks(kpis: Dict) -> Dict:
    """
    Analiza KPIs para identificar cuellos de botella específicos
    
    Args:
        kpis: Diccionario de KPIs
        
    Returns:
        Diccionario con análisis de problemas
    """
    bottlenecks = {
        'critical': [],
        'moderate': [],
        'minor': []
    }
    
    # Analizar PDR
    pdr = kpis.get('avg_pdr', 100)
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
    
    # Analizar Delay
    delay = kpis.get('avg_delay', 0)
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
    
    # Analizar Throughput
    throughput = kpis.get('avg_throughput', 0)
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
            'causes': ['Uso ineficiente del canal', 'Overhead'],
            'priority': 2
        })
    
    # Analizar variabilidad
    std_pdr = kpis.get('std_pdr', 0)
    if std_pdr > 20:
        bottlenecks['moderate'].append({
            'metric': 'Variabilidad PDR',
            'value': std_pdr,
            'issue': 'Alta variabilidad en PDR',
            'causes': ['Inestabilidad de rutas', 'Movilidad'],
            'priority': 2
        })
    
    # Analizar tasa de éxito
    success_rate = kpis.get('success_rate', 100)
    if success_rate < 80:
        bottlenecks['critical'].append({
            'metric': 'Success Rate',
            'value': success_rate,
            'issue': 'Muchos flujos fallidos',
            'causes': ['Desconexiones', 'Rutas no encontradas'],
            'priority': 1
        })
    
    return bottlenecks


def propose_dl_architecture(bottlenecks: Dict, task: str) -> str:
    """
    Propone arquitectura de Deep Learning específica para los problemas detectados
    
    Args:
        bottlenecks: Análisis de cuellos de botella
        task: Tarea original
        
    Returns:
        Propuesta de arquitectura
    """
    try:
        llm = ChatOllama(
            model=MODEL_REASONING,
            temperature=0.2,
            base_url=OLLAMA_BASE_URL
        )
        
        # Preparar resumen de problemas
        problems_summary = []
        
        if bottlenecks['critical']:
            problems_summary.append("**PROBLEMAS CRÍTICOS:**")
            for b in bottlenecks['critical']:
                problems_summary.append(f"- {b['metric']}: {b['issue']} (valor: {b['value']:.2f})")
                problems_summary.append(f"  Causas: {', '.join(b['causes'])}")
        
        if bottlenecks['moderate']:
            problems_summary.append("\n**PROBLEMAS MODERADOS:**")
            for b in bottlenecks['moderate']:
                problems_summary.append(f"- {b['metric']}: {b['issue']} (valor: {b['value']:.2f})")
        
        problems_text = "\n".join(problems_summary)
        
        prompt = f"""
Eres un experto en Deep Reinforcement Learning aplicado a redes de telecomunicaciones.

**TAREA ORIGINAL:**
{task}

**ANÁLISIS DE PROBLEMAS DETECTADOS:**
{problems_text}

**OBJETIVO:**
Diseña una arquitectura de Deep Learning ESPECÍFICA para resolver estos problemas.

**PROPUESTA REQUERIDA:**

1. **Tipo de Arquitectura Recomendada**:
   - DQN (Deep Q-Network) - para decisiones discretas de enrutamiento
   - DDPG (Deep Deterministic Policy Gradient) - para control continuo
   - A3C (Asynchronous Advantage Actor-Critic) - para entornos distribuidos
   - GNN (Graph Neural Network) - para topologías dinámicas
   - Transformer - para secuencias temporales
   
   Justifica tu elección basándote en los problemas específicos detectados.

2. **Diseño del Espacio de Estados** (qué observa el agente):
   ```
   Estado = [
       # Información local del nodo
       buffer_occupancy,      # 0-1
       num_neighbors,         # entero
       energy_level,          # 0-1 (si aplica)
       
       # Información de vecinos
       neighbor_distances,    # array de distancias
       neighbor_loads,        # array de cargas
       
       # Métricas históricas
       recent_pdr,           # últimos N paquetes
       recent_delay,         # promedio reciente
       
       # Información de destino
       distance_to_dest,     # distancia euclidiana
       hops_to_dest,         # número de saltos
   ]
   ```
   Dimensionalidad total: X valores

3. **Diseño del Espacio de Acciones** (qué puede decidir):
   ```
   Acciones = {{
       'select_next_hop': [0, 1, 2, ..., N-1],  # ID del vecino
       'adjust_tx_power': [0.1, 0.5, 1.0],      # niveles de potencia
       'set_priority': [0, 1, 2],                # prioridad del paquete
   }}
   ```

4. **Función de Recompensa** (ecuación matemática):
   ```
   R(t) = w1 * PDR_improvement 
        - w2 * normalized_delay 
        - w3 * energy_consumption
        + w4 * throughput_gain
        - w5 * routing_overhead
   
   Donde:
   - w1 = 0.4 (peso para PDR)
   - w2 = 0.3 (peso para delay)
   - w3 = 0.1 (peso para energía)
   - w4 = 0.15 (peso para throughput)
   - w5 = 0.05 (peso para overhead)
   ```
   
   Ajusta los pesos según los problemas detectados.

5. **Arquitectura de Red Neuronal**:
   ```
   Input Layer: [estado_dim]
   Hidden Layer 1: [256 neurons, ReLU]
   Hidden Layer 2: [128 neurons, ReLU]
   Hidden Layer 3: [64 neurons, ReLU]
   Output Layer: [accion_dim, Softmax/Linear]
   ```

6. **Hiperparámetros de Entrenamiento**:
   - Learning rate: 0.001
   - Batch size: 64
   - Replay buffer: 10000
   - Epsilon decay: 0.995
   - Gamma (discount): 0.99
   - Target network update: cada 100 steps

7. **Estrategia de Entrenamiento**:
   - Episodios: 2000-5000
   - Duración por episodio: 100-200s simulados
   - Exploración: ε-greedy con decay
   - Criterio de convergencia: recompensa promedio estable por 100 episodios

8. **Integración con NS-3**:
   - Usar ns3-ai para comunicación Python-C++
   - Frecuencia de decisiones: cada paquete / cada N paquetes
   - Sincronización: síncrona vs asíncrona

**FORMATO:**
Sé extremadamente específico. Incluye valores numéricos concretos.
Prioriza soluciones para los problemas críticos detectados.
"""
        
        response = llm.invoke(prompt)
        return response.content
        
    except Exception as e:
        return f"Error generando propuesta: {str(e)}"


def generate_optimization_code(architecture_proposal: str, baseline_code: str, task: str) -> str:
    """
    Genera código optimizado basado en la propuesta de arquitectura
    
    Args:
        architecture_proposal: Propuesta de arquitectura DL
        baseline_code: Código baseline original
        task: Tarea original
        
    Returns:
        Código optimizado
    """
    try:
        llm = ChatOllama(
            model=MODEL_CODING,
            temperature=0.1,
            base_url=OLLAMA_BASE_URL
        )
        
        prompt = f"""
Eres un experto en NS-3 y Deep Learning. Genera código OPTIMIZADO basado en la propuesta.

**TAREA:**
{task}

**PROPUESTA DE ARQUITECTURA DL:**
{architecture_proposal[:1500]}

**CÓDIGO BASELINE (referencia):**
```python
{baseline_code[:1000]}
```

**OBJETIVO:**
Genera un script NS-3 MEJORADO que implemente optimizaciones basadas en la propuesta.

**OPTIMIZACIONES A IMPLEMENTAR:**

1. **Ajustes de Parámetros del Protocolo**:
   - Ajustar intervalos de HELLO/TC
   - Optimizar tamaños de buffer
   - Ajustar potencia de transmisión

2. **Mejoras en Configuración**:
   - Usar protocolo más adecuado si es necesario
   - Optimizar modelo de movilidad
   - Ajustar parámetros WiFi

3. **Preparación para DL** (comentado, para futura implementación):
   - Puntos de instrumentación para observar estado
   - Puntos de decisión para acciones del agente
   - Logging de métricas para entrenamiento

**ESTRUCTURA DEL CÓDIGO:**
```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'build/lib/python3')

import ns.core
import ns.network
import ns.internet
import ns.wifi
import ns.mobility
import ns.applications
import ns.flow_monitor
# import ns.aodv / ns.olsr según corresponda

def main():
    # Configuración OPTIMIZADA
    # ... parámetros ajustados según análisis
    
    # TODO: Integración futura con DL
    # - Observar: buffer, vecinos, métricas
    # - Decidir: next hop, potencia, prioridad
    # - Recompensar: según función propuesta
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

**IMPORTANTE:**
- Mantén compatibilidad con NS-3 Python bindings
- Incluye comentarios explicando las optimizaciones
- El código debe ser EJECUTABLE inmediatamente
- Las mejoras de DL son preparatorias (comentadas)

Devuelve SOLO el código Python completo.
"""
        
        response = llm.invoke(prompt)
        
        # Extraer código
        import re
        code_pattern = r'```python\n(.*?)\n```'
        matches = re.findall(code_pattern, response.content, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # Si no hay bloques markdown, buscar solo ```
        code_pattern = r'```\n(.*?)\n```'
        matches = re.findall(code_pattern, response.content, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        return response.content.strip()
        
    except Exception as e:
        return f"# Error generando código optimizado: {str(e)}"


def extract_drl_parameters(optimization_proposal: str) -> Dict:
    """
    Extrae parámetros de DRL de la propuesta del optimizer
    
    Args:
        optimization_proposal: Texto de la propuesta
        
    Returns:
        Diccionario con parámetros PPO
    """
    params = {
        'algorithm': 'PPO',
        'learning_rate': 0.0003,
        'gamma': 0.99,
        'eps_clip': 0.2,
        'k_epochs': 4,
        'batch_size': 32,
        'state_dim': 10,
        'action_dim': 5
    }
    
    return params


def optimizer_node(state: AgentState) -> Dict:
    """
    Nodo del agente optimizador para LangGraph
    
    Args:
        state: Estado actual del sistema
        
    Returns:
        Diccionario con actualizaciones al estado
    """
    print("\n" + "="*80)
    print("🚀 AGENTE OPTIMIZADOR ACTIVADO")
    print("="*80)
    
    # Verificar que haya métricas para analizar
    kpis = state.get('metrics', {})
    
    if not kpis:
        print("⚠️  No hay métricas para optimizar")
        return {
            'messages': ['No hay métricas disponibles para optimización'],
            **add_audit_entry(state, "optimizer", "no_metrics", {})
        }
    
    task = state.get('task', '')
    baseline_code = state.get('code_snippet', '')
    
    print(f"📋 Tarea: {task}")
    print(f"📊 Analizando rendimiento actual...")
    print(f"   PDR: {kpis.get('avg_pdr', 0):.2f}%")
    print(f"   Delay: {kpis.get('avg_delay', 0):.2f} ms")
    print(f"   Throughput: {kpis.get('avg_throughput', 0):.3f} Mbps")
    print(f"   Clasificación: {kpis.get('performance_grade', 'N/A')}")
    print()
    
    # Paso 1: Analizar cuellos de botella
    print("🔍 Identificando cuellos de botella...")
    bottlenecks = analyze_performance_bottlenecks(kpis)
    
    critical_count = len(bottlenecks['critical'])
    moderate_count = len(bottlenecks['moderate'])
    
    print(f"   Problemas críticos: {critical_count}")
    print(f"   Problemas moderados: {moderate_count}")
    
    if critical_count > 0:
        print(f"\n   ⚠️  PROBLEMAS CRÍTICOS DETECTADOS:")
        for b in bottlenecks['critical']:
            print(f"      - {b['metric']}: {b['issue']}")
    
    if moderate_count > 0:
        print(f"\n   ℹ️  Problemas moderados:")
        for b in bottlenecks['moderate']:
            print(f"      - {b['metric']}: {b['issue']}")
    
    # Si no hay problemas significativos, no optimizar
    if critical_count == 0 and moderate_count == 0:
        print("\n✅ Rendimiento óptimo. No se requieren optimizaciones.")
        return {
            'optimization_proposal': 'Rendimiento óptimo - no se requieren cambios',
            'optimized_code': baseline_code,
            'messages': ['Rendimiento óptimo alcanzado'],
            **add_audit_entry(state, "optimizer", "optimal_performance", {
                'kpis': kpis
            })
        }
    
    # Paso 2: Proponer arquitectura DL
    print(f"\n🧠 Diseñando arquitectura de Deep Learning...")
    architecture_proposal = propose_dl_architecture(bottlenecks, task)
    print(f"   ✓ Propuesta generada ({len(architecture_proposal)} caracteres)")
    
    # Paso 3: Determinar si usar DRL
    print(f"\n🤖 Evaluando necesidad de Deep Reinforcement Learning...")
    use_drl = should_use_drl(kpis)
    
    if use_drl:
        print(f"   ✅ DRL recomendado para estos problemas")
        print(f"   📚 Generando código con integración ns3-ai...")
        
        # Extraer parámetros de la propuesta
        drl_params = extract_drl_parameters(architecture_proposal)
        
        # Generar código con ns3-ai
        # Extraer parámetros de la tarea
        import re
        nodes_match = re.search(r'(\d+)\s*nodos', task, re.IGNORECASE)
        area_match = re.search(r'(\d+)x(\d+)', task, re.IGNORECASE)
        protocol_match = re.search(r'(AODV|OLSR|DSDV|DSR)', task, re.IGNORECASE)
        
        nodes = int(nodes_match.group(1)) if nodes_match else 20
        area_size = int(area_match.group(1)) if area_match else 1000
        protocol = protocol_match.group(1) if protocol_match else 'AODV'
        
        optimized_code = generate_ns3_ai_code(protocol, nodes, area_size)
        
        # También generar código de entrenamiento
        training_code = generate_drl_training_code(protocol)
        
        # Guardar código de entrenamiento
        from pathlib import Path
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        training_file = Path("sistema-a2a-tesis/simulations/scripts") / f"train_drl_{timestamp}.py"
        training_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(training_file, 'w', encoding='utf-8') as f:
            f.write(training_code)
        
        print(f"   ✓ Código DRL generado")
        print(f"   ✓ Script de entrenamiento: {training_file.name}")
    else:
        print(f"   ℹ️  DRL no necesario - optimización paramétrica suficiente")
        print(f"\n💻 Generando código optimizado...")
        optimized_code = generate_optimization_code(
            architecture_proposal,
            baseline_code,
            task
        )
        print(f"   ✓ Código optimizado generado ({len(optimized_code)} caracteres)")
    
    # Guardar propuesta y código
    from pathlib import Path
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Guardar propuesta de arquitectura
    proposal_file = Path("sistema-a2a-tesis/simulations/optimizations") / f"proposal_{timestamp}.md"
    proposal_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(proposal_file, 'w', encoding='utf-8') as f:
        f.write(f"# Propuesta de Optimización\n\n")
        f.write(f"**Fecha:** {timestamp}\n")
        f.write(f"**Tarea:** {task}\n\n")
        f.write(f"## Métricas Baseline\n\n")
        f.write(f"- PDR: {kpis.get('avg_pdr', 0):.2f}%\n")
        f.write(f"- Delay: {kpis.get('avg_delay', 0):.2f} ms\n")
        f.write(f"- Throughput: {kpis.get('avg_throughput', 0):.3f} Mbps\n")
        f.write(f"- Clasificación: {kpis.get('performance_grade', 'N/A')}\n\n")
        f.write(f"## Problemas Detectados\n\n")
        
        if bottlenecks['critical']:
            f.write(f"### Críticos\n\n")
            for b in bottlenecks['critical']:
                f.write(f"- **{b['metric']}**: {b['issue']}\n")
                f.write(f"  - Valor: {b['value']:.2f}\n")
                f.write(f"  - Causas: {', '.join(b['causes'])}\n\n")
        
        if bottlenecks['moderate']:
            f.write(f"### Moderados\n\n")
            for b in bottlenecks['moderate']:
                f.write(f"- **{b['metric']}**: {b['issue']}\n\n")
        
        f.write(f"\n## Propuesta de Arquitectura DL\n\n")
        f.write(architecture_proposal)
    
    print(f"   📄 Propuesta guardada en: {proposal_file.name}")
    
    # Guardar código optimizado
    code_file = Path("sistema-a2a-tesis/simulations/scripts") / f"optimized_{timestamp}.py"
    code_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(code_file, 'w', encoding='utf-8') as f:
        f.write(optimized_code)
    
    print(f"   💾 Código guardado en: {code_file.name}")
    
    print(f"\n{'='*80}")
    print(f"✅ OPTIMIZACIÓN COMPLETADA")
    print(f"{'='*80}")
    print(f"Problemas detectados: {critical_count + moderate_count}")
    print(f"Propuesta: {proposal_file.name}")
    print(f"Código optimizado: {code_file.name}")
    print(f"🔄 El código optimizado será regenerado por el Agente Programador")
    print(f"{'='*80}")
    
    # Importar función para incrementar contador
    from utils.state import increment_optimization_count
    
    # Forzar regeneración de código: resetear validación y actualizar notas
    return {
        'optimization_proposal': architecture_proposal,
        'code_snippet': '',  # Resetear para forzar regeneración
        'code_validated': False,  # Forzar nueva validación
        'research_notes': [f"OPTIMIZACIÓN REQUERIDA:\n{architecture_proposal[:500]}..."],  # Añadir contexto
        'bottlenecks': bottlenecks,
        'optimization_files': {
            'proposal': str(proposal_file),
            'code': str(code_file)
        },
        'messages': [
            f'Optimización propuesta: {critical_count} problemas críticos, {moderate_count} moderados',
            'Código será regenerado con optimizaciones aplicadas'
        ],
        **increment_optimization_count(state),
        **add_audit_entry(state, "optimizer", "optimization_completed", {
            'critical_issues': critical_count,
            'moderate_issues': moderate_count,
            'proposal_file': str(proposal_file),
            'code_file': str(code_file),
            'optimization_cycle': state.get('optimization_count', 0) + 1
        })
    }


if __name__ == "__main__":
    # Prueba del agente
    from utils.state import create_initial_state
    
    test_state = create_initial_state("Optimizar AODV con 20 nodos")
    
    # Simular métricas pobres
    test_state['metrics'] = {
        'avg_pdr': 65.5,
        'std_pdr': 15.2,
        'avg_delay': 150.3,
        'avg_throughput': 0.45,
        'success_rate': 70.0,
        'performance_grade': 'Pobre'
    }
    
    test_state['code_snippet'] = "# Código baseline de prueba"
    
    result = optimizer_node(test_state)
    
    print("\n" + "="*80)
    print("RESULTADO DE PRUEBA")
    print("="*80)
    print(f"Propuesta generada: {len(result.get('optimization_proposal', ''))> 0}")
    print(f"Código optimizado: {len(result.get('optimized_code', '')) > 0}")
    print(f"Archivos: {result.get('optimization_files', {})}")
