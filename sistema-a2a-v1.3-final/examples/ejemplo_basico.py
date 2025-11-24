#!/usr/bin/env python3
"""
Ejemplo Básico del Sistema A2A

Este ejemplo muestra cómo usar el sistema para una tarea simple.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from supervisor import SupervisorOrchestrator


def ejemplo_simple():
    """
    Ejemplo 1: Simulación simple con AODV
    """
    print("\n" + "="*80)
    print("EJEMPLO 1: Simulación Simple")
    print("="*80)
    
    # Crear supervisor
    supervisor = SupervisorOrchestrator()
    
    # Definir tarea simple
    task = "Simular protocolo AODV con 10 nodos en área de 300x300m durante 100 segundos"
    
    # Ejecutar
    result = supervisor.run_experiment(
        task=task,
        max_iterations=3
    )
    
    if result:
        print("\n✅ Ejemplo 1 completado")
        return True
    else:
        print("\n❌ Ejemplo 1 falló")
        return False


def ejemplo_comparacion():
    """
    Ejemplo 2: Comparación de protocolos
    """
    print("\n" + "="*80)
    print("EJEMPLO 2: Comparación de Protocolos")
    print("="*80)
    
    supervisor = SupervisorOrchestrator()
    
    task = """
    Comparar los protocolos AODV y OLSR en una red de 30 nodos.
    Configuración:
    - Área: 500x500 metros
    - Duración: 200 segundos
    - Movilidad: Random Waypoint
    - Métricas: PDR, latencia, throughput
    """
    
    result = supervisor.run_experiment(
        task=task,
        max_iterations=5
    )
    
    if result:
        print("\n✅ Ejemplo 2 completado")
        print("\nMétricas obtenidas:")
        if result.get('metrics'):
            for key, value in result['metrics'].items():
                print(f"  {key}: {value}")
        return True
    else:
        print("\n❌ Ejemplo 2 falló")
        return False


def main():
    """Ejecuta los ejemplos"""
    print("\n" + "="*80)
    print("EJEMPLOS DEL SISTEMA A2A")
    print("="*80)
    print("\nEstos ejemplos demuestran el uso básico del sistema.")
    print("Cada ejemplo puede tardar varios minutos en completarse.\n")
    
    # Preguntar qué ejemplo ejecutar
    print("Ejemplos disponibles:")
    print("  1. Simulación simple (rápido, ~5 minutos)")
    print("  2. Comparación de protocolos (completo, ~10-15 minutos)")
    print("  3. Ambos")
    
    try:
        choice = input("\nSelecciona un ejemplo (1-3): ").strip()
        
        if choice == "1":
            ejemplo_simple()
        elif choice == "2":
            ejemplo_comparacion()
        elif choice == "3":
            ejemplo_simple()
            ejemplo_comparacion()
        else:
            print("Opción inválida")
            return 1
        
        print("\n" + "="*80)
        print("EJEMPLOS COMPLETADOS")
        print("="*80)
        print("\nRevisa los resultados en:")
        print("  - simulations/results/")
        print("  - simulations/plots/")
        print("  - logs/")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nEjemplos cancelados")
        return 1


if __name__ == "__main__":
    sys.exit(main())
