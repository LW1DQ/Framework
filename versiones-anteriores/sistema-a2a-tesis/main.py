#!/usr/bin/env python3
"""
Sistema Multi-Agente A2A para Tesis Doctoral
Punto de Entrada Principal

Uso:
    python main.py --task "Tu tarea de investigación"
    python main.py --task "Comparar AODV y OLSR" --max-iterations 5
"""

import sys
import argparse
from pathlib import Path

# Añadir directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from supervisor import SupervisorOrchestrator
from rich.console import Console
from rich.panel import Panel

console = Console()


def main():
    """Función principal"""
    
    # Parsear argumentos
    parser = argparse.ArgumentParser(
        description='Sistema Multi-Agente A2A para Investigación en Redes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Comparación básica de protocolos
  python main.py --task "Comparar AODV y OLSR en red de 50 nodos"
  
  # Análisis de escalabilidad
  python main.py --task "Evaluar escalabilidad de AODV con 25, 50, 100 nodos"
  
  # Con más iteraciones
  python main.py --task "Simular VANET urbana" --max-iterations 10
  
  # Continuar experimento previo
  python main.py --task "Mi tarea" --thread-id abc-123-def

Para más información, consulta: docs/03-USO-BASICO.md
        """
    )
    
    parser.add_argument(
        '--task',
        type=str,
        required=True,
        help='Descripción de la tarea de investigación'
    )
    
    parser.add_argument(
        '--max-iterations',
        type=int,
        default=5,
        help='Número máximo de iteraciones para corrección de errores (default: 5)'
    )
    
    parser.add_argument(
        '--thread-id',
        type=str,
        default=None,
        help='ID de thread para continuar experimento previo'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Mostrar información detallada'
    )
    
    args = parser.parse_args()
    
    # Mostrar banner
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]🤖 Sistema Multi-Agente A2A[/bold cyan]\n"
        "[dim]Optimización de Protocolos de Enrutamiento[/dim]",
        border_style="cyan"
    ))
    console.print("\n")
    
    # Validar configuración básica
    try:
        from config.settings import validate_configuration
        errors = validate_configuration()
        
        if errors:
            console.print("[bold red]⚠️  ERRORES DE CONFIGURACIÓN:[/bold red]\n")
            for error in errors:
                console.print(f"  [red]✗[/red] {error}")
            console.print("\n[yellow]Ejecuta:[/yellow] python scripts/check_system.py")
            return 1
            
    except Exception as e:
        console.print(f"[red]Error validando configuración: {e}[/red]")
        return 1
    
    # Crear orquestador
    try:
        supervisor = SupervisorOrchestrator()
    except Exception as e:
        console.print(f"[red]Error creando supervisor: {e}[/red]")
        return 1
    
    # Ejecutar experimento
    try:
        result = supervisor.run_experiment(
            task=args.task,
            thread_id=args.thread_id,
            max_iterations=args.max_iterations
        )
        
        if result:
            console.print("\n")
            console.print(Panel.fit(
                "[bold green]✅ EXPERIMENTO COMPLETADO EXITOSAMENTE[/bold green]\n\n"
                "Revisa los resultados en:\n"
                "  [cyan]simulations/results/[/cyan] - Datos de simulación\n"
                "  [cyan]simulations/plots/[/cyan] - Gráficos generados\n"
                "  [cyan]logs/[/cyan] - Logs del sistema",
                border_style="green"
            ))
            return 0
        else:
            console.print("\n")
            console.print(Panel.fit(
                "[bold red]❌ EXPERIMENTO FALLÓ[/bold red]\n\n"
                "Revisa los logs para más detalles:\n"
                "  [cyan]logs/sistema_a2a.log[/cyan]",
                border_style="red"
            ))
            return 1
            
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Experimento cancelado por el usuario[/yellow]")
        return 1
        
    except Exception as e:
        console.print(f"\n[red]❌ Error inesperado: {e}[/red]")
        import traceback
        if args.verbose:
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
