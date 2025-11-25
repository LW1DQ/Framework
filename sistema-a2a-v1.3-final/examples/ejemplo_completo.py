#!/usr/bin/env python3
"""
Ejemplo Completo del Sistema A2A

Este ejemplo muestra el flujo completo con análisis detallado.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from supervisor import SupervisorOrchestrator
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import pandas as pd

console = Console()


def ejemplo_comparacion_completa():
    """
    Ejemplo completo: Comparación de protocolos con análisis detallado
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Ejemplo Completo: Comparación de Protocolos[/bold cyan]\n"
        "[dim]Este ejemplo ejecuta un flujo completo de investigación[/dim]",
        border_style="cyan"
    ))
    console.print("\n")
    
    # Crear supervisor
    supervisor = SupervisorOrchestrator()
    
    # Definir tarea compleja
    task = """
    Comparar los protocolos de enrutamiento AODV y OLSR en una red vehicular (VANET).
    
    Configuración:
    - Número de nodos: 50 vehículos
    - Área de simulación: 1000x1000 metros (escenario urbano)
    - Duración: 300 segundos
    - Modelo de movilidad: Random Waypoint (simula movimiento vehicular)
    - Velocidad de nodos: 10-30 m/s
    
    Métricas a evaluar:
    - PDR (Packet Delivery Ratio)
    - Latencia end-to-end
    - Throughput
    - Overhead de enrutamiento
    
    Objetivo: Determinar cuál protocolo es más adecuado para VANETs urbanas.
    """
    
    console.print("[bold]Tarea definida:[/bold]")
    console.print(task)
    console.print("\n[yellow]Iniciando experimento...[/yellow]\n")
    
    # Ejecutar experimento
    result = supervisor.run_experiment(
        task=task,
        max_iterations=5
    )
    
    if not result:
        console.print("[red]❌ Experimento falló[/red]")
        return False
    
    # Mostrar resultados detallados
    console.print("\n")
    console.print(Panel.fit(
        "[bold green]✅ Experimento Completado[/bold green]",
        border_style="green"
    ))
    
    # Tabla de métricas
    if result.get('metrics'):
        console.print("\n[bold]📊 Métricas Obtenidas:[/bold]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="green")
        table.add_column("Interpretación", style="yellow")
        
        metrics = result['metrics']
        
        # PDR
        pdr = metrics.get('avg_pdr', 0)
        pdr_interp = "Excelente" if pdr > 90 else "Bueno" if pdr > 80 else "Regular" if pdr > 70 else "Malo"
        table.add_row("PDR", f"{pdr:.2f}%", pdr_interp)
        
        # Throughput
        throughput = metrics.get('avg_throughput', 0)
        table.add_row("Throughput", f"{throughput:.2f} Mbps", "")
        
        # Delay
        delay = metrics.get('avg_delay', 0)
        delay_interp = "Excelente" if delay < 50 else "Bueno" if delay < 100 else "Regular" if delay < 200 else "Malo"
        table.add_row("Delay", f"{delay:.2f} ms", delay_interp)
        
        # Flujos
        total = metrics.get('total_flows', 0)
        successful = metrics.get('successful_flows', 0)
        table.add_row("Flujos exitosos", f"{successful}/{total}", "")
        
        console.print(table)
    
    # Mostrar propuesta de optimización
    if result.get('analysis_results', {}).get('proposal'):
        console.print("\n[bold]🧠 Propuesta de Optimización con ML:[/bold]\n")
        proposal = result['analysis_results']['proposal']
        console.print(Panel(proposal[:500] + "...", border_style="blue"))
    
    # Mostrar gráficos generados
    if result.get('plots_generated'):
        console.print("\n[bold]📈 Gráficos Generados:[/bold]\n")
        for plot in result['plots_generated']:
            console.print(f"  📊 {Path(plot).name}")
    
    # Resumen de papers encontrados
    if result.get('papers_found'):
        console.print(f"\n[bold]📚 Papers Encontrados:[/bold] {len(result['papers_found'])}")
        for i, paper in enumerate(result['papers_found'][:3], 1):
            console.print(f"  {i}. {paper.get('title', 'Sin título')[:60]}...")
    
    # Información de bitácora
    if result.get('audit_trail'):
        console.print(f"\n[bold]📝 Acciones Registradas:[/bold] {len(result['audit_trail'])}")
    
    console.print("\n[bold green]✓ Ejemplo completo finalizado[/bold green]\n")
    
    return True


def ejemplo_analisis_escalabilidad():
    """
    Ejemplo: Análisis de escalabilidad con múltiples tamaños de red
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Ejemplo: Análisis de Escalabilidad[/bold cyan]\n"
        "[dim]Evalúa el rendimiento con diferentes tamaños de red[/dim]",
        border_style="cyan"
    ))
    console.print("\n")
    
    supervisor = SupervisorOrchestrator()
    
    # Diferentes tamaños de red
    node_counts = [25, 50, 100]
    results_data = []
    
    for nodes in node_counts:
        console.print(f"\n[yellow]Evaluando con {nodes} nodos...[/yellow]\n")
        
        task = f"""
        Evaluar el protocolo AODV en una red MANET con {nodes} nodos.
        Área: 500x500 metros
        Duración: 200 segundos
        Movilidad: Random Waypoint
        Métricas: PDR, latencia, throughput
        """
        
        result = supervisor.run_experiment(task, max_iterations=3)
        
        if result and result.get('metrics'):
            metrics = result['metrics']
            results_data.append({
                'nodos': nodes,
                'pdr': metrics.get('avg_pdr', 0),
                'throughput': metrics.get('avg_throughput', 0),
                'delay': metrics.get('avg_delay', 0)
            })
            
            console.print(f"[green]✓ Completado con {nodes} nodos[/green]")
        else:
            console.print(f"[red]✗ Falló con {nodes} nodos[/red]")
    
    # Mostrar resultados comparativos
    if results_data:
        console.print("\n[bold]📊 Resultados Comparativos:[/bold]\n")
        
        df = pd.DataFrame(results_data)
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Nodos", style="cyan")
        table.add_column("PDR (%)", style="green")
        table.add_column("Throughput (Mbps)", style="blue")
        table.add_column("Delay (ms)", style="yellow")
        
        for _, row in df.iterrows():
            table.add_row(
                str(row['nodos']),
                f"{row['pdr']:.2f}",
                f"{row['throughput']:.2f}",
                f"{row['delay']:.2f}"
            )
        
        console.print(table)
        
        # Guardar resultados
        output_file = "analisis_escalabilidad.csv"
        df.to_csv(output_file, index=False)
        console.print(f"\n[green]✓ Resultados guardados en: {output_file}[/green]")
        
        # Análisis de tendencias
        console.print("\n[bold]📈 Análisis de Tendencias:[/bold]\n")
        
        if df['pdr'].iloc[-1] < df['pdr'].iloc[0] * 0.8:
            console.print("  ⚠️  PDR degrada significativamente con más nodos")
        else:
            console.print("  ✓ PDR se mantiene estable")
        
        if df['delay'].iloc[-1] > df['delay'].iloc[0] * 1.5:
            console.print("  ⚠️  Delay aumenta considerablemente con más nodos")
        else:
            console.print("  ✓ Delay se mantiene aceptable")
    
    console.print("\n[bold green]✓ Análisis de escalabilidad completado[/bold green]\n")
    
    return True


def ejemplo_investigacion_enfocada():
    """
    Ejemplo: Investigación enfocada en un tema específico
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Ejemplo: Investigación Enfocada[/bold cyan]\n"
        "[dim]Investiga un tema específico sin simulación[/dim]",
        border_style="cyan"
    ))
    console.print("\n")
    
    # Solo ejecutar el agente investigador
    from agents.researcher import research_node
    from utils.state import create_initial_state
    
    task = """
    Investigar técnicas de optimización de enrutamiento usando Graph Neural Networks (GNN)
    para redes vehiculares (VANETs) en ciudades inteligentes.
    
    Enfoque:
    - Papers recientes (2023-2025)
    - Implementaciones en NS-3
    - Métricas de rendimiento reportadas
    - Limitaciones identificadas
    """
    
    console.print("[bold]Tema de investigación:[/bold]")
    console.print(task)
    console.print("\n[yellow]Buscando literatura...[/yellow]\n")
    
    state = create_initial_state(task)
    result = research_node(state)
    
    if result.get('research_notes'):
        console.print("\n[bold]📚 Síntesis de Investigación:[/bold]\n")
        console.print(Panel(result['research_notes'][0], border_style="blue"))
    
    if result.get('papers_found'):
        console.print(f"\n[bold]📄 Papers Encontrados:[/bold] {len(result['papers_found'])}\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Título", style="cyan", width=50)
        table.add_column("Año", style="green")
        table.add_column("Citas", style="yellow")
        
        for paper in result['papers_found'][:5]:
            table.add_row(
                paper.get('title', 'Sin título')[:47] + "...",
                str(paper.get('year', 'N/A')),
                str(paper.get('citations', 0))
            )
        
        console.print(table)
    
    console.print("\n[bold green]✓ Investigación completada[/bold green]\n")
    
    return True


