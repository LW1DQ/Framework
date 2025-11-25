# 🐙 Agente de GitHub Manager

## Gestión Automática del Proyecto con Git y GitHub

El Agente de GitHub Manager mantiene tu proyecto organizado y versionado automáticamente.

---

## 🎯 Funcionalidades

### Gestión Automática

✅ **Inicialización de Repositorio**
- Crea repositorio git si no existe
- Configura .gitignore automáticamente
- Establece rama principal

✅ **Ramas de Prueba**
- Crea ramas automáticas para cada experimento
- Nomenclatura: `test/experiment_YYYYMMDD_HHMMSS`
- Aísla cambios experimentales

✅ **Commits Automáticos**
- Commitea resultados de simulaciones
- Incluye métricas en el mensaje
- Documenta estado del experimento

✅ **Integración Inteligente**
- Detecta experimentos exitosos
- Sugiere merge a develop
- Mantiene historial limpio

✅ **Gestión de Releases**
- Crea tags para versiones
- Documenta cambios importantes
- Facilita rollback si es necesario

---

## 🚀 Uso Básico

### Configuración Inicial

El agente se activa automáticamente al final de cada experimento.

#### 1. Configurar Repositorio Remoto (Primera Vez)

```bash
# En el directorio del proyecto
cd sistema-a2a-tesis

# Añadir repositorio remoto
git remote add origin https://github.com/tu-usuario/sistema-a2a-tesis.git

# Verificar
git remote -v
```

#### 2. Configurar Credenciales

```bash
# Configurar nombre y email
git config user.name "Tu Nombre"
git config user.email "tu_email@ejemplo.com"

# Para evitar pedir contraseña cada vez (opcional)
git config credential.helper store
```

### Flujo Automático

Cuando ejecutas un experimento:

```bash
python main.py --task "Comparar AODV y OLSR con 50 nodos"
```

El agente de GitHub automáticamente:

1. **Detecta cambios** (resultados, gráficos, logs)
2. **Crea rama de prueba** (`test/experiment_20241123_143022`)
3. **Hace commit** con descripción del experimento
4. **Pushea a GitHub** (si está configurado)
5. **Sugiere integración** si el experimento fue exitoso

---

## 📋 Comandos Manuales

### Usar el Agente Directamente

```python
from agents.github_manager import GitHubManager

# Crear instancia
manager = GitHubManager()

# Inicializar repositorio
manager.init_repo()

# Crear rama
manager.create_branch("feature/nueva-funcionalidad")

# Ver estado
status = manager.get_status()
print(f"Archivos modificados: {len(status['modified'])}")

# Hacer commit
manager.add_files()
manager.commit("Mensaje del commit", "Descripción detallada")

# Push
manager.push()
```

### Operaciones Comunes

#### Crear Rama de Desarrollo

```python
manager = GitHubManager()

# Crear rama develop si no existe
manager.create_branch("develop", from_branch="main")

# Cambiar a develop
manager.switch_branch("develop")
```

#### Integrar Cambios Exitosos

```python
# Después de un experimento exitoso
manager.switch_branch("develop")
manager.merge_branch("test/experiment_20241123_143022")
manager.push("develop")
```

#### Crear Release

```python
# Crear tag para release
manager.switch_branch("main")
manager.merge_branch("develop")
manager.create_tag("v1.0.0", "Primera versión estable")
manager.push("main")
```

---

## 🔄 Flujo de Trabajo Recomendado

### Estructura de Ramas

```
main (producción)
  ↑
develop (desarrollo)
  ↑
test/experiment_* (experimentos)
```

### Ciclo de Vida de un Experimento

1. **Ejecutar Experimento**
   ```bash
   python main.py --task "Tu experimento"
   ```
   - Agente crea rama `test/experiment_*`
   - Commitea resultados automáticamente

2. **Revisar Resultados**
   ```bash
   # Ver qué se commiteó
   git log -1
   
   # Ver cambios
   git show HEAD
   ```

3. **Si el Experimento es Exitoso**
   ```bash
   # Integrar a develop
   git checkout develop
   git merge test/experiment_20241123_143022
   git push origin develop
   
   # Eliminar rama de prueba
   git branch -d test/experiment_20241123_143022
   ```

4. **Si el Experimento Falló**
   ```bash
   # Simplemente ignorar la rama
   # O eliminarla
   git branch -D test/experiment_20241123_143022
   ```

---

## 🎨 Personalización

### Configurar Comportamiento del Agente

Editar `agents/github_manager.py`:

```python
class GitHubManager:
    def __init__(self, repo_path: Path = None):
        self.repo_path = repo_path or Path.cwd()
        self.main_branch = "main"        # Cambiar si usas "master"
        self.dev_branch = "develop"      # Rama de desarrollo
```

### Personalizar Mensajes de Commit

En `github_manager_node()`:

```python
# Personalizar formato del mensaje
commit_msg = f"[Experimento] {task_summary}"

# Añadir más detalles
details = [
    f"Métricas: {state['metrics']}",
    f"Estado: {state['simulation_status']}",
    f"Iteraciones: {state['iteration_count']}"
]
```

### Cambiar Nomenclatura de Ramas

