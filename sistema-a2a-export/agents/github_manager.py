"""
Agente de Gestión de GitHub

Responsable de mantener el proyecto actualizado en GitHub:
- Crear y gestionar ramas
- Hacer commits automáticos
- Crear pull requests
- Integrar cambios cuando funcionan
- Gestionar releases
- Mantener documentación actualizada
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, List, Optional
import subprocess
import json
from datetime import datetime

from utils.state import AgentState, add_audit_entry


class GitHubManager:
    """
    Gestor de GitHub para el proyecto
    """
    
    def __init__(self, repo_path: Path = None):
        """
        Inicializa el gestor de GitHub
        
        Args:
            repo_path: Ruta al repositorio (por defecto, directorio actual)
        """
        self.repo_path = repo_path or Path.cwd()
        self.main_branch = "main"
        self.dev_branch = "develop"
    
    def _run_git_command(self, command: List[str]) -> tuple:
        """
        Ejecuta un comando de git
        
        Args:
            command: Lista con el comando y argumentos
            
        Returns:
            (success, output, error)
        """
        try:
            result = subprocess.run(
                ["git"] + command,
                cwd=str(self.repo_path),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return (
                result.returncode == 0,
                result.stdout.strip(),
                result.stderr.strip()
            )
        except Exception as e:
            return False, "", str(e)
    
    def is_git_repo(self) -> bool:
        """Verifica si el directorio es un repositorio git"""
        success, _, _ = self._run_git_command(["status"])
        return success
    
    def init_repo(self) -> bool:
        """Inicializa un repositorio git"""
        if self.is_git_repo():
            print("✓ Repositorio ya inicializado")
            return True
        
        print("📦 Inicializando repositorio git...")
        success, output, error = self._run_git_command(["init"])
        
        if success:
            print("✓ Repositorio inicializado")
            
            # Configurar rama principal
            self._run_git_command(["branch", "-M", self.main_branch])
            
            # Crear .gitignore si no existe
            gitignore_path = self.repo_path / ".gitignore"
            if not gitignore_path.exists():
                self._create_gitignore()
            
            return True
        else:
            print(f"✗ Error: {error}")
            return False
    
    def _create_gitignore(self):
        """Crea archivo .gitignore básico"""
        gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
*.egg-info/
.pytest_cache/

# Logs
logs/*.log
*.log

# Datos
data/papers/*.pdf
data/vector_db/*
simulations/results/*.xml
simulations/results/*.csv
simulations/plots/*.png

# Base de datos
*.db
*.sqlite

# NS-3
ns-allinone-*/

# Temporales
*.tmp
*.bak
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp

# Configuración local
config/settings_local.py
.env
"""
        gitignore_path = self.repo_path / ".gitignore"
        with open(gitignore_path, 'w') as f:
            f.write(gitignore_content.strip())
        
        print("✓ .gitignore creado")
    
    def get_current_branch(self) -> Optional[str]:
        """Obtiene la rama actual"""
        success, output, _ = self._run_git_command(["branch", "--show-current"])
        return output if success else None
    
    def create_branch(self, branch_name: str, from_branch: str = None) -> bool:
        """
        Crea una nueva rama
        
        Args:
            branch_name: Nombre de la nueva rama
            from_branch: Rama base (por defecto, la actual)
            
        Returns:
            True si se creó exitosamente
        """
        print(f"🌿 Creando rama: {branch_name}")
        
        # Si se especifica rama base, cambiar a ella primero
        if from_branch:
            self._run_git_command(["checkout", from_branch])
        
        # Crear y cambiar a la nueva rama
        success, output, error = self._run_git_command(["checkout", "-b", branch_name])
        
        if success:
            print(f"✓ Rama '{branch_name}' creada")
            return True
        else:
            # Si la rama ya existe, solo cambiar a ella
            if "already exists" in error:
                success, _, _ = self._run_git_command(["checkout", branch_name])
                if success:
                    print(f"✓ Cambiado a rama existente '{branch_name}'")
                    return True
            
            print(f"✗ Error: {error}")
            return False
    
    def switch_branch(self, branch_name: str) -> bool:
        """Cambia a una rama existente"""
        print(f"🔄 Cambiando a rama: {branch_name}")
        
        success, output, error = self._run_git_command(["checkout", branch_name])
        
        if success:
            print(f"✓ Cambiado a '{branch_name}'")
            return True
        else:
            print(f"✗ Error: {error}")
            return False
    
    def get_status(self) -> Dict:
        """Obtiene el estado del repositorio"""
        success, output, _ = self._run_git_command(["status", "--porcelain"])
        
        if not success:
            return {'modified': [], 'untracked': [], 'deleted': []}
        
        modified = []
        untracked = []
        deleted = []
        
        for line in output.split('\n'):
            if not line:
                continue
            
            status = line[:2]
            file_path = line[3:]
            
            if 'M' in status or 'A' in status:
                modified.append(file_path)
            elif '?' in status:
                untracked.append(file_path)
            elif 'D' in status:
                deleted.append(file_path)
        
        return {
            'modified': modified,
            'untracked': untracked,
            'deleted': deleted
        }
    
    def add_files(self, files: List[str] = None) -> bool:
        """
        Añade archivos al staging area
        
        Args:
            files: Lista de archivos (None para añadir todos)
            
        Returns:
            True si se añadieron exitosamente
        """
        if files is None:
            # Añadir todos los archivos
            success, _, error = self._run_git_command(["add", "."])
        else:
            # Añadir archivos específicos
            success, _, error = self._run_git_command(["add"] + files)
        
        if success:
            print(f"✓ Archivos añadidos al staging")
            return True
        else:
            print(f"✗ Error: {error}")
            return False
    
    def commit(self, message: str, description: str = None) -> bool:
        """
        Hace un commit
        
        Args:
            message: Mensaje del commit
            description: Descripción adicional (opcional)
            
        Returns:
            True si el commit fue exitoso
        """
        print(f"💾 Haciendo commit: {message}")
        
        # Construir mensaje completo
        full_message = message
        if description:
            full_message += f"\n\n{description}"
        
        success, output, error = self._run_git_command(["commit", "-m", full_message])
        
        if success:
            print(f"✓ Commit realizado")
            return True
        else:
            if "nothing to commit" in error:
                print("ℹ No hay cambios para commitear")
                return True
            print(f"✗ Error: {error}")
            return False
    
    def push(self, branch: str = None, force: bool = False) -> bool:
        """
        Hace push a GitHub
        
        Args:
            branch: Rama a pushear (None para la actual)
            force: Forzar push
            
        Returns:
            True si el push fue exitoso
        """
        if branch is None:
            branch = self.get_current_branch()
        
        print(f"⬆️  Pusheando a GitHub: {branch}")
        
        command = ["push", "origin", branch]
        if force:
            command.append("--force")
        
        success, output, error = self._run_git_command(command)
        
        if success:
            print(f"✓ Push exitoso")
            return True
        else:
            # Si la rama no existe en remoto, crear con --set-upstream
            if "has no upstream branch" in error or "set-upstream" in error:
                print("ℹ Creando rama en remoto...")
                success, _, error = self._run_git_command([
                    "push", "--set-upstream", "origin", branch
                ])
                if success:
                    print(f"✓ Rama creada y pusheada")
                    return True
            
            print(f"✗ Error: {error}")
            return False
    
    def pull(self, branch: str = None) -> bool:
        """
        Hace pull desde GitHub
        
        Args:
            branch: Rama a pullear (None para la actual)
            
        Returns:
            True si el pull fue exitoso
        """
        if branch is None:
            branch = self.get_current_branch()
        
        print(f"⬇️  Pulleando desde GitHub: {branch}")
        
        success, output, error = self._run_git_command(["pull", "origin", branch])
        
        if success:
            print(f"✓ Pull exitoso")
            return True
        else:
            print(f"✗ Error: {error}")
            return False
    
    def merge_branch(self, source_branch: str, target_branch: str = None) -> bool:
        """
        Mergea una rama en otra
        
        Args:
            source_branch: Rama fuente
            target_branch: Rama destino (None para la actual)
            
        Returns:
            True si el merge fue exitoso
        """
        if target_branch:
            self.switch_branch(target_branch)
        
        current = self.get_current_branch()
        print(f"🔀 Mergeando '{source_branch}' en '{current}'")
        
        success, output, error = self._run_git_command(["merge", source_branch])
        
        if success:
            print(f"✓ Merge exitoso")
            return True
        else:
            if "CONFLICT" in error or "CONFLICT" in output:
                print(f"⚠️  Conflictos detectados. Resolver manualmente.")
            else:
                print(f"✗ Error: {error}")
            return False
    
    def delete_branch(self, branch_name: str, force: bool = False) -> bool:
        """
        Elimina una rama
        
        Args:
            branch_name: Nombre de la rama
            force: Forzar eliminación
            
        Returns:
            True si se eliminó exitosamente
        """
        print(f"🗑️  Eliminando rama: {branch_name}")
        
        flag = "-D" if force else "-d"
        success, output, error = self._run_git_command(["branch", flag, branch_name])
        
        if success:
            print(f"✓ Rama eliminada")
            return True
        else:
            print(f"✗ Error: {error}")
            return False
    
    def create_tag(self, tag_name: str, message: str = None) -> bool:
        """
        Crea un tag (para releases)
        
        Args:
            tag_name: Nombre del tag (ej: v1.0.0)
            message: Mensaje del tag
            
        Returns:
            True si se creó exitosamente
        """
        print(f"🏷️  Creando tag: {tag_name}")
        
        if message:
            success, output, error = self._run_git_command([
                "tag", "-a", tag_name, "-m", message
            ])
        else:
            success, output, error = self._run_git_command(["tag", tag_name])
        
        if success:
            print(f"✓ Tag creado")
            
            # Pushear tag
            self._run_git_command(["push", "origin", tag_name])
            print(f"✓ Tag pusheado")
            
            return True
        else:
            print(f"✗ Error: {error}")
            return False
    
    def get_commit_history(self, limit: int = 10) -> List[Dict]:
        """
        Obtiene el historial de commits
        
        Args:
            limit: Número de commits a obtener
            
        Returns:
            Lista de commits
        """
        success, output, _ = self._run_git_command([
            "log", f"-{limit}", "--pretty=format:%H|%an|%ae|%ad|%s"
        ])
        
        if not success or not output:
            return []
        
        commits = []
        for line in output.split('\n'):
            parts = line.split('|')
            if len(parts) == 5:
                commits.append({
                    'hash': parts[0],
                    'author': parts[1],
                    'email': parts[2],
                    'date': parts[3],
                    'message': parts[4]
                })
        
        return commits


