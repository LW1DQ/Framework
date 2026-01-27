"""
Agente Optimizador - Versión Refactorizada

Responsable de proponer y generar código optimizado basado en los resultados
de simulaciones previas. Usa técnicas de Deep Learning para mejorar protocolos.

Refactorizado para mejor mantenibilidad y separación de responsabilidades.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, List, Any
from langchain_ollama import ChatOllama

from config.settings import OLLAMA_BASE_URL, MODEL_REASONING, MODEL_CODING
from utils.state import AgentState, add_audit_entry
from utils.logging_utils import update_agent_status, log_message
from agents.optimization import (
    PerformanceAnalyzer,
    OptimizationProposer,
    CodeGenerator
)


class OptimizerAgent:
    """
    Agente optimizador con arquitectura modular
    """
    
    def __init__(self):
        """Inicializa el agente optimizador con sus componentes"""
        self.performance_analyzer = PerformanceAnalyzer()
        self.optimization_proposer = OptimizationProposer()
        self.code_generator = CodeGenerator()
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self) -> ChatOllama:
        """Inicializa el modelo de lenguaje"""
        return ChatOllama(
            model=MODEL_REASONING,
            temperature=MODEL_TEMPERATURE_REASONING or 0.1,
            base_url=OLLAMA_BASE_URL,
            timeout=120
        )
    
    def _extract_protocol_from_code(self, code: str) -> str:
        """Extrae el protocolo del código de simulación"""
        if 'AODV' in code.upper():
            return 'AODV'
        elif 'OLSR' in code.upper():
            return 'OLSR'
        elif 'DSDV' in code.upper():
            return 'DSDV'
        elif 'HWMP' in code.upper():
            return 'HWMP'
        else:
            return 'AODV'  # Default
    
    def _generate_optimization_summary(self, proposal: Dict, bottlenecks: Dict) -> str:
        """Genera resumen de optimización para el usuario"""
        critical_count = len(bottlenecks['critical'])
        moderate_count = len(bottlenecks['moderate'])
        
        summary = f"""
OPTIMIZACIÓN PROPUESTA:

📊 Problemas Detectados:
• Críticos: {critical_count}
• Moderados: {moderate_count}

🎯 Tipo de Optimización: {proposal['optimization_type'].upper()}

📈 Estrategias Seleccionadas:
"""
        
        for i, strategy in enumerate(proposal['strategies'], 1):
            summary += f"{i}. {strategy.name} - {strategy.description}\n"
            summary += f"   Mejora esperada: {strategy.estimated_improvement}\n"
            summary += f"   Complejidad: {strategy.implementation_complexity}\n\n"
        
        summary += f"""
🔍 Mejoras Esperadas:
{chr(10).join([f"• {k}: {v}" for k, v in proposal['expected_improvements'].items()])}

⚙️ Complejidad de Implementación: {proposal['complexity_assessment'].upper()}

📋 Orden de Implementación:
{chr(10).join([f"{i+1}. {step}" for i, step in enumerate(proposal['implementation_order'])])}
"""
        
        return summary


def optimizer_node(state: AgentState) -> AgentState:
    """
    Nodo del optimizador para LangGraph
    
    Args:
        state: Estado actual del sistema
        
    Returns:
        Estado actualizado con propuesta de optimización
    """
    try:
        update_agent_status("Optimizer", "processing", "Analizando rendimiento y proponiendo optimizaciones")
        log_message("Optimizer", "Iniciando análisis de rendimiento")
        
        # Verificar que existan métricas para analizar
        metrics = state.get('metrics', {})
        if not metrics:
            error_msg = "No se encontraron métricas para optimizar"
            log_message("Optimizer", error_msg, level="ERROR")
            return {
                'errors': [error_msg],
                **add_audit_entry(state, "optimizer", "failed", {"error": error_msg})
            }
        
        # Crear instancia del agente
        optimizer = OptimizerAgent()
        
        print(f"\n🔍 ANALIZANDO RENDIMIENTO")
        print(f"{'='*50}")
        
        # 1. Analizar cuellos de botella
        bottlenecks = optimizer.performance_analyzer.analyze_bottlenecks(metrics)
        
        # 2. Calificar rendimiento actual
        grade, score = optimizer.performance_analyzer.get_performance_grade(bottlenecks)
        
        print(f"📊 Calificación Actual: {grade} (Score: {score:.1f}/100)")
        print(f"   Problemas Críticos: {len(bottlenecks['critical'])}")
        print(f"   Problemas Moderados: {len(bottlenecks['moderate'])}")
        print(f"   Problemas Menores: {len(bottlenecks['minor'])}")
        
        # 3. Generar propuesta de optimización
        original_code = state.get('code_snippet', '')
        protocol = optimizer._extract_protocol_from_code(original_code)
        
        proposal = optimizer.optimization_proposer.generate_proposal(bottlenecks, protocol)
        
        print(f"\n🎯 PROPUESTA DE OPTIMIZACIÓN:")
        print(f"   Tipo: {proposal['optimization_type']}")
        print(f"   Estrategias: {len(proposal['strategies'])}")
        print(f"   Complejidad: {proposal['complexity_assessment']}")
        
        # 4. Generar código optimizado
        code_generation = optimizer.code_generator.generate_optimized_code(
            proposal, original_code, protocol
        )
        
        # 5. Guardar archivos de optimización
        from config.settings import SIMULATIONS_DIR
        timestamp = str(int(Path().resolve().name))
        
        # Guardar propuesta
        proposal_file = SIMULATIONS_DIR / f"optimization_proposal_{timestamp}.txt"
        with open(proposal_file, 'w') as f:
            f.write(optimizer._generate_optimization_summary(proposal, bottlenecks))
        
        # Guardar código optimizado
        optimized_code_file = SIMULATIONS_DIR / f"optimized_code_{timestamp}.py"
        with open(optimized_code_file, 'w') as f:
            f.write(code_generation['main_code'])
        
        # Generar resumen con LLM
        llm_prompt = f"""