```python
# En lugar de test/experiment_*
test_branch = f"exp/{task_summary[:20]}_{timestamp}"

# O por tipo de experimento
test_branch = f"vanet/test_{timestamp}"
```

---

## 🔧 Integración con GitHub Actions

### Crear Workflow para Tests Automáticos

Crear `.github/workflows/test-experiments.yml`:

```yaml
name: Test Experiments

on:
  push:
    branches:
      - 'test/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ -v
    
    - name: Validate results
      run: |
        python scripts/validate_results.py
```

### Auto-merge de Experimentos Exitosos

Crear `.github/workflows/auto-merge.yml`:

```yaml
name: Auto-merge Successful Experiments

on:
  push:
    branches:
      - 'test/**'

jobs:
  check-and-merge:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Check if experiment succeeded
      id: check
      run: |
        # Verificar si hay archivo de éxito
        if [ -f "simulations/results/success.flag" ]; then
          echo "success=true" >> $GITHUB_OUTPUT
        fi
    
    - name: Create Pull Request
      if: steps.check.outputs.success == 'true'
      uses: peter-evans/create-pull-request@v5
      with:
        branch: develop
        title: "Auto-merge: Successful experiment"
        body: "Experimento completado exitosamente. Revisar e integrar."
```

---

## 📊 Monitoreo y Reportes

### Ver Historial de Experimentos

```python
from agents.github_manager import GitHubManager

manager = GitHubManager()

# Obtener últimos 20 commits
commits = manager.get_commit_history(limit=20)

# Filtrar experimentos
experiments = [c for c in commits if 'Experimento:' in c['message']]

print(f"Total de experimentos: {len(experiments)}")
for exp in experiments:
    print(f"  {exp['date']}: {exp['message']}")
```

### Generar Reporte de Actividad

```python
import pandas as pd

commits = manager.get_commit_history(limit=100)

# Crear DataFrame
df = pd.DataFrame(commits)

# Análisis
print(f"Commits por autor:")
print(df['author'].value_counts())

print(f"\nActividad por día:")
df['date'] = pd.to_datetime(df['date'])
print(df.groupby(df['date'].dt.date).size())
```

---

## 🛡️ Mejores Prácticas

### 1. Commits Frecuentes

✅ **Hacer**: Commitear después de cada experimento exitoso
❌ **Evitar**: Acumular muchos cambios sin commitear

### 2. Mensajes Descriptivos

✅ **Hacer**: "Experimento: Comparación AODV vs OLSR - 50 nodos - PDR: 85%"
❌ **Evitar**: "test", "cambios", "update"

### 3. Ramas Organizadas

✅ **Hacer**: Usar prefijos claros (`test/`, `feature/`, `fix/`)
❌ **Evitar**: Nombres genéricos (`branch1`, `temp`, `new`)

### 4. Limpieza Regular

```bash
# Eliminar ramas de prueba antiguas (más de 30 días)
git branch | grep 'test/' | while read branch; do
    last_commit=$(git log -1 --format=%ct $branch)
    now=$(date +%s)
    age=$(( ($now - $last_commit) / 86400 ))
    if [ $age -gt 30 ]; then
        git branch -D $branch
    fi
done
```

### 5. Backup Regular

```bash
# Pushear todas las ramas importantes
git push origin main develop

# Crear backup local
git bundle create backup_$(date +%Y%m%d).bundle --all
```

---

## 🔍 Troubleshooting

### Problema: "No se puede pushear"

```bash
# Verificar remoto
git remote -v

# Si no hay remoto, añadir
git remote add origin https://github.com/tu-usuario/repo.git

# Verificar credenciales
git config user.name
git config user.email
```

### Problema: "Conflictos al mergear"

```bash
# Ver archivos en conflicto
git status

# Resolver manualmente
nano archivo_en_conflicto.py

# Marcar como resuelto
git add archivo_en_conflicto.py

# Completar merge
git commit
```

### Problema: "Rama no existe en remoto"

```bash
# Crear rama en remoto
git push --set-upstream origin nombre-rama
```

---

## 📚 Recursos Adicionales

### Comandos Git Útiles

```bash
# Ver todas las ramas
git branch -a

# Ver ramas remotas
git branch -r

# Eliminar rama remota
git push origin --delete nombre-rama

# Ver diferencias entre ramas
git diff main..develop

# Ver log gráfico
git log --graph --oneline --all

# Deshacer último commit (mantener cambios)
git reset --soft HEAD~1

# Deshacer último commit (eliminar cambios)
git reset --hard HEAD~1
```

### Configuración Avanzada

```bash
# Alias útiles
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit

# Editor por defecto
git config --global core.editor "nano"

# Colores
git config --global color.ui auto
```

---

## 🎯 Próximos Pasos

1. Configura tu repositorio remoto en GitHub
2. Ejecuta un experimento y observa el agente en acción
3. Revisa las ramas creadas automáticamente
4. Integra experimentos exitosos a develop
5. Crea tu primer release cuando tengas resultados estables

---

**El Agente de GitHub Manager mantiene tu investigación organizada y versionada automáticamente, permitiéndote enfocarte en la ciencia, no en la gestión de código.**
