# Sistema Multi-Agente A2A para Optimización de Protocolos de Enrutamiento

## 📋 Descripción

Sistema autónomo de agentes de IA para investigación doctoral en optimización de protocolos de enrutamiento en ciudades inteligentes. Integra NS-3, Ollama (LLMs locales) y LangGraph para automatizar:

- 🔍 Investigación bibliográfica
- 💻 Generación de código de simulación
- 🎯 Ejecución de simulaciones en NS-3
- 📊 Análisis estadístico de resultados
- 📈 Visualización de métricas
- 📝 Documentación automática

## 🎯 Características Principales

- **Costo Cero**: Usa herramientas open-source y modelos locales
- **Reproducible**: Bitácora automática de todos los experimentos
- **Escalable**: Desde 10 hasta 200+ nodos en simulaciones
- **Académico**: Genera reportes en formato IEEE/LaTeX

## 📁 Estructura del Proyecto

```
sistema-a2a-tesis/
├── docs/                    # Documentación completa
│   ├── 01-INSTALACION.md   # Guía de instalación paso a paso
│   ├── 02-CONFIGURACION.md # Configuración del sistema
│   ├── 03-USO-BASICO.md    # Guía de uso básico
│   ├── 04-USO-AVANZADO.md  # Características avanzadas
│   └── 05-TROUBLESHOOTING.md # Solución de problemas
├── agents/                  # Agentes especializados
│   ├── __init__.py
│   ├── researcher.py       # Agente investigador
│   ├── coder.py           # Agente programador
│   ├── simulator.py       # Agente ejecutor
│   ├── analyst.py         # Agente analista
│   └── visualizer.py      # Agente visualizador
├── config/                  # Configuración
│   ├── __init__.py
│   └── settings.py        # Configuración global
├── utils/                   # Utilidades
│   ├── __init__.py
│   ├── state.py           # Estado global
│   └── llm_utils.py       # Utilidades LLM
├── scripts/                 # Scripts de automatización
│   ├── install.sh         # Instalador automático
│   ├── setup_ollama.sh    # Configurar Ollama
│   ├── setup_ns3.sh       # Compilar NS-3
│   ├── check_system.py    # Verificar instalación
│   └── start_system.sh    # Iniciar sistema
├── tests/                   # Pruebas
│   └── test_basic.py      # Pruebas básicas
├── examples/                # Ejemplos de uso
│   ├── ejemplo_basico.py
│   └── ejemplo_completo.py
├── simulations/             # Resultados de simulaciones
│   ├── scripts/           # Scripts NS-3 generados
│   ├── results/           # Resultados XML/CSV
│   └── plots/             # Gráficos generados
├── data/                    # Datos
│   ├── papers/            # Papers descargados
│   └── vector_db/         # Base de datos ChromaDB
├── logs/                    # Logs del sistema
├── supervisor.py            # Orquestador principal
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias Python
└── .gitignore             # Archivos a ignorar

```

## 🚀 Inicio Rápido

### Requisitos Mínimos

- **SO**: Ubuntu 22.04+ (recomendado) o Windows con WSL2
- **RAM**: 16 GB mínimo, 32 GB recomendado
- **Almacenamiento**: 100 GB libres
- **CPU**: 4 cores mínimo

### Instalación en 3 Pasos

```bash
# 1. Clonar o descargar el proyecto
cd sistema-a2a-tesis

# 2. Ejecutar instalador automático (Linux/Mac)
chmod +x scripts/install.sh
./scripts/install.sh

# 3. Verificar instalación
python scripts/check_system.py
```

### Primer Uso

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Ejecutar ejemplo básico
python examples/ejemplo_basico.py

# O usar el sistema completo
python main.py --task "Simular protocolo AODV con 20 nodos"
```

## 📚 Documentación

Consulta la carpeta `docs/` para guías detalladas:

1. **[Instalación](docs/01-INSTALACION.md)** - Instalación paso a paso por etapas
2. **[Configuración](docs/02-CONFIGURACION.md)** - Configurar el sistema
3. **[Uso Básico](docs/03-USO-BASICO.md)** - Primeros pasos y ejemplos
4. **[Uso Avanzado](docs/04-USO-AVANZADO.md)** - Características avanzadas
5. **[Troubleshooting](docs/05-TROUBLESHOOTING.md)** - Solución de problemas

## 🎓 Para el Grupo de Investigación

### Roles y Permisos

- **Investigadores Principales**: Acceso completo, pueden modificar configuración
- **Asistentes de Investigación**: Pueden ejecutar simulaciones y ver resultados
- **Colaboradores**: Solo lectura de resultados

### Flujo de Trabajo Recomendado

1. Definir tarea de investigación clara
2. Ejecutar sistema con `python main.py --task "tu tarea"`
3. Monitorear progreso en logs
4. Revisar resultados en `simulations/`
5. Analizar reportes generados
6. Iterar según necesidad

## 🛠️ Tecnologías Utilizadas

- **NS-3 3.45**: Simulador de redes
- **Ollama**: Inferencia local de LLMs
- **LangGraph**: Orquestación de agentes
- **Python 3.10+**: Lenguaje principal
- **ChromaDB**: Base de datos vectorial
- **Pandas/Matplotlib**: Análisis y visualización

## 📊 Ejemplos de Tareas

```bash
# Comparación de protocolos
python main.py --task "Comparar AODV y OLSR en red de 50 nodos"

# Análisis de escalabilidad
python main.py --task "Evaluar escalabilidad de AODV con 25, 50, 100 nodos"

# Optimización con ML
python main.py --task "Proponer optimización con GNN para enrutamiento en VANET"
```

## 🐛 Reportar Problemas

Si encuentras problemas:

1. Revisa [Troubleshooting](docs/05-TROUBLESHOOTING.md)
2. Ejecuta `python scripts/check_system.py`
3. Revisa logs en `logs/`
4. Contacta al administrador del sistema

## 📄 Licencia

Este proyecto es para uso académico en el contexto de investigación doctoral.

## 👥 Autores

- **Desarrollador Principal**: [Tu Nombre]
- **Grupo de Investigación**: [Nombre del Grupo]
- **Universidad**: UNLP

## 🙏 Agradecimientos

Basado en investigaciones y frameworks open-source de la comunidad académica.

---

**Versión**: 1.0.0  
**Última Actualización**: Noviembre 2025
