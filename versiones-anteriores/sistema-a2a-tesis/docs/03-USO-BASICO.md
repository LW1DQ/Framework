# 📖 Guía de Uso Básico - Sistema A2A

## Para el Grupo de Investigación

Esta guía está diseñada para que cualquier miembro del grupo pueda usar el sistema sin necesidad de conocimientos técnicos profundos.

---

## 🎯 Inicio Rápido (3 Pasos)

### Paso 1: Activar el Entorno

```bash
# Navegar al directorio del proyecto
cd sistema-a2a-tesis

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

**Verificación**: Deberías ver `(venv)` al inicio de tu terminal.

### Paso 2: Verificar que Todo Funciona

```bash
# Ejecutar verificación del sistema
python scripts/check_system.py
```

**Resultado esperado**: Todas las marcas ✅ en verde.

### Paso 3: Ejecutar Tu Primera Tarea

```bash
# Ejemplo simple
python main.py --task "Simular protocolo AODV con 20 nodos"
```

**Tiempo estimado**: 5-10 minutos

---

## 📝 Cómo Definir Tareas

### Estructura de una Tarea

Una buena tarea debe ser **específica** y **clara**. Incluye:

1. **Qué simular**: Protocolo(s) de enrutamiento
2. **Configuración**: Número de nodos, área, duración
3. **Qué medir**: Métricas de interés

### ✅ Ejemplos de Tareas Buenas

```bash
# Ejemplo 1: Comparación básica
python main.py --task "Comparar AODV y OLSR en red de 50 nodos durante 200 segundos"

# Ejemplo 2: Análisis de escalabilidad
python main.py --task "Evaluar escalabilidad de AODV con 25, 50 y 100 nodos. Medir PDR y latencia"

# Ejemplo 3: Escenario específico
python main.py --task "Simular red vehicular (VANET) con 30 vehículos en área urbana de 1000x1000m. Protocolo AODV. Movilidad realista. Duración 300 segundos"

# Ejemplo 4: Con métricas específicas
python main.py --task "Comparar throughput y overhead de AODV vs OLSR en MANET con 40 nodos móviles"
```

### ❌ Ejemplos de Tareas Malas (Muy Vagas)

```bash
# Demasiado vago
python main.py --task "Simular redes"

# Falta información
python main.py --task "Comparar protocolos"

# Sin contexto
python main.py --task "Optimizar enrutamiento"
```

---

## 🎮 Comandos Principales

### Comando Básico

```bash
python main.py --task "Tu tarea aquí"
```

### Con Opciones Avanzadas

```bash
# Más iteraciones (para tareas complejas)
python main.py --task "Tu tarea" --max-iterations 10

# Modo verbose (más información)
python main.py --task "Tu tarea" --verbose

# Continuar experimento previo
python main.py --task "Tu tarea" --thread-id abc-123-def
```

---

## 📊 Entender los Resultados

### Dónde Encontrar los Resultados

Después de ejecutar una tarea, los resultados se guardan en:

```
sistema-a2a-tesis/
├── simulations/
│   ├── results/          # Datos crudos (XML)
│   │   └── sim_20241123_143022.xml
│   ├── plots/            # Gráficos generados
│   │   ├── pdr_per_flow.png
│   │   ├── delay_distribution.png
│   │   └── throughput_flows.png
│   └── scripts/          # Código NS-3 generado
│       └── tesis_sim.py
└── logs/                 # Logs del sistema
    └── sistema_a2a.log
