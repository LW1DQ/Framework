import yaml
from pathlib import Path
from typing import Dict, Any

# Ruta al archivo de prompts
PROMPTS_FILE = Path(__file__).parent.parent / "config" / "prompts.yaml"

_prompts_cache = None

def load_prompts() -> Dict[str, Any]:
    """
    Carga los prompts desde el archivo YAML.
    Usa caché para evitar lecturas repetidas.
    """
    global _prompts_cache
    if _prompts_cache is None:
        if not PROMPTS_FILE.exists():
            raise FileNotFoundError(f"No se encontró el archivo de prompts: {PROMPTS_FILE}")
        
        with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
            _prompts_cache = yaml.safe_load(f)
            
    return _prompts_cache

def get_prompt(agent: str, key: str, **kwargs) -> str:
    """
    Obtiene un prompt específico y formatea sus placeholders.
    
    Args:
        agent: Nombre del agente (coder, researcher, etc.)
        key: Clave del prompt (briefing, generation, etc.)
        **kwargs: Variables para formatear el prompt
        
    Returns:
        Prompt formateado
    """
    prompts = load_prompts()
    
    if agent not in prompts:
        raise KeyError(f"Agente '{agent}' no encontrado en prompts.yaml")
        
    if key not in prompts[agent]:
        # Soporte para claves anidadas (ej: error_strategy.compilation)
        if '.' in key:
            parts = key.split('.')
            value = prompts[agent]
            for part in parts:
                if part in value:
                    value = value[part]
                else:
                    raise KeyError(f"Clave '{key}' no encontrada para agente '{agent}'")
            return value.format(**kwargs)
        else:
            raise KeyError(f"Clave '{key}' no encontrada para agente '{agent}'")
            
    prompt_template = prompts[agent][key]
    try:
        return prompt_template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Falta variable para formatear prompt '{agent}.{key}': {e}")
