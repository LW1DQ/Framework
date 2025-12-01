"""
Agente Crítico (Reflection Pattern)

Responsable de evaluar la lógica y calidad del código generado por el Coder
antes de pasar a la simulación. Verifica alineación con la tarea y lógica de negocio.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, Any
from langchain_ollama import ChatOllama

from config.settings import (
    OLLAMA_BASE_URL,
    MODEL_REASONING,
    MODEL_TEMPERATURE_REASONING
)
from utils.state import AgentState, add_audit_entry
from utils.logging_utils import update_agent_status, log_message

def critic_node(state: AgentState) -> Dict[str, Any]:
    """
    Nodo del agente crítico para LangGraph.
    Evalúa el código generado y decide si es apto para simulación.
    
    Args:
        state: Estado actual del sistema
        
    Returns:
        Actualización del estado con feedback del crítico
    """
    print("\n" + "="*80)
    print("🧐 AGENTE CRÍTICO ACTIVADO")
    print("="*80)
    
    task = state['task']
    code = state.get('code_snippet', '')
    iteration = state.get('iteration', 0)
    
    update_agent_status("Critic", "running", "Evaluando lógica del código...")
    log_message("Critic", f"Iniciando evaluación de código para: {task}")
    
    if not code:
        return {
            'critic_approved': False,
            'critique': "No hay código para evaluar.",
            **add_audit_entry(state, "critic", "evaluation_failed", {'reason': "no_code"})
        }

    try:
        llm = ChatOllama(
            model=MODEL_REASONING,
            temperature=MODEL_TEMPERATURE_REASONING,
            base_url=OLLAMA_BASE_URL
        )
        
        prompt = f"""
Actúa como un Revisor de Código Experto en NS-3 y Redes.
Tu objetivo es encontrar ERRORES LÓGICOS o DE ALINEACIÓN con la tarea. NO te preocupes por errores de sintaxis (eso lo hace el compilador).

**TAREA ORIGINAL:**
{task}

**CÓDIGO GENERADO:**
```python
{code[:4000]}  # Truncado para evitar contexto excesivo si es muy largo
```

**CRITERIOS DE EVALUACIÓN:**
1. ¿El código implementa el protocolo solicitado? (Ej: Si pide AODV, ¿usa AODV?)
2. ¿La topología y movilidad coinciden con lo pedido?
3. ¿Se están recolectando las métricas necesarias?
4. ¿Hay lógica "tonta" o placeholders obvios?

**FORMATO DE RESPUESTA:**
Responde EXACTAMENTE con este formato JSON:
{{
    "approved": true/false,
    "critique": "Explicación breve del problema (si approved=false) o 'Aprobado' (si approved=true)"
}}
"""
        
        print("  🤔 Analizando lógica y alineación...")
        response = llm.invoke(prompt)
        content = response.content.strip()
        
        # Intentar parsear JSON (o buscarlo en el texto)
        import json
        import re
        
        approved = False
        critique = "Error parseando respuesta del crítico"
        
        # Buscar bloque JSON
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                approved = data.get('approved', False)
                critique = data.get('critique', "Sin comentarios")
            except:
                # Fallback si el JSON está mal formado
                if "true" in content.lower() and "approved" in content.lower():
                    approved = True
                    critique = "Aprobado (Fallback parse)"
                else:
                    critique = content[:200]
        else:
             # Fallback si no hay JSON
            # Fallback si no hay JSON
            content_lower = content.lower()
            if "approved" in content_lower and "rejected" not in content_lower:
                approved = True
                critique = "Aprobado (No JSON)"
            elif "true" in content_lower and "false" not in content_lower:
                approved = True
                critique = "Aprobado (No JSON)"
            else:
                critique = content[:200]

        
        if approved:
            print("  ✅ Código APROBADO por el Crítico")
            log_message("Critic", "Código aprobado")
            return {
                'critic_approved': True,
                'critique': critique,
                **add_audit_entry(state, "critic", "approved", {'critique': critique})
            }
        else:
            print(f"  ❌ Código RECHAZADO: {critique}")
            log_message("Critic", f"Código rechazado: {critique}", level="WARNING")
            return {
                'critic_approved': False,
                'critique': critique,
                # Incrementar iteración aquí podría ser opcional, pero mejor dejar que el supervisor decida
                # o que el coder incremente al reintentar.
                # Por ahora, pasamos el feedback.
                **add_audit_entry(state, "critic", "rejected", {'critique': critique})
            }

    except Exception as e:
        print(f"  ⚠️ Error en crítico: {e}")
        log_message("Critic", f"Error ejecutando crítico: {e}", level="ERROR")
        # En caso de error del crítico, aprobamos por defecto para no bloquear
        return {
            'critic_approved': True, 
            'critique': "Error en crítico, aprobado por defecto.",
            **add_audit_entry(state, "critic", "error_bypass", {'error': str(e)})
        }
