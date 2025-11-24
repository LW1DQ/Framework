# 📦 INSTALACIÓN COMPLETA - Sistema A2A v1.2

**Framework Multi-Agente para Tesis Doctoral**  
**Versión**: 1.2  
**Fecha de Exportación**: 2024-11-23

---

## 📋 CONTENIDO DEL PAQUETE

Este paquete contiene el framework completo del Sistema A2A listo para instalar en una máquina nueva.

### Estructura del Paquete
```
sistema-a2a-export/
├── agents/                    # 7 agentes especializados
├── config/                    # Configuración del sistema
├── utils/                     # Utilidades compartidas
├── docs/                      # Documentación completa (6 guías)
├── examples/                  # 3 ejemplos funcionales
├── scripts/                   # Scripts de instalación y utilidades
├── simulations/               # Directorio para resultados
├── tests/                     # Tests unitarios
├── logs/                      # Logs del sistema
├── data/                      # Datos y base vectorial
├── main.py                    # Punto de entrada principal
├── supervisor.py              # Supervisor de agentes
├── requirements.txt           # Dependencias Python
└── INSTALACION-COMPLETA.md    # Este archivo
```

---

## 🖥️ REQUISITOS DEL SISTEMA

### Sistema Operativo
- ✅ Linux (Ubuntu 20.04+, Debian 11+)
- ✅ macOS (10.15+)
- ✅ Windows 10/11 (con WSL2 recomendado para NS-3)

### Software Requerido

#### 1. Python
```bash
# Versión requerida: Python 3.8+
python3 --version
```

#### 2. NS-3 (Network Simulator 3)
```bash
# Versión recomendada: NS-3.36 o superior
# Descargar de: https://www.nsnam.org/releases/
```

#### 3. Ollama (LLM Local)
```bash
# Instalar desde: https://ollama.ai/
# O usar comando:
curl -fsSL https://ollama.com/install.sh | sh
```

#### 4. Git (para GitHub Manager)
```bash
git --version
```

### Hardware Recomendado
- **CPU**: 4+ cores
- **RAM**: 8GB+ (16GB recomendado)
- **Disco**: 20GB+ libres
- **GPU**: Opcional (para entrenamiento DL futuro)

---

## 🚀 INSTALACIÓN PASO A PASO

### Paso 1: Copiar el Framework

```bash
# Opción A: Desde USB/Disco
cp -r /ruta/al/usb/sistema-a2a-export ~/sistema-a2a

# Opción B: Desde archivo comprimido
tar -xzf sistema-a2a-export.tar.gz -C ~/
cd ~/sistema-a2a-export
```

### Paso 2: Instalar Python y Dependencias

```bash
# Actualizar sistema (Linux)
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.8+ y pip
sudo apt install python3 python3-pip python3-venv -y

# Crear entorno virtual (RECOMENDADO)
cd ~/sistema-a2a-export
python3 -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 3: Instalar NS-3

#### Opción A: Instalación Completa (Recomendado)

```bash
# Descargar NS-3
cd ~
wget https://www.nsnam.org/releases/ns-allinone-3.38.tar.bz2
tar -xjf ns-allinone-3.38.tar.bz2
cd ns-allinone-3.38

# Compilar NS-3
./build.py --enable-examples --enable-tests

# Configurar Python bindings
cd ns-3.38
./ns3 configure --enable-python-bindings
./ns3 build
```

#### Opción B: Instalación Rápida (Solo Python)

```bash
# Instalar desde pip (limitado)
pip install ns3
```

### Paso 4: Instalar Ollama y Modelos

```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Iniciar servicio Ollama
ollama serve &

# Descargar modelos necesarios
ollama pull llama3.1:8b          # Para razonamiento
ollama pull codellama:13b        # Para generación de código
ollama pull nomic-embed-text     # Para embeddings

# Verificar modelos instalados
ollama list
```

### Paso 5: Configurar el Sistema

```bash
cd ~/sistema-a2a-export

# Editar configuración
nano config/settings.py
```

**Configurar las siguientes variables:**

```python
# Ruta a NS-3 (IMPORTANTE)
NS3_ROOT = Path("/home/usuario/ns-allinone-3.38/ns-3.38")

# URL de Ollama (por defecto localhost)
OLLAMA_BASE_URL = "http://localhost:11434"

# Modelos a usar
MODEL_REASONING = "llama3.1:8b"
MODEL_CODING = "codellama:13b"
MODEL_EMBEDDING = "nomic-embed-text"

