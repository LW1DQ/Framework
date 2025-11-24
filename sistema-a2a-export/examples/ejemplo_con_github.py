#!/usr/bin/env python3
"""
Ejemplo: Sistema A2A con Gestión de GitHub

Este ejemplo muestra cómo el sistema gestiona automáticamente
el versionado con GitHub durante los experimentos.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from supervisor import SupervisorOrchestrator
from agents.github_manager import GitHubManager
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def ejemplo_con_versionado():
    """
    Ejemplo completo con versionado automático
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]🐙 Ejemplo: Sistema A2A con GitHub Manager[/bold cyan]\n"
        "[dim]Demuestra el versionado automático de experimentos[/dim]",
        border_style="cyan"
    ))
    console.print("\n")
    
    # Verificar si es repositorio git
    manager = GitHubManager()
    
    if not manager.is_git_repo():
        console.print("[yellow]⚠️  No es un repositorio git. Inicializando...[/yellow]\n")
        
        if manager.init_repo():
            console.print("[green]✓ Repositorio inicializado[/green]\n")
        else:
            console.print("[red]✗ Error al inicializar repositorio[/red]")
            return False
    
    # Mostrar estado inicial
    console.print("[bold]📍 Estado Inicial del Repositorio:[/bold]\n")
    
    current_branch = manager.get_current_branch()
    status = manager.get_status()
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Propiedad", style="cyan")
    table.add_column("Valor", style="green")
    
    table.add_row("Rama actual", current_branch or "N/A")
    table.add_row("Archivos modificados", str(len(status['modified'])))
    table.add_row("Archivos nuevos", str(len(status['untracked'])))
    
    console.print(table)
    console.print("\n")
    
    # Ejecutar experimento
    console.print("[bold]🚀 Ejecutando Experimento con Versionado Automático[/bold]\n")
    
    supervisor = SupervisorOrchestrator()
    
    task = """
    Simular protocolo AODV en red MANET con 30 nodos.
    Área: 500x500 metros
    Duración: 150 segundos
    Movilidad: Random Waypoint
    Métricas: PDR, latencia, throughput
    """
    
    console.print(f"[yellow]Tarea:[/yellow] {task.strip()}\n")
    console.print("[dim]El sistema creará automáticamente una rama de prueba...[/dim]\n")
    
    # Ejecutar
    result = supervisor.run_experiment(task, max_iterations=3)
    
    if not result:
        console.print("\n[red]❌ Experimento falló[/red]")
        return False
    
    # Mostrar estado después del experimento
    console.print("\n")
    console.print("[bold]📍 Estado Después del Experimento:[/bold]\n")
    
    # Actualizar estado
    current_branch = manager.get_current_branch()
    commits = manager.get_commit_history(limit=3)
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Propiedad", style="cyan")
    table.add_column("Valor", style="green")
    
    table.add_row("Rama actual", current_branch or "N/A")
    table.add_row("Último commit", commits[0]['message'] if commits else "N/A")
    table.add_row("Commits totales", str(len(commits)))
    
    console.print(table)
    
    # Mostrar últimos commits
    if commits:
        console.print("\n[bold]📜 Últimos Commits:[/bold]\n")
        
        for commit in commits:
            console.print(f"  [cyan]{commit['hash'][:7]}[/cyan] - {commit['message']}")
            console.print(f"    [dim]{commit['author']} - {commit['date']}[/dim]\n")
    
    # Mostrar resultados del experimento
    if result.get('metrics'):
        console.print("\n[bold]📊 Métricas del Experimento:[/bold]\n")
        
        metrics_table = Table(show_header=True, header_style="bold magenta")
        metrics_table.add_column("Métrica", style="cyan")
        metrics_table.add_column("Valor", style="green")
        
        for key, value in result['metrics'].items():
            metrics_table.add_row(key, f"{value:.2f}")
        
        console.print(metrics_table)
    
    # Sugerencias de integración
    if result.get('simulation_status') == 'completed':
        console.print("\n")
        console.print(Panel.fit(
            "[bold green]✅ Experimento Exitoso[/bold green]\n\n"
            "Los cambios están en una rama de prueba.\n\n"
            "[bold]Para integrar a develop:[/bold]\n"
            f"  [cyan]git checkout develop[/cyan]\n"
            f"  [cyan]git merge {current_branch}[/cyan]\n"
            f"  [cyan]git push origin develop[/cyan]\n\n"
            "[bold]O usar el script:[/bold]\n"
            f"  [cyan]python scripts/github_utils.py merge {current_branch} --target develop --push[/cyan]",
            border_style="green"
        ))
    
    console.print("\n[bold green]✓ Ejemplo completado[/bold green]\n")
    
    return True


