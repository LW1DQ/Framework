# Manual de Usuario: Sistema AGENTES A2A v1.4

Este documento sirve como guía integral para el uso del sistema **AGENTES A2A**, actualizado con capacidades de Inteligencia Artificial Avanzada (Deep Reinforcement Learning) y monitoreo en tiempo real.

---

## Parte 1: Descripción de las Mejoras Implementadas

Hemos enriquecido el sistema original con dos componentes críticos para la investigación de nivel doctoral:

### 1.1. Inteligencia Artificial Real (Deep Reinforcement Learning)
Anteriormente, el sistema utilizaba "placeholders" (código de relleno) para la optimización. Ahora, hemos implementado un agente de **Aprendizaje por Refuerzo Profundo (Deep Reinforcement Learning - DRL)** completamente funcional.

*   **Algoritmo**: Utilizamos **PPO (Proximal Policy Optimization)**, considerado el estándar actual por su estabilidad y eficiencia.
*   **Tecnología**: Implementado sobre **PyTorch**, una de las librerías de IA más potentes del mundo.
*   **Funcionamiento**:
    *   El agente "observa" el estado de la red (congestión, vecinos, latencia).
    *   Toma decisiones (cambiar rutas, ajustar potencia).
    *   Recibe una "recompensa" si la red mejora (mayor PDR, menor retardo).
    *   **Aprende** automáticamente con cada simulación, volviéndose más experto con el tiempo.

### 1.2. Dashboard de Monitoreo en Tiempo Real
Para facilitar la supervisión de los experimentos, hemos creado un panel de control visual interactivo.

*   **Tecnología**: Construido con **Streamlit**.
*   **Funcionalidades**:
    *   **Estado del Sistema**: Muestra qué agente (Investigador, Programador, Simulador) está trabajando en este momento.
    *   **Gráficos en Vivo**: Visualiza la evolución del **PDR (Packet Delivery Ratio)**, **Delay** y **Throughput** en tiempo real.
    *   **Transparencia**: Permite leer los "pensamientos" y logs de los agentes mientras trabajan.

### 1.3. Integración Nativa NS-3 AI
Para escenarios de alto rendimiento, el sistema ahora soporta **ns3-ai**, una interfaz de memoria compartida entre Python y C++.
*   **Velocidad**: Elimina la latencia de comunicación entre el agente y el simulador.
*   **Arquitectura**: Usa `RingBuffer` para transferir tensores de estado y acción en microsegundos.
*   **Compatibilidad**: Detecta automáticamente si `ns3-ai` está instalado y lo utiliza; si no, usa el modo estándar.

### 1.4. Sistema de Auto-Corrección Robusta
El sistema ahora cuenta con un manejo de errores estructurado que permite a los agentes recuperarse de fallos comunes sin intervención humana.
*   **Errores de Compilación**: El agente Programador identifica imports faltantes o errores de sintaxis y los corrige automáticamente.
*   **Errores de Simulación**: Si NS-3 falla (ej. configuración inválida), el Simulador captura el error y el Programador ajusta el script.
*   **Timeouts**: Si una simulación tarda demasiado, el sistema la aborta y sugiere simplificar el escenario.

---

## Parte 2: Guía de Instalación Detallada

Siga estos pasos para preparar el entorno en una máquina nueva.

### Prerrequisitos
*   **Sistema Operativo**: Windows (con WSL2 recomendado) o Linux (Ubuntu 20.04/22.04).
*   **Python**: Versión 3.8 o superior.
*   **NS-3**: Debe tener instalado el simulador NS-3 (versión 3.30+ recomendada).
    *   *Opcional*: Para usar la integración de alta velocidad, compile NS-3 con el módulo `ns3-ai`.
*   **Ollama**: Debe tener instalado y ejecutándose Ollama para los modelos de lenguaje.

### Paso 1: Instalar Dependencias de Python
Abra una terminal en la carpeta del proyecto (`sistema-a2a-v1.3-final`) y ejecute:

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar librerías base del proyecto
pip install -r requirements.txt

# Instalar PyTorch (Versión CPU para mayor compatibilidad inicial)
pip install torch torchvision torchaudio

# Instalar librerías del Dashboard
pip install streamlit watchdog plotly
```

### Paso 2: Verificar Instalación de NS-3
Asegúrese de que la variable `NS3_ROOT` en el archivo `config/settings.py` apunte correctamente a su carpeta de instalación de NS-3.

```python
# Ejemplo en config/settings.py
NS3_ROOT = Path("/home/usuario/ns-allinone-3.35/ns-3.35") 
```

### Paso 3: Verificar Modelos de Ollama
Asegúrese de tener los modelos necesarios descargados:

```bash
ollama pull llama3
ollama pull qwen2.5-coder
```

---

## Parte 3: Guía de Uso para Investigadores de Redes

Esta sección está diseñada para expertos en telecomunicaciones que no necesariamente son expertos en IA o Agentes.

### Concepto General
Imagine que tiene un equipo de asistentes virtuales expertos:
*   Un **Investigador** que lee papers por usted.
*   Un **Programador** que escribe scripts de NS-3.
*   Un **Simulador** que ejecuta las pruebas.
*   Un **Analista** que interpreta los resultados.

Usted es el **Director del Proyecto**. Su trabajo es definir el objetivo; los agentes harán el resto.

### 3.1. Cómo Iniciar un Experimento

1.  **Abra una terminal** en la carpeta del proyecto.
2.  **Ejecute el comando principal**:
    ```bash
    python main.py --task "Optimizar protocolo AODV en escenario urbano denso con 50 nodos y alta movilidad"
    ```
    *   *Nota*: Sea descriptivo en la tarea. Incluya el protocolo, número de nodos y tipo de escenario.

### 3.2. Cómo Monitorear el Progreso (Dashboard)

Mientras el sistema trabaja (puede tardar minutos u horas), usted puede ver qué está pasando:

1.  **Abra una SEGUNDA terminal**.
2.  **Ejecute el dashboard**:
    ```bash
    streamlit run dashboard.py
    ```
3.  Se abrirá automáticamente una pestaña en su navegador web.
    *   **Panel Izquierdo**: Verá si el sistema está "Running" (Corriendo) y qué agente está activo.
    *   **Gráficos**: Verá cómo el PDR y el Delay cambian con cada iteración de mejora. Si la línea verde (PDR) sube, el agente está aprendiendo.
    *   **Logs**: Abajo a la izquierda puede leer qué está haciendo cada agente (ej. "Compilando script...", "Analizando resultados...").

### 3.3. Interpretación de Resultados

Al finalizar, el sistema generará varios archivos en la carpeta `simulations/results`:
*   `resultados.xml`: Métricas detalladas de NS-3.
*   `sim_...pcap`: Archivos de captura de paquetes para abrir con **Wireshark**.
*   `optimized_script.py`: El script de Python final con las mejoras aplicadas.

### Preguntas Frecuentes

**¿Qué hago si el PDR es bajo?**
El agente **Optimizador** detectará esto automáticamente y propondrá cambios (ej. ajustar intervalos de Hello, cambiar potencias). Usted verá estas propuestas en el Dashboard.

**¿Necesito saber programar en Python/C++?**
No necesariamente. El agente **Coder** escribe el código por usted. Sin embargo, puede revisar los scripts generados en la carpeta `scratch` de NS-3 si desea validarlos manualmente.

**¿Cómo sé si la IA está funcionando?**
En el Dashboard, observe la gráfica de métricas. En un escenario típico de DRL, verá un rendimiento inestable al principio (exploración) que se estabiliza y mejora después de varias iteraciones (explotación).