Analiza esta propuesta de optimización para protocolo {protocol} y genera un resumen ejecutivo:

PROPUESTA:
{optimizer._generate_optimization_summary(proposal, bottlenecks)}

MÉTRICAS ACTUALES:
{metrics}

Genera un resumen conciso destacando:
1. Problemas principales detectados
2. Soluciones propuestas más importantes
3. Impacto esperado en el rendimiento
4. Recomendaciones de implementación
"""
        
        try:
            response = optimizer.llm.invoke(llm_prompt)
            executive_summary = response.content
        except Exception as e:
            log_message("Optimizer", f"Error generando resumen con LLM: {e}", level="WARNING")
            executive_summary = optimizer._generate_optimization_summary(proposal, bottlenecks)
        
        # Mostrar resultados
        critical_count = len(bottlenecks['critical'])
        moderate_count = len(bottlenecks['moderate'])
        
        print(f"\n{'='*80}")
        print(f"✅ OPTIMIZACIÓN COMPLETADA")
        print(f"{'='*80}")
        print(f"Problemas detectados: {critical_count + moderate_count}")
        print(f"Propuesta: {proposal_file.name}")
        print(f"Código optimizado: {optimized_code_file.name}")
        print(f"🔄 El código optimizado será regenerado por el Agente Programador")
        print(f"{'='*80}")
        
        log_message("Optimizer", "Optimización completada exitosamente")
        update_agent_status("Optimizer", "completed", "Optimización finalizada")
        
        # Importar función para incrementar contador
        from utils.state import increment_optimization_count
        
        # Actualizar estado
        return {
            'optimization_proposal': executive_summary,
            'code_snippet': '',  # Resetear para forzar regeneración
            'code_validated': False,  # Forzar nueva validación
            'research_notes': [f"OPTIMIZACIÓN REQUERIDA:\n{executive_summary[:500]}..."],
            'bottlenecks': bottlenecks,
            'performance_grade': grade,
            'performance_score': score,
            'optimization_files': {
                'proposal': str(proposal_file),
                'code': str(optimized_code_file)
            },
            'messages': [
                f'Optimización propuesta: {critical_count} problemas críticos, {moderate_count} moderados',
                f'Tipo de optimización: {proposal["optimization_type"]}',
                'Código será regenerado con optimizaciones aplicadas'
            ],
            **increment_optimization_count(state),
            **add_audit_entry(state, "optimizer", "optimization_completed", {
                'critical_issues': critical_count,
                'moderate_issues': moderate_count,
                'proposal_file': str(proposal_file),
                'code_file': str(optimized_code_file),
                'optimization_type': proposal['optimization_type'],
                'performance_grade': grade,
                'optimization_cycle': state.get('optimization_count', 0) + 1
            })
        }
        
    except Exception as e:
        error_msg = f"Error en optimizador: {str(e)}"
        log_message("Optimizer", error_msg, level="ERROR")
        update_agent_status("Optimizer", "failed", error_msg)
        
        return {
            'errors': [error_msg],
            **add_audit_entry(state, "optimizer", "failed", {"error": error_msg})
        }


if __name__ == "__main__":
    # Prueba del agente refactorizado
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
    
    test_state['code_snippet'] = "# Código baseline de prueba con AODV"
    
    result = optimizer_node(test_state)
    
    print("\n" + "="*80)
    print("RESULTADO DE PRUEBA - OPTIMIZADOR REFACTORIZADO")
    print("="*80)
    print(f"Propuesta generada: {len(result.get('optimization_proposal', '')) > 0}")
    print(f"Performance grade: {result.get('performance_grade', 'N/A')}")
    print(f"Archivos: {result.get('optimization_files', {})}")
    print(f"Bottlenecks: {len(result.get('bottlenecks', {}).get('critical', []))} críticos")
    
    # Verificar componentes modulares
    optimizer = OptimizerAgent()
    print(f"\nComponentes inicializados:")
    print(f"• Performance Analyzer: ✓")
    print(f"• Optimization Proposer: ✓")
    print(f"• Code Generator: ✓")
    print(f"• LLM Client: ✓")