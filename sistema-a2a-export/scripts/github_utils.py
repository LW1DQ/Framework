#!/usr/bin/env python3
"""
Utilidades de GitHub para el Sistema A2A

Script de línea de comandos para gestionar el repositorio.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
from agents.github_manager import GitHubManager
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def cmd_init(args):
    """Inicializa el repositorio"""
    manager = GitHubManager()
    
    if manager.init_repo():
        console.print("[green]✓ Repositorio inicializado[/green]")
        
        if args.remote:
            console.print(f"\n[yellow]Configurando remoto...[/yellow]")
            manager._run_git_command(["remote", "add", "origin", args.remote])
            console.print(f"[green]✓ Remoto añadido: {args.remote}[/green]")
    else:
        console.print("[red]✗ Error al inicializar[/red]")


def cmd_status(args):
    """Muestra el estado del repositorio"""
    manager = GitHubManager()
    
    if not manager.is_git_repo():
        console.print("[red]✗ No es un repositorio git[/red]")
        return
    
    # Rama actual
    current_branch = manager.get_current_branch()
    
    # Estado
    status = manager.get_status()
    
    # Historial
    commits = manager.get_commit_history(limit=5)
    
    # Panel de información
    console.print("\n")
    console.print(Panel.fit(
        f"[bold cyan]Estado del Repositorio[/bold cyan]\n\n"
        f"[yellow]Rama actual:[/yellow] {current_branch}\n"
        f"[yellow]Archivos modificados:[/yellow] {len(status['modified'])}\n"
        f"[yellow]Archivos nuevos:[/yellow] {len(status['untracked'])}\n"
        f"[yellow]Archivos eliminados:[/yellow] {len(status['deleted'])}",
        border_style="cyan"
    ))
    
    # Tabla de archivos modificados
    if status['modified'] or status['untracked']:
        console.print("\n[bold]Cambios pendientes:[/bold]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Estado", style="cyan")
        table.add_column("Archivo", style="white")
        
        for file in status['modified']:
            table.add_row("Modificado", file)
        
        for file in status['untracked']:
            table.add_row("Nuevo", file)
        
        for file in status['deleted']:
            table.add_row("Eliminado", file)
        
        console.print(table)
    
    # Historial de commits
    if commits:
        console.print("\n[bold]Últimos commits:[/bold]\n")
        
        for commit in commits:
            console.print(f"  [cyan]{commit['hash'][:7]}[/cyan] - {commit['message']}")
            console.print(f"    [dim]{commit['author']} - {commit['date']}[/dim]")


def cmd_commit(args):
    """Hace un commit"""
    manager = GitHubManager()
    
    if not manager.is_git_repo():
        console.print("[red]✗ No es un repositorio git[/red]")
        return
    
    # Añadir archivos
    console.print("[yellow]Añadiendo archivos...[/yellow]")
    if not manager.add_files():
        console.print("[red]✗ Error al añadir archivos[/red]")
        return
    
    # Hacer commit
    console.print(f"[yellow]Haciendo commit: {args.message}[/yellow]")
    if manager.commit(args.message, args.description):
        console.print("[green]✓ Commit realizado[/green]")
        
        # Push si se solicita
        if args.push:
            console.print("[yellow]Pusheando a GitHub...[/yellow]")
            if manager.push():
                console.print("[green]✓ Push exitoso[/green]")
            else:
                console.print("[red]✗ Error al pushear[/red]")
    else:
        console.print("[red]✗ Error al hacer commit[/red]")


def cmd_branch(args):
    """Gestiona ramas"""
    manager = GitHubManager()
    
    if not manager.is_git_repo():
        console.print("[red]✗ No es un repositorio git[/red]")
        return
    
    if args.action == "list":
        # Listar ramas
        success, output, _ = manager._run_git_command(["branch", "-a"])
        if success:
            console.print("\n[bold]Ramas:[/bold]\n")
            console.print(output)
    
    elif args.action == "create":
        # Crear rama
        if not args.name:
            console.print("[red]✗ Especifica el nombre de la rama con --name[/red]")
            return
        
        if manager.create_branch(args.name, args.from_branch):
            console.print(f"[green]✓ Rama '{args.name}' creada[/green]")
    
    elif args.action == "switch":
        # Cambiar de rama
        if not args.name:
            console.print("[red]✗ Especifica el nombre de la rama con --name[/red]")
            return
        
        if manager.switch_branch(args.name):
            console.print(f"[green]✓ Cambiado a '{args.name}'[/green]")
    
    elif args.action == "delete":
        # Eliminar rama
        if not args.name:
            console.print("[red]✗ Especifica el nombre de la rama con --name[/red]")
            return
        
        if manager.delete_branch(args.name, force=args.force):
            console.print(f"[green]✓ Rama '{args.name}' eliminada[/green]")


def cmd_merge(args):
    """Mergea ramas"""
    manager = GitHubManager()
    
    if not manager.is_git_repo():
        console.print("[red]✗ No es un repositorio git[/red]")
        return
    
    console.print(f"[yellow]Mergeando '{args.source}' en '{args.target or 'rama actual'}'...[/yellow]")
    
    if manager.merge_branch(args.source, args.target):
        console.print("[green]✓ Merge exitoso[/green]")
        
        if args.push:
            console.print("[yellow]Pusheando cambios...[/yellow]")
            if manager.push():
                console.print("[green]✓ Push exitoso[/green]")
    else:
        console.print("[red]✗ Error al mergear[/red]")


def cmd_release(args):
    """Crea un release"""
    manager = GitHubManager()
    
    if not manager.is_git_repo():
        console.print("[red]✗ No es un repositorio git[/red]")
        return
    
    # Cambiar a main
    console.print("[yellow]Cambiando a rama main...[/yellow]")
    manager.switch_branch("main")
    
    # Mergear develop
    if args.merge_develop:
        console.print("[yellow]Mergeando develop...[/yellow]")
        if not manager.merge_branch("develop"):
            console.print("[red]✗ Error al mergear develop[/red]")
            return
    
    # Crear tag
    console.print(f"[yellow]Creando tag {args.version}...[/yellow]")
    if manager.create_tag(args.version, args.message):
        console.print(f"[green]✓ Release {args.version} creado[/green]")
    else:
        console.print("[red]✗ Error al crear release[/red]")


def cmd_cleanup(args):
    """Limpia ramas de prueba antiguas"""
    manager = GitHubManager()
    
    if not manager.is_git_repo():
        console.print("[red]✗ No es un repositorio git[/red]")
        return
    
    console.print("[yellow]Buscando ramas de prueba antiguas...[/yellow]")
    
    # Obtener todas las ramas
    success, output, _ = manager._run_git_command(["branch"])
    
    if not success:
        console.print("[red]✗ Error al listar ramas[/red]")
        return
    
    branches = [b.strip().replace('* ', '') for b in output.split('\n') if b.strip()]
    test_branches = [b for b in branches if b.startswith('test/')]
    
    console.print(f"\n[bold]Ramas de prueba encontradas: {len(test_branches)}[/bold]\n")
    
    deleted = 0
    for branch in test_branches:
        if args.force or console.input(f"¿Eliminar '{branch}'? (s/n): ").lower() == 's':
            if manager.delete_branch(branch, force=True):
                console.print(f"[green]✓ Eliminada: {branch}[/green]")
                deleted += 1
    
    console.print(f"\n[green]✓ {deleted} ramas eliminadas[/green]")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Utilidades de GitHub para Sistema A2A',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando: init
    parser_init = subparsers.add_parser('init', help='Inicializar repositorio')
    parser_init.add_argument('--remote', help='URL del repositorio remoto')
    
    # Comando: status
    subparsers.add_parser('status', help='Ver estado del repositorio')
    
    # Comando: commit
    parser_commit = subparsers.add_parser('commit', help='Hacer commit')
    parser_commit.add_argument('-m', '--message', required=True, help='Mensaje del commit')
    parser_commit.add_argument('-d', '--description', help='Descripción adicional')
    parser_commit.add_argument('--push', action='store_true', help='Pushear después del commit')
    
    # Comando: branch
    parser_branch = subparsers.add_parser('branch', help='Gestionar ramas')
    parser_branch.add_argument('action', choices=['list', 'create', 'switch', 'delete'])
    parser_branch.add_argument('--name', help='Nombre de la rama')
    parser_branch.add_argument('--from-branch', help='Rama base para crear')
    parser_branch.add_argument('--force', action='store_true', help='Forzar eliminación')
    
    # Comando: merge
    parser_merge = subparsers.add_parser('merge', help='Mergear ramas')
    parser_merge.add_argument('source', help='Rama fuente')
    parser_merge.add_argument('--target', help='Rama destino (actual si no se especifica)')
    parser_merge.add_argument('--push', action='store_true', help='Pushear después del merge')
    
    # Comando: release
    parser_release = subparsers.add_parser('release', help='Crear release')
    parser_release.add_argument('version', help='Versión (ej: v1.0.0)')
    parser_release.add_argument('-m', '--message', help='Mensaje del release')
    parser_release.add_argument('--merge-develop', action='store_true', help='Mergear develop antes')
    
    # Comando: cleanup
    parser_cleanup = subparsers.add_parser('cleanup', help='Limpiar ramas de prueba')
    parser_cleanup.add_argument('--force', action='store_true', help='No pedir confirmación')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Ejecutar comando
    try:
        if args.command == 'init':
            cmd_init(args)
        elif args.command == 'status':
            cmd_status(args)
        elif args.command == 'commit':
            cmd_commit(args)
        elif args.command == 'branch':
            cmd_branch(args)
        elif args.command == 'merge':
            cmd_merge(args)
        elif args.command == 'release':
            cmd_release(args)
        elif args.command == 'cleanup':
            cmd_cleanup(args)
        
        return 0
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Operación cancelada[/yellow]")
        return 1
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