def main():
    """
    Menú principal de ejemplos
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]🎓 Ejemplos Completos del Sistema A2A[/bold cyan]\n"
        "[dim]Demostraciones avanzadas del sistema[/dim]",
        border_style="cyan"
    ))
    console.print("\n")
    
    console.print("[bold]Ejemplos disponibles:[/bold]\n")
    console.print("  1. Comparación completa de protocolos (15-20 min)")
    console.print("  2. Análisis de escalabilidad (30-40 min)")
    console.print("  3. Investigación enfocada (solo literatura, 5 min)")
    console.print("  4. Ejecutar todos los ejemplos")
    console.print("  0. Salir")
    
    try:
        choice = input("\n[bold]Selecciona un ejemplo (0-4):[/bold] ").strip()
        
        if choice == "1":
            ejemplo_comparacion_completa()
        elif choice == "2":
            ejemplo_analisis_escalabilidad()
        elif choice == "3":
            ejemplo_investigacion_enfocada()
        elif choice == "4":
            console.print("\n[yellow]Ejecutando todos los ejemplos...[/yellow]\n")
            ejemplo_investigacion_enfocada()
            ejemplo_comparacion_completa()
            ejemplo_analisis_escalabilidad()
        elif choice == "0":
            console.print("\n[yellow]Saliendo...[/yellow]\n")
            return 0
        else:
            console.print("\n[red]Opción inválida[/red]\n")
            return 1
        
        console.print("\n")
        console.print(Panel.fit(
            "[bold green]✅ Ejemplos Completados[/bold green]\n\n"
            "Revisa los resultados en:\n"
            "  [cyan]simulations/results/[/cyan]\n"
            "  [cyan]simulations/plots/[/cyan]\n"
            "  [cyan]logs/[/cyan]",
            border_style="green"
        ))
        
        return 0
        
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Ejemplos cancelados[/yellow]\n")
        return 1
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