def create_experiment_report(state: AgentState) -> str:
    """
    Crea un reporte detallado del experimento para el commit
    
    Args:
        state: Estado del sistema
        
    Returns:
        Reporte formateado
    """
    report = []
    
    # Información básica
    report.append(f"Tarea: {state.get('task', 'N/A')}")
    report.append(f"Iteración: {state.get('iteration', 0) + 1}")
    report.append("")
    
    # Estado de simulación
    sim_status = state.get('simulation_status', 'unknown')
    report.append(f"Estado de Simulación: {sim_status}")
    
    if sim_status == 'completed':
        report.append("✅ Simulación exitosa")
    elif sim_status == 'failed':
        report.append("❌ Simulación fallida")
    
    report.append("")
    
    # Métricas si existen
    if state.get('metrics'):
        metrics = state['metrics']
        report.append("Métricas Obtenidas:")
        report.append(f"  - PDR: {metrics.get('avg_pdr', 0):.2f}%")
        report.append(f"  - Delay: {metrics.get('avg_delay', 0):.2f} ms")
        report.append(f"  - Throughput: {metrics.get('avg_throughput', 0):.3f} Mbps")
        report.append(f"  - Flujos exitosos: {metrics.get('successful_flows', 0)}/{metrics.get('total_flows', 0)}")
        report.append(f"  - Clasificación: {metrics.get('performance_grade', 'N/A')}")
        report.append("")
    
    # Información de ejecución
    if state.get('execution_time'):
        report.append(f"Tiempo de ejecución: {state['execution_time']:.2f}s")
    
    # Archivos generados
    if state.get('plots_generated'):
        report.append(f"Gráficos generados: {len(state['plots_generated'])}")
    
    if state.get('code_filepath'):
        report.append(f"Código: {Path(state['code_filepath']).name}")
    
    # Errores si existen
    if state.get('errors'):
        report.append("")
        report.append("Errores:")
        for error in state['errors'][-3:]:  # Últimos 3 errores
            report.append(f"  - {error[:100]}")
    
    return "\n".join(report)