# Timeouts
SIMULATION_TIMEOUT = 600  # 10 minutos
```

### Paso 6: Verificar Instalación

```bash
# Ejecutar script de verificación
python scripts/check_system.py
```

**Salida esperada:**
```
✅ Python 3.x encontrado
✅ NS-3 encontrado en /ruta/a/ns-3
✅ Ollama corriendo en http://localhost:11434
✅ Modelos LLM disponibles
✅ Dependencias Python instaladas
✅ Directorios creados correctamente

🎉 Sistema listo para usar!
```

---

## 🧪 PRUEBA INICIAL

### Test Rápido

```bash
# Activar entorno virtual (si no está activo)
source venv/bin/activate

# Ejecutar ejemplo básico
python examples/ejemplo_basico.py
```

### Test Completo

```bash
# Ejecutar sistema completo
python main.py
```

**Cuando se solicite, ingresa:**
```
Tarea: Simular protocolo AODV con 10 nodos en área de 300x300m
```

**Resultados esperados:**
- ✅ Papers encontrados y sintetizados
- ✅ Código NS-3 generado
- ✅ Simulación ejecutada
- ✅ Análisis con KPIs calculados
- ✅ Gráficos generados en `simulations/plots/`
- ✅ Propuesta de optimización (si aplica)
- ✅ Commit en Git (si está configurado)

---

## 🔧 CONFIGURACIÓN AVANZADA

### 1. Configurar GitHub (Opcional)

```bash
cd ~/sistema-a2a-export

# Inicializar repositorio
git init
git config user.name "Tu Nombre"
git config user.email "tu@email.com"

# Conectar con GitHub
git remote add origin https://github.com/tu-usuario/tu-repo.git

# Primer commit
git add .
git commit -m "Instalación inicial del Sistema A2A v1.2"
git push -u origin main
```

### 2. Configurar ChromaDB (Base Vectorial)

```bash
# ChromaDB se instala automáticamente con requirements.txt
# Los datos se guardan en: data/vector_db/

