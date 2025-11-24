# 🚀 Inicio Rápido - Sistema A2A v1.2

**Versión**: 1.2  
**Última actualización**: 2024-11-23

---

## ⚡ Instalación en 3 Pasos

### 1. Clonar o Descargar
```bash
cd sistema-a2a-tesis
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Variables
```bash
# Editar config/settings.py
NS3_ROOT = Path("/ruta/a/ns-3")
OLLAMA_BASE_URL = "http://localhost:11434"
```

---

## 🎯 Uso Básico

### Ejecutar Sistema Completo
```bash
python main.py
```

Cuando se solicite, ingresa tu tarea:
```
Ejemplo: "Comparar AODV y OLSR con 20 nodos en área de 500x500m"
```

---

## 📊 Qué Obtendrás

### 1. Investigación Automática
- Papers relevantes de Semantic Scholar y arXiv
- Síntesis con hallazgos clave
- Referencias con URLs

### 2. Código NS-3 Generado
- Script Python completo y ejecutable
- Configuración optimizada
- Comentarios explicativos

### 3. Simulación Ejecutada
- Resultados en XML (FlowMonitor)
- Logs de ejecución
- Backup del código

### 4. Análisis Profundo
- 15+ KPIs calculados
- Clasificación de rendimiento
- Propuesta de optimización con DL

### 5. Visualizaciones Profesionales
- Dashboard de métricas (2x2)
- Gráfico de dispersión PDR vs Delay
- Box plots comparativos
- Top/Bottom 10 flujos

### 6. Optimización (si es necesario)
- Análisis de cuellos de botella
- Propuesta de arquitectura DL
- Código optimizado generado

### 7. Gestión de GitHub
- Rama de experimento creada
- Commit con reporte detallado
- Trazabilidad completa

---

## 📁 Dónde Encontrar Resultados

```
sistema-a2a-tesis/
├── simulations/
│   ├── scripts/
│   │   ├── tesis_sim_TIMESTAMP.py      # Código generado
│   │   ├── optimized_TIMESTAMP.py      # Código optimizado
│   │   └── backups/                    # Backups
│   ├── results/
│   │   ├── sim_TIMESTAMP.xml           # Resultados FlowMonitor
│   │   └── sim_TIMESTAMP_stdout.txt    # Logs
│   ├── plots/
│   │   └── TIMESTAMP/                  # Gráficos
│   │       ├── dashboard_metricas.png
│   │       ├── scatter_pdr_delay.png
│   │       ├── boxplots_metricas.png
│   │       └── top_bottom_flows.png
│   └── optimizations/
│       └── proposal_TIMESTAMP.md       # Propuesta de optimización
```

---

## 🎓 Ejemplos de Tareas

### Comparación de Protocolos
```
"Comparar rendimiento de AODV, OLSR y DSDV en red MANET con 30 nodos"
```

### Optimización con DL
```
"Optimizar protocolo AODV usando Deep Reinforcement Learning"
```

### Evaluación de Movilidad
```
"Evaluar impacto de movilidad en protocolo OLSR con velocidades de 5, 10 y 20 m/s"
```

### Análisis de Escalabilidad
```
"Analizar escalabilidad de AODV con 10, 20, 50 y 100 nodos"
```

---

## 🔧 Configuración Avanzada

### Cambiar Modelos de LLM
Editar `config/settings.py`:
```python
MODEL_REASONING = "llama3.1:8b"      # Para análisis
MODEL_CODING = "codellama:13b"       # Para código
MODEL_EMBEDDING = "nomic-embed-text" # Para RAG
```

### Ajustar Timeouts
```python
SIMULATION_TIMEOUT = 600  # 10 minutos
```

### Configurar GitHub
```bash
# Inicializar repositorio (si no existe)
git init
git remote add origin <tu-repo-url>
```

---

## 🧪 Testing Individual de Agentes

```bash
# Test de investigador
python agents/researcher.py

# Test de programador
python agents/coder.py