def ejemplo_gestion_manual():
    """
    Ejemplo de gestión manual con el agente
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]🔧 Ejemplo: Gestión Manual de GitHub[/bold cyan]\n"
        "[dim]Uso directo del GitHubManager[/dim]",
        border_style="cyan"
    ))
    console.print("\n")
    
    manager = GitHubManager()
    
    # 1. Crear rama de desarrollo
    console.print("[bold]1. Creando rama de desarrollo[/bold]\n")
    
    if manager.create_branch("develop", from_branch="main"):
        console.print("[green]✓ Rama 'develop' creada[/green]\n")
    
    # 2. Crear rama de feature
    console.print("[bold]2. Creando rama de feature[/bold]\n")
    
    if manager.create_branch("feature/mejora-analisis"):
        console.print("[green]✓ Rama 'feature/mejora-analisis' creada[/green]\n")
    
    # 3. Ver estado
    console.print("[bold]3. Estado del repositorio[/bold]\n")
    
    status = manager.get_status()
    console.print(f"  Archivos modificados: {len(status['modified'])}")
    console.print(f"  Archivos nuevos: {len(status['untracked'])}\n")
    
    # 4. Hacer commit (si hay cambios)
    if status['modified'] or status['untracked']:
        console.print("[bold]4. Haciendo commit[/bold]\n")
        
        manager.add_files()
        if manager.commit("Mejora en análisis de métricas"):
            console.print("[green]✓ Commit realizado[/green]\n")
    
    # 5. Cambiar a develop
    console.print("[bold]5. Cambiando a develop[/bold]\n")
    
    if manager.switch_branch("develop"):
        console.print("[green]✓ Cambiado a 'develop'[/green]\n")
    
    # 6. Mergear feature
    console.print("[bold]6. Mergeando feature[/bold]\n")
    
    if manager.merge_branch("feature/mejora-analisis"):
        console.print("[green]✓ Merge exitoso[/green]\n")
    
    # 7. Ver historial
    console.print("[bold]7. Historial de commits[/bold]\n")
    
    commits = manager.get_commit_history(limit=5)
    
    for commit in commits:
        console.print(f"  [cyan]{commit['hash'][:7]}[/cyan] - {commit['message']}")
    
    console.print("\n[bold green]✓ Ejemplo de gestión manual completado[/bold green]\n")
    
    return True


def ejemplo_workflow_completo():
    """
    Ejemplo de workflow completo: desarrollo → prueba → integración → release
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]🔄 Ejemplo: Workflow Completo[/bold cyan]\n"
        "[dim]Desarrollo → Prueba → Integración → Release[/dim]",
        border_style="cyan"
    ))
    console.print("\n")
    
    manager = GitHubManager()
    
    # Fase 1: Desarrollo
    console.print("[bold]📝 Fase 1: Desarrollo[/bold]\n")
    
    manager.switch_branch("develop")
    console.print("  ✓ En rama develop")
    
    # Fase 2: Experimento
    console.print("\n[bold]🧪 Fase 2: Experimento[/bold]\n")
    
    console.print("  Ejecutando experimento...")
    console.print("  (El sistema crea rama de prueba automáticamente)")
    
    # Fase 3: Revisión
    console.print("\n[bold]🔍 Fase 3: Revisión[/bold]\n")
    
    commits = manager.get_commit_history(limit=1)
    if commits:
        console.print(f"  Último commit: {commits[0]['message']}")
        console.print("  ✓ Resultados commiteados")
    
    # Fase 4: Integración
    console.print("\n[bold]🔀 Fase 4: Integración[/bold]\n")
    
    console.print("  Si el experimento fue exitoso:")
    console.print("    1. Revisar resultados")
    console.print("    2. Mergear a develop")
    console.print("    3. Pushear cambios")
    
    # Fase 5: Release
    console.print("\n[bold]🏷️  Fase 5: Release[/bold]\n")
    
    console.print("  Cuando tengas resultados estables:")
    console.print("    1. Mergear develop a main")
    console.print("    2. Crear tag (v1.0.0)")
    console.print("    3. Pushear tag")
    
    console.print("\n[bold green]✓ Workflow completo explicado[/bold green]\n")
    
    return True


def main():
    """
    Menú principal
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]🐙 Ejemplos del Agente de GitHub Manager[/bold cyan]",
        border_style="cyan"
    ))
    console.print("\n")
    
    console.print("[bold]Ejemplos disponibles:[/bold]\n")
    console.print("  1. Experimento con versionado automático (10-15 min)")
    console.print("  2. Gestión manual de GitHub (5 min)")
    console.print("  3. Workflow completo explicado (2 min)")
    console.print("  4. Ejecutar todos los ejemplos")
    console.print("  0. Salir")
    
    try:
        choice = input("\nSelecciona un ejemplo (0-4): ").strip()
        
        if choice == "1":
            ejemplo_con_versionado()
        elif choice == "2":
            ejemplo_gestion_manual()
        elif choice == "3":
            ejemplo_workflow_completo()
        elif choice == "4":
            ejemplo_workflow_completo()
            ejemplo_gestion_manual()
            ejemplo_con_versionado()
        elif choice == "0":
            console.print("\n[yellow]Saliendo...[/yellow]\n")
            return 0
        else:
            console.print("\n[red]Opción inválida[/red]\n")
            return 1
        
        console.print("\n")
        console.print(Panel.fit(
            "[bold green]✅ Ejemplos Completados[/bold green]\n\n"
            "Para más información:\n"
            "  [cyan]docs/06-GITHUB-MANAGER.md[/cyan]",
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