def github_manager_node(state: AgentState) -> Dict:
    """
    Nodo del agente de GitHub para LangGraph con gestión inteligente
    
    Args:
        state: Estado actual del sistema
        
    Returns:
        Diccionario con actualizaciones al estado
    """
    print("\n" + "="*80)
    print("🐙 AGENTE GITHUB MANAGER ACTIVADO")
    print("="*80)
    
    manager = GitHubManager()
    
    # Verificar si es un repositorio git
    if not manager.is_git_repo():
        print("📦 Inicializando repositorio...")
        if not manager.init_repo():
            return {
                'errors': ['No se pudo inicializar el repositorio git'],
                **add_audit_entry(state, "github_manager", "init_failed", {})
            }
    
    # Obtener estado actual
    current_branch = manager.get_current_branch()
    status = manager.get_status()
    
    print(f"\n📍 Rama actual: {current_branch}")
    print(f"📝 Archivos modificados: {len(status['modified'])}")
    print(f"📄 Archivos nuevos: {len(status['untracked'])}")
    
    if status['deleted']:
        print(f"🗑️  Archivos eliminados: {len(status['deleted'])}")
    
    # Mostrar algunos archivos modificados
    if status['modified']:
        print(f"\n📋 Archivos modificados (primeros 5):")
        for file in status['modified'][:5]:
            print(f"   - {file}")
    
    if status['untracked']:
        print(f"\n📋 Archivos nuevos (primeros 5):")
        for file in status['untracked'][:5]:
            print(f"   - {file}")
    
    # Determinar acción basada en el estado
    action_taken = None
    branch_created = None
    commit_hash = None
    
    # Si hay cambios, crear rama de experimento y commitear
    if status['modified'] or status['untracked'] or status['deleted']:
        # Determinar tipo de rama basado en el estado
        sim_status = state.get('simulation_status', 'unknown')
        iteration = state.get('iteration', 0)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if sim_status == 'completed':
            branch_prefix = "experiment/success"
        elif sim_status == 'failed':
            branch_prefix = "experiment/failed"
        else:
            branch_prefix = "experiment/test"
        
        test_branch = f"{branch_prefix}_{timestamp}_iter{iteration+1}"
        
        print(f"\n🌿 Creando rama de experimento: {test_branch}")
        
        if manager.create_branch(test_branch):
            branch_created = test_branch
            
            # Añadir archivos
            print("📦 Añadiendo archivos al staging...")
            if manager.add_files():
                # Crear mensaje de commit detallado
                task_summary = state.get('task', 'Experimento')[:60]
                commit_msg = f"[{sim_status.upper()}] {task_summary}"
                
                # Crear descripción detallada
                description = create_experiment_report(state)
                
                print(f"\n💾 Creando commit...")
                print(f"   Mensaje: {commit_msg}")
                
                if manager.commit(commit_msg, description):
                    print("   ✓ Commit realizado")
                    
                    # Obtener hash del commit
                    commits = manager.get_commit_history(limit=1)
                    if commits:
                        commit_hash = commits[0]['hash']
                        print(f"   📌 Hash: {commit_hash[:7]}")
                    
                    # Intentar push
                    print(f"\n⬆️  Intentando push a remoto...")
                    if manager.push(test_branch):
                        print("   ✓ Cambios pusheados a GitHub")
                        action_taken = "branch_created_and_pushed"
                        
                        # Si la simulación fue exitosa, sugerir PR
                        if sim_status == 'completed':
                            print(f"\n✅ SIMULACIÓN EXITOSA")
                            print(f"   📊 Métricas: PDR={state.get('metrics', {}).get('avg_pdr', 0):.1f}%")
                            print(f"   💡 Sugerencia: Crear Pull Request para integrar cambios")
                            print(f"   🔗 Rama: {test_branch}")
                    else:
                        print("   ⚠️  No se pudo pushear")
                        print("   💡 Posibles causas:")
                        print("      - No hay remoto configurado (git remote add origin <url>)")
                        print("      - No hay permisos de escritura")
                        print("      - No hay conexión a internet")
                        action_taken = "branch_created_locally"
                else:
                    print("   ❌ Commit falló")
                    action_taken = "commit_failed"
            else:
                print("   ❌ No se pudieron añadir archivos")
                action_taken = "add_failed"
        else:
            print("   ❌ No se pudo crear rama")
            action_taken = "branch_creation_failed"
    else:
        print("\nℹ️  No hay cambios para commitear")
        action_taken = "no_changes"
    
    # Estadísticas del repositorio
    print(f"\n📊 Estadísticas del Repositorio:")
    commits = manager.get_commit_history(limit=10)
    print(f"   Total de commits recientes: {len(commits)}")
    
    if commits:
        print(f"\n📜 Últimos 5 commits:")
        for i, commit in enumerate(commits[:5], 1):
            print(f"   {i}. {commit['hash'][:7]} - {commit['message'][:60]}")
            print(f"      Por: {commit['author']} - {commit['date'][:16]}")
    
    # Resumen de acción
    print(f"\n{'='*80}")
    print(f"📋 RESUMEN DE ACCIÓN")
    print(f"{'='*80}")
    print(f"Acción: {action_taken}")
    if branch_created:
        print(f"Rama creada: {branch_created}")
    if commit_hash:
        print(f"Commit: {commit_hash[:7]}")
    print(f"{'='*80}")
    
    # Preparar resultado
    result = {
        'messages': [f"GitHub: {action_taken}"],
        'github_branch': branch_created,
        'github_commit': commit_hash,
        **add_audit_entry(state, "github_manager", action_taken, {
            'branch': current_branch,
            'new_branch': branch_created,
            'commit_hash': commit_hash,
            'modified_files': len(status['modified']),
            'new_files': len(status['untracked']),
            'deleted_files': len(status['deleted']),
            'simulation_status': state.get('simulation_status', 'unknown')
        })
    }
    
    # Si fue exitoso y hay métricas, añadir sugerencia de tag/release
    if (action_taken == "branch_created_and_pushed" and 
        state.get('simulation_status') == 'completed' and
        state.get('metrics', {}).get('performance_grade') in ['Excelente', 'Bueno']):
        
        result['messages'].append(
            f"💡 Rendimiento {state['metrics']['performance_grade']}: "
            f"Considerar crear tag/release"
        )
    
    return result


if __name__ == "__main__":
    # Prueba del agente
    from utils.state import create_initial_state
    
    test_state = create_initial_state("Prueba de GitHub Manager")
    test_state['simulation_status'] = 'completed'
    test_state['metrics'] = {'pdr': 85.5, 'delay': 45.2}
    
    result = github_manager_node(test_state)
    
    print("\n" + "="*80)
    print("RESULTADO DE PRUEBA")
    print("="*80)
    print(f"Mensajes: {result.get('messages', [])}")
    print(f"Errores: {result.get('errors', [])}")
