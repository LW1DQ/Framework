"""
Supervisor - Orquestador Principal del Sistema A2A

Gestiona el flujo de trabajo entre todos los agentes usando LangGraph.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from typing import Literal
import sqlite3
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

from utils.state import AgentState
from agents import (
    research_node,
    coder_node,
    simulator_node,
    analyst_node,
    visualizer_node,
    github_manager_node
)
from config.settings import LOGS_DIR


class SupervisorOrchestrator:
    """
    Orquestador central del sistema multi-agente A2A
    """
    
    def __init__(self):
        """Inicializa el orquestador"""
        # Crear grafo de estados
        self.workflow = StateGraph(AgentState)
        
        # Añadir nodos (agentes)
        self.workflow.add_node("researcher", research_node)
        self.workflow.add_node("coder", coder_node)
        self.workflow.add_node("simulator", simulator_node)
        self.workflow.add_node("analyst", analyst_node)
        self.workflow.add_node("visualizer", visualizer_node)
        self.workflow.add_node("github_manager", github_manager_node)
        
        # Definir flujo de trabajo
        self._define_workflow()
        
        # Configurar persistencia (bitácora automática)
        db_path = LOGS_DIR / "langgraph_checkpoints.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        memory = SqliteSaver(
            sqlite3.connect(str(db_path), check_same_thread=False)
        )
        
        # Compilar grafo
        self.app = self.workflow.compile(checkpointer=memory)
    
    def _define_workflow(self):
        """Define el flujo de trabajo entre agentes"""
        
        # Punto de entrada: Investigador
        self.workflow.set_entry_point("researcher")
        
        # Flujo: Investigador → Programador
        self.workflow.add_edge("researcher", "coder")
        
        # Lógica condicional: ¿El código es válido?
        self.workflow.add_conditional_edges(
            "coder",
            self._should_retry_code,
            {
                "simulator": "simulator",
                "retry": "coder",
                "end": END
            }
        )
        
        # Lógica condicional: ¿La simulación fue exitosa?
        self.workflow.add_conditional_edges(
            "simulator",
            self._should_retry_simulation,
            {
                "analyst": "analyst",
                "retry_code": "coder",
                "end": END
            }
        )
        
        # Análisis → Visualización
        self.workflow.add_edge("analyst", "visualizer")
        
        # Visualización → GitHub Manager
        self.workflow.add_edge("visualizer", "github_manager")
        
        # GitHub Manager → Fin
        self.workflow.add_edge("github_manager", END)
    
    def _should_retry_code(self, state: AgentState) -> Literal["simulator", "retry", "end"]:
        """
        Decide si reintentar generación de código
        
        Args:
            state: Estado actual
            
        Returns:
            Siguiente nodo a ejecutar
        """
        # Si hay errores y no se excedió límite de iteraciones
        if state.get('errors') and state['iteration_count'] < state['max_iterations']:
            print(f"\n🔄 Reintentando código (iteración {state['iteration_count']}/{state['max_iterations']})")
            return "retry"
        
        # Si código validado
        if state.get('code_validated', False):
            return "simulator"
        
        # Si se excedió límite
        print(f"\n⚠️  Límite de iteraciones alcanzado ({state['max_iterations']})")
        return "end"
    
    def _should_retry_simulation(self, state: AgentState) -> Literal["analyst", "retry_code", "end"]:
        """
        Decide qué hacer después de simulación
        
        Args:
            state: Estado actual
            
        Returns:
            Siguiente nodo a ejecutar
        """
        sim_status = state.get('simulation_status', '')
        
        # Si simulación exitosa
        if sim_status == 'completed':
            return "analyst"
        
        # Si falló y no se excedió límite
        if sim_status == 'failed' and state['iteration_count'] < state['max_iterations']:
            print(f"\n🔄 Reintentando desde código (iteración {state['iteration_count']}/{state['max_iterations']})")
            return "retry_code"
        
        # Si se excedió límite
        print(f"\n⚠️  Límite de iteraciones alcanzado ({state['max_iterations']})")
        return "end"
    
    def run_experiment(self, task: str, thread_id: str = None, max_iterations: int = 5):
        """
        Ejecuta un experimento completo
        
        Args:
            task: Descripción de la tarea de investigación
            thread_id: ID del thread (para continuar experimentos)
            max_iterations: Número máximo de iteraciones
            
        Returns:
            Estado final del experimento
        """
        from uuid import uuid4
        from utils.state import create_initial_state
        
        if thread_id is None:
            thread_id = str(uuid4())
        
        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }
        
        # Estado inicial
        initial_state = create_initial_state(task, max_iterations)
        
        print("\n" + "="*80)
        print("🚀 INICIANDO EXPERIMENTO A2A")
        print("="*80)
        print(f"📋 Tarea: {task}")
        print(f"🆔 Thread ID: {thread_id}")
        print(f"🔄 Max iteraciones: {max_iterations}")
        print("="*80)
        
        # Ejecutar workflow
        try:
            for event in self.app.stream(initial_state, config=config):
                for node_name, node_output in event.items():
                    print(f"\n✓ Nodo completado: {node_name}")
                    
                    # Mostrar errores si existen
                    if 'errors' in node_output and node_output['errors']:
                        print(f"  ⚠️  Errores: {node_output['errors'][-1][:100]}...")
            
            # Obtener estado final
            final_state = self.app.get_state(config)
            
            print("\n" + "="*80)
            print("🎉 EXPERIMENTO COMPLETADO")
            print("="*80)
            
            # Resumen de resultados
            if final_state.values.get('metrics'):
                print("\n📊 MÉTRICAS FINALES:")
                for key, value in final_state.values['metrics'].items():
                    print(f"   {key}: {value}")
            
            if final_state.values.get('plots_generated'):
                print(f"\n📈 Gráficos generados: {len(final_state.values['plots_generated'])}")
                for plot in final_state.values['plots_generated']:
                    print(f"   📊 {Path(plot).name}")
            
            if final_state.values.get('errors'):
                print(f"\n⚠️  Errores encontrados: {len(final_state.values['errors'])}")
            
            print("\n" + "="*80)
            
            return final_state.values
            
        except Exception as e:
            print(f"\n❌ ERROR EN EXPERIMENTO: {str(e)}")
            import traceback
            traceback.print_exc()
            return None


if __name__ == "__main__":
    # Prueba del supervisor
    supervisor = SupervisorOrchestrator()
    
    result = supervisor.run_experiment(
        task="Simular protocolo AODV con 20 nodos en área de 500x500m",
        max_iterations=3
    )
    
    if result:
        print("\n✅ Prueba del supervisor completada")
    else:
        print("\n❌ Prueba del supervisor falló")