```

### Interpretar los Gráficos

#### 1. PDR (Packet Delivery Ratio)

![PDR Example](../assets/pdr_example.png)

- **Qué muestra**: Porcentaje de paquetes entregados exitosamente
- **Valores buenos**: > 80%
- **Valores malos**: < 60%

#### 2. Delay (Latencia)

![Delay Example](../assets/delay_example.png)

- **Qué muestra**: Tiempo que tarda un paquete en llegar
- **Valores buenos**: < 50 ms
- **Valores malos**: > 200 ms

#### 3. Throughput

![Throughput Example](../assets/throughput_example.png)

- **Qué muestra**: Cantidad de datos transmitidos por segundo
- **Valores buenos**: Depende del escenario (típicamente > 1 Mbps)

---

## 🔍 Monitorear el Progreso

### Ver Logs en Tiempo Real

```bash
# En otra terminal
tail -f logs/sistema_a2a.log
```

### Entender los Mensajes

```
🔍 AGENTE INVESTIGADOR ACTIVADO    # Buscando papers
💻 AGENTE PROGRAMADOR ACTIVADO     # Generando código
⚡ AGENTE SIMULADOR ACTIVADO        # Ejecutando NS-3
🔬 AGENTE ANALISTA ACTIVADO         # Analizando resultados
📊 AGENTE VISUALIZADOR ACTIVADO     # Creando gráficos
```

### Tiempo Estimado por Etapa

| Etapa | Tiempo Típico |
|-------|---------------|
| Investigación | 1-2 minutos |
| Generación de código | 1-2 minutos |
| Simulación NS-3 | 2-5 minutos |
| Análisis | 30 segundos |
| Visualización | 30 segundos |
| **TOTAL** | **5-10 minutos** |

---

## 🛠️ Casos de Uso Comunes

### Caso 1: Comparar Dos Protocolos

**Objetivo**: Determinar cuál protocolo es mejor para tu escenario.

```bash
python main.py --task "Comparar AODV y OLSR en red de 50 nodos. Área 500x500m. Duración 200s. Métricas: PDR, latencia, throughput"
```

**Qué revisar**:
- Gráficos de PDR: ¿Cuál tiene mayor entrega?
- Gráficos de delay: ¿Cuál tiene menor latencia?
- Análisis del agente: Propuesta de optimización

### Caso 2: Análisis de Escalabilidad

**Objetivo**: Ver cómo se comporta un protocolo con diferentes tamaños de red.

```bash
# Ejecutar 3 veces con diferentes tamaños
python main.py --task "Evaluar AODV con 25 nodos"
python main.py --task "Evaluar AODV con 50 nodos"
python main.py --task "Evaluar AODV con 100 nodos"
```

**Qué revisar**:
- Comparar PDR entre los 3 experimentos
- Ver si la latencia aumenta con más nodos
- Identificar el punto donde el rendimiento degrada

### Caso 3: Escenario Específico (VANET)

**Objetivo**: Simular red vehicular realista.

```bash
python main.py --task "Simular VANET con 40 vehículos en ciudad. Protocolo AODV. Movilidad vehicular realista. Área 1000x1000m. Duración 300s. Evaluar PDR y latencia"
```

**Qué revisar**:
- PDR en escenarios de alta movilidad
- Propuesta del agente para optimización con ML

---

## 📋 Checklist de Uso

Antes de ejecutar una tarea, verifica:

- [ ] Entorno virtual activado (`(venv)` visible)
- [ ] Sistema verificado (`python scripts/check_system.py`)
- [ ] Tarea bien definida (específica y clara)
- [ ] Suficiente espacio en disco (al menos 1 GB libre)

Después de ejecutar:

- [ ] Revisar logs para errores
- [ ] Verificar que se generaron gráficos
- [ ] Analizar métricas obtenidas
- [ ] Leer propuesta de optimización del agente

---

## ❓ Preguntas Frecuentes

### ¿Cuánto tarda una simulación?

**Respuesta**: Entre 5-15 minutos dependiendo de la complejidad. Simulaciones con más de 100 nodos pueden tardar más.

### ¿Puedo ejecutar varias tareas en paralelo?

**Respuesta**: No recomendado. El sistema usa recursos intensivos (CPU, RAM). Ejecuta una tarea a la vez.

### ¿Qué hago si la simulación falla?

**Respuesta**: 
1. Revisa `logs/sistema_a2a.log`
2. Verifica que la tarea esté bien definida
3. Intenta con una tarea más simple primero
4. Consulta [Troubleshooting](05-TROUBLESHOOTING.md)

### ¿Cómo guardo mis resultados importantes?

**Respuesta**:
```bash
# Crear carpeta para tu experimento
mkdir mis_resultados/experimento_1

# Copiar resultados
cp simulations/results/sim_*.xml mis_resultados/experimento_1/
cp simulations/plots/*.png mis_resultados/experimento_1/
```

### ¿Puedo modificar el código generado?

**Respuesta**: Sí. El código está en `simulations/scripts/`. Puedes editarlo y ejecutarlo manualmente en NS-3.

---

## 🎓 Mejores Prácticas

### 1. Empieza Simple

Antes de tareas complejas, prueba con algo simple:

```bash
python main.py --task "Simular AODV con 10 nodos"
```

### 2. Documenta Tus Experimentos

Crea un archivo de notas:

```bash
# experimentos.txt
2024-11-23: Comparación AODV vs OLSR - 50 nodos
Resultados: AODV mejor PDR (85% vs 78%)
Archivo: sim_20241123_143022.xml

2024-11-24: Escalabilidad AODV
Resultados: PDR degrada con >100 nodos
```

### 3. Usa Nombres Descriptivos

Al guardar resultados importantes, usa nombres claros:

```bash
mv simulations/results/sim_20241123_143022.xml \
   mis_resultados/aodv_50nodos_urbano.xml
```

### 4. Revisa Siempre los Logs

Antes de confiar en los resultados, verifica que no hubo errores:

```bash
grep "ERROR\|WARN" logs/sistema_a2a.log
```

---

## 🚀 Próximos Pasos

Una vez domines el uso básico:

1. Lee [Uso Avanzado](04-USO-AVANZADO.md) para características avanzadas
2. Explora los [Ejemplos](../examples/) incluidos
3. Consulta [Troubleshooting](05-TROUBLESHOOTING.md) si encuentras problemas

---

## 📞 Soporte

Si tienes problemas:

1. **Primero**: Consulta [Troubleshooting](05-TROUBLESHOOTING.md)
2. **Segundo**: Revisa los logs en `logs/`
3. **Tercero**: Contacta al administrador del sistema

---

**¿Listo para empezar?** Ejecuta tu primera tarea:

```bash
python main.py --task "Simular protocolo AODV con 20 nodos"
```

¡Buena suerte con tu investigación! 🎓