# Test de simulador
python agents/simulator.py

# Test de analista
python agents/analyst.py

# Test de visualizador
python agents/visualizer.py

# Test de GitHub manager
python agents/github_manager.py

# Test de optimizador
python agents/optimizer.py
```

---

## 📊 Interpretar Resultados

### Clasificación de Rendimiento
- **Excelente**: PDR > 95%, Delay < 50ms
- **Bueno**: PDR > 85%, Delay < 100ms
- **Regular**: PDR > 70%, Delay < 200ms
- **Pobre**: Por debajo de Regular

### KPIs Principales
- **PDR**: Packet Delivery Ratio (% de paquetes entregados)
- **Delay**: Latencia end-to-end promedio (ms)
- **Throughput**: Tasa de transferencia (Mbps)
- **Success Rate**: % de flujos exitosos

---

## 🐛 Solución Rápida de Problemas

### Error: NS-3 no encontrado
```bash
# Verificar NS3_ROOT en config/settings.py
# Debe apuntar a la carpeta ns-3.XX (no ns-allinone)
```

### Error: Ollama no responde
```bash
# Verificar que Ollama esté corriendo
ollama serve

# En otra terminal, verificar modelos
ollama list
```

### Error: No se generan gráficos
```bash
# Instalar dependencias de visualización
pip install matplotlib seaborn pandas
```

### Error: Git push falla
```bash
# Configurar remoto
git remote add origin <url>

# O trabajar solo localmente (el sistema funciona igual)
```

---

## 💡 Tips y Trucos

### 1. Empezar Simple
Primera vez: usa tareas simples con pocos nodos (10-20).

### 2. Revisar Logs
Los logs en `logs/` contienen información detallada de cada ejecución.

### 3. Usar Backups
Si algo falla, los backups en `simulations/scripts/backups/` tienen todo el código ejecutado.

### 4. Iterar
El sistema aprende de errores. Si falla, ejecuta de nuevo y se auto-corregirá.

### 5. Revisar Propuestas
Las propuestas de optimización en `simulations/optimizations/` son muy detalladas.

---

## 📚 Documentación Completa

Para más detalles, consulta:
- `README.md` - Introducción
- `GUIA-RAPIDA.md` - Guía rápida original
- `docs/` - Documentación detallada
- `MEJORAS-COMPLETADAS.md` - Detalles de mejoras v1.2
- `CHECKPOINT-MEJORAS-AGENTES.md` - Detalles técnicos

---

## 🎯 Flujo de Trabajo Recomendado

```
1. Define tu tarea de investigación
   ↓
2. Ejecuta: python main.py
   ↓
3. Revisa papers encontrados (opcional)
   ↓
4. Espera a que termine la simulación
   ↓
5. Revisa gráficos en simulations/plots/
   ↓
6. Lee propuesta de optimización (si hay)
   ↓
7. Si es necesario, ejecuta de nuevo con código optimizado
   ↓
8. Revisa commits en GitHub para trazabilidad
```

---

## ⚡ Comandos Rápidos

```bash
# Ejecutar sistema completo
python main.py

# Ver últimos resultados
ls -lt simulations/results/ | head

# Ver últimos gráficos
ls -lt simulations/plots/ | head

# Ver propuestas de optimización
ls -lt simulations/optimizations/ | head

# Ver commits recientes
git log --oneline -10

# Ver ramas de experimentos
git branch -a | grep experiment
```

---

## 🎉 ¡Listo!

El sistema está configurado y listo para usar. Simplemente ejecuta:

```bash
python main.py
```

Y sigue las instrucciones en pantalla.

---

## 📞 Ayuda Adicional

Si encuentras problemas:
1. Revisa `docs/05-TROUBLESHOOTING.md`
2. Revisa logs en `logs/`
3. Revisa backups en `simulations/scripts/backups/`
4. Ejecuta tests individuales de agentes

---

**¡Buena suerte con tu investigación!** 🚀🎓