# Para limpiar base de datos:
rm -rf data/vector_db/*
```

### 3. Ajustar Recursos

**Para máquinas con menos recursos:**

Editar `config/settings.py`:
```python
# Reducir timeout
SIMULATION_TIMEOUT = 300  # 5 minutos

# Usar modelos más pequeños
MODEL_REASONING = "llama3.1:7b"
MODEL_CODING = "codellama:7b"
```

**Para máquinas potentes:**
```python
# Aumentar timeout
SIMULATION_TIMEOUT = 1200  # 20 minutos

# Usar modelos más grandes
MODEL_REASONING = "llama3.1:70b"
MODEL_CODING = "codellama:34b"
```

---

## 📁 ESTRUCTURA DE DIRECTORIOS

### Directorios Principales

```
sistema-a2a-export/
│
├── agents/                         # Agentes especializados
│   ├── researcher.py              # Búsqueda de literatura
│   ├── coder.py                   # Generación de código
│   ├── simulator.py               # Ejecución de simulaciones
│   ├── analyst.py                 # Análisis de resultados
│   ├── visualizer.py              # Generación de gráficos
│   ├── github_manager.py          # Gestión de versiones
│   ├── optimizer.py               # Optimización con DL
│   └── __init__.py
│
├── config/                         # Configuración
│   ├── settings.py                # Configuración principal
│   └── __init__.py
│
├── utils/                          # Utilidades
│   ├── state.py                   # Gestión de estado
│   └── __init__.py
│
├── docs/                           # Documentación
│   ├── 01-INSTALACION.md
│   ├── 02-CONFIGURACION.md
│   ├── 03-USO-BASICO.md
│   ├── 04-USO-AVANZADO.md
│   ├── 05-TROUBLESHOOTING.md
│   └── 06-GITHUB-MANAGER.md
│
├── examples/                       # Ejemplos
│   ├── ejemplo_basico.py
│   ├── ejemplo_completo.py
│   └── ejemplo_con_github.py
│
├── scripts/                        # Scripts de utilidad
│   ├── check_system.py            # Verificación del sistema
│   ├── github_utils.py            # Utilidades de Git
│   └── install.sh                 # Script de instalación
│
├── simulations/                    # Resultados de simulaciones
│   ├── scripts/                   # Código generado
│   │   └── backups/              # Backups automáticos
│   ├── results/                   # Resultados XML
│   ├── plots/                     # Gráficos generados
│   └── optimizations/             # Propuestas de optimización
│
├── tests/                          # Tests unitarios
│   └── test_basic.py
│
├── logs/                           # Logs del sistema
│
├── data/                           # Datos
│   ├── papers/                    # Papers descargados
│   └── vector_db/                 # Base de datos vectorial
│
├── main.py                         # Punto de entrada
├── supervisor.py                   # Supervisor de agentes
├── requirements.txt                # Dependencias Python
├── .gitignore                      # Archivos ignorados por Git
│
└── Documentación:
    ├── README.md
    ├── GUIA-RAPIDA.md
    ├── INICIO-RAPIDO-v1.2.md
    ├── INDICE-COMPLETO.md
    ├── CHECKPOINT-MEJORAS-AGENTES.md
    ├── MEJORAS-COMPLETADAS.md
    ├── SESION-COMPLETADA.md
    ├── RESUMEN-VISUAL.txt
    └── INSTALACION-COMPLETA.md    # Este archivo
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS COMUNES

### Problema 1: NS-3 no encontrado

**Error:**
```
FileNotFoundError: NS-3 no encontrado en /ruta/especificada
```

**Solución:**
```bash
# Verificar ruta de NS-3
ls -la ~/ns-allinone-3.38/ns-3.38

# Actualizar config/settings.py con la ruta correcta
nano config/settings.py
# Cambiar: NS3_ROOT = Path("/ruta/correcta/a/ns-3.38")
```

### Problema 2: Ollama no responde

**Error:**
```
ConnectionError: Could not connect to Ollama
```

**Solución:**
```bash
# Verificar si Ollama está corriendo
curl http://localhost:11434/api/tags

# Si no responde, iniciar Ollama
ollama serve &

# Verificar modelos
ollama list
```

### Problema 3: Dependencias faltantes

**Error:**
```
ModuleNotFoundError: No module named 'xxx'
```

**Solución:**
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# O instalar módulo específico
pip install nombre-del-modulo
```

### Problema 4: Permisos de escritura

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solución:**
```bash
# Dar permisos a directorios
chmod -R 755 ~/sistema-a2a-export

# O ejecutar con permisos de usuario
# (NO usar sudo para Python)
```

### Problema 5: Simulación muy lenta

**Solución:**
```python
# Editar config/settings.py
SIMULATION_TIMEOUT = 300  # Reducir timeout

# En la tarea, usar menos nodos
"Simular AODV con 10 nodos"  # En vez de 50+
```

---

## 📚 DOCUMENTACIÓN DISPONIBLE

### Guías de Inicio
1. **README.md** - Introducción general al sistema
2. **INICIO-RAPIDO-v1.2.md** - Inicio rápido en 5 pasos
3. **GUIA-RAPIDA.md** - Guía rápida original

### Documentación Técnica
4. **docs/01-INSTALACION.md** - Instalación detallada
5. **docs/02-CONFIGURACION.md** - Configuración avanzada
6. **docs/03-USO-BASICO.md** - Uso básico del sistema
7. **docs/04-USO-AVANZADO.md** - Funcionalidades avanzadas
8. **docs/05-TROUBLESHOOTING.md** - Solución de problemas
9. **docs/06-GITHUB-MANAGER.md** - Gestión de GitHub

### Documentación de Desarrollo
10. **CHECKPOINT-MEJORAS-AGENTES.md** - Detalles técnicos de mejoras
11. **MEJORAS-COMPLETADAS.md** - Resumen de mejoras v1.2
12. **SESION-COMPLETADA.md** - Resumen de sesión de desarrollo

### Referencias Rápidas
13. **INDICE-COMPLETO.md** - Índice de toda la documentación
14. **RESUMEN-VISUAL.txt** - Resumen visual con estadísticas

---

## 🎓 CASOS DE USO ACADÉMICOS

### 1. Comparación de Protocolos
```bash
python main.py
# Tarea: "Comparar AODV, OLSR y DSDV en red MANET con 30 nodos"
```

### 2. Optimización con Deep Learning
```bash
python main.py
# Tarea: "Optimizar protocolo AODV usando Deep Reinforcement Learning"
```

### 3. Evaluación de Movilidad
```bash
python main.py
# Tarea: "Evaluar impacto de movilidad en OLSR con velocidades 5, 10, 20 m/s"
```

### 4. Análisis de Escalabilidad
```bash
python main.py
# Tarea: "Analizar escalabilidad de AODV con 10, 20, 50 y 100 nodos"
```

---

## 🔄 ACTUALIZACIÓN DEL SISTEMA

### Actualizar Dependencias

```bash
# Activar entorno virtual
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Actualizar dependencias
pip install -r requirements.txt --upgrade
```

### Actualizar Modelos de Ollama

```bash
# Actualizar modelo específico
ollama pull llama3.1:8b

# Actualizar todos los modelos
ollama list | grep -v NAME | awk '{print $1}' | xargs -I {} ollama pull {}
```

### Actualizar NS-3

```bash
# Descargar nueva versión
cd ~
wget https://www.nsnam.org/releases/ns-allinone-3.XX.tar.bz2

# Seguir pasos de instalación de NS-3
# Actualizar NS3_ROOT en config/settings.py
```

---

## 📊 VERIFICACIÓN POST-INSTALACIÓN

### Checklist de Verificación

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias Python instaladas
- [ ] NS-3 compilado y funcionando
- [ ] Ollama instalado y corriendo
- [ ] Modelos LLM descargados
- [ ] config/settings.py configurado
- [ ] Script check_system.py ejecutado exitosamente
- [ ] Ejemplo básico ejecutado sin errores
- [ ] Directorios de resultados creados
- [ ] Git configurado (opcional)

### Comando de Verificación Completa

```bash
cd ~/sistema-a2a-export
source venv/bin/activate
python scripts/check_system.py
```

---

## 🎯 PRÓXIMOS PASOS

### Después de la Instalación

1. **Familiarízate con el sistema**
   ```bash
   # Leer documentación
   cat README.md
   cat INICIO-RAPIDO-v1.2.md
   ```

2. **Ejecuta ejemplos**
   ```bash
   python examples/ejemplo_basico.py
   python examples/ejemplo_completo.py
   ```

3. **Prueba con tu primera tarea**
   ```bash
   python main.py
   # Ingresa una tarea simple
   ```

4. **Revisa resultados**
   ```bash
   # Ver gráficos generados
   ls -la simulations/plots/

   # Ver propuestas de optimización
   ls -la simulations/optimizations/
   ```

5. **Configura GitHub (opcional)**
   ```bash
   git init
   git remote add origin <tu-repo>
   ```

---

## 💡 CONSEJOS IMPORTANTES

### Para Mejor Rendimiento

1. **Usa entorno virtual**: Siempre activa el venv antes de trabajar
2. **Empieza simple**: Primeras tareas con pocos nodos (10-20)
3. **Revisa logs**: Los logs en `logs/` tienen información valiosa
4. **Usa backups**: Los backups en `simulations/scripts/backups/` son útiles
5. **Itera**: El sistema aprende de errores, ejecuta de nuevo si falla

### Para Investigación

1. **Documenta todo**: El sistema crea trazabilidad automática
2. **Usa Git**: Mantén versiones de tus experimentos
3. **Revisa propuestas**: Las propuestas de DL son muy detalladas
4. **Compara resultados**: Usa múltiples ejecuciones para validar
5. **Publica gráficos**: Los gráficos están listos para papers

---

## 📞 SOPORTE Y RECURSOS

### Documentación
- Carpeta `docs/` con 6 guías detalladas
- 14 documentos de referencia en raíz

### Logs y Debugging
- Logs del sistema: `logs/`
- Backups de código: `simulations/scripts/backups/`
- Resultados: `simulations/results/`

### Ejemplos
- `examples/ejemplo_basico.py` - Ejemplo simple
- `examples/ejemplo_completo.py` - Ejemplo completo
- `examples/ejemplo_con_github.py` - Con integración Git

---

## ✅ INSTALACIÓN COMPLETADA

Si llegaste hasta aquí y todos los pasos funcionaron:

🎉 **¡Felicitaciones!** 🎉

El Sistema A2A v1.2 está instalado y listo para impulsar tu investigación doctoral.

### Comando para Empezar

```bash
cd ~/sistema-a2a-export
source venv/bin/activate
python main.py
```

---

**Versión**: 1.2  
**Fecha**: 2024-11-23  
**Estado**: Producción  
**Calidad**: ⭐⭐⭐⭐⭐

**¡Buena suerte con tu tesis doctoral!** 🎓🚀
