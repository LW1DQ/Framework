# 🚀 Guía de Instalación de ns3-ai

Guía completa para instalar y configurar ns3-ai para comunicación Python-C++ con NS-3.

---

## 📋 Requisitos Previos

- **NS-3 3.36+** instalado y compilado
- **Python 3.8+**
- **CMake 3.10+**
- **Protobuf** (para serialización)
- **ZMQ** (opcional, para comunicación alternativa)

---

## 🔧 PASO 1: Instalar Dependencias del Sistema

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y \
    cmake \
    g++ \
    python3-dev \
    libprotobuf-dev \
    protobuf-compiler \
    libzmq3-dev \
    python3-pip
```

### Fedora

```bash
sudo dnf install -y \
    cmake \
    gcc-c++ \
    python3-devel \
    protobuf-devel \
    protobuf-compiler \
    zeromq-devel \
    python3-pip
```

### macOS

```bash
brew install cmake protobuf zeromq python@3.10
```

---

## 🔧 PASO 2: Clonar ns3-ai

```bash
# Navegar al directorio contrib de NS-3
cd ~/ns-3-dev/contrib

# Clonar ns3-ai
git clone https://github.com/hust-diangroup/ns3-ai.git

# Verificar estructura
ls -la ns3-ai/
```

**Estructura esperada:**
```
ns3-ai/
├── model/
├── examples/
├── py_interface/
├── CMakeLists.txt
└── wscript
```

---

## 🔧 PASO 3: Compilar NS-3 con ns3-ai

```bash
# Volver al directorio raíz de NS-3
cd ~/ns-3-dev

# Limpiar compilación anterior (opcional)
./ns3 clean

# Configurar con ns3-ai habilitado
./ns3 configure \
    --enable-examples \
    --enable-tests \
    --enable-python-bindings

# Compilar
./ns3 build

# Verificar que ns3-ai se compiló
./ns3 show modules | grep ns3-ai
```

**Salida esperada:**
```
ns3-ai
```

---

## 🔧 PASO 4: Instalar Interfaz Python de ns3-ai

```bash
# Navegar al directorio de interfaz Python
cd ~/ns-3-dev/contrib/ns3-ai/py_interface

# Instalar en modo desarrollo
pip install -e .

# Verificar instalación
python3 -c "import ns3_ai; print('✅ ns3-ai instalado correctamente')"
```

---

## 🔧 PASO 5: Probar Instalación con Ejemplo

### Ejecutar Ejemplo Básico

```bash
cd ~/ns-3-dev

# Ejecutar ejemplo de ns3-ai
./ns3 run ns3-ai-gym-example

# O ejecutar ejemplo de mensajes
./ns3 run ns3-ai-msg-example
```

**Salida esperada:**
```
🚀 Iniciando ejemplo ns3-ai...
✅ Comunicación Python-C++ establecida
📊 Intercambiando mensajes...
✅ Ejemplo completado exitosamente
```

---

## 🔧 PASO 6: Integrar con Sistema A2A

### 6.1 Instalar Módulo DRL Routing

```bash
# Navegar al directorio de integración
cd /ruta/a/sistema-a2a/ns3-integration

# Dar permisos de ejecución
chmod +x install-drl-module.sh

# Ejecutar instalación
./install-drl-module.sh
```

### 6.2 Verificar Módulo DRL

```bash
cd ~/ns-3-dev

# Verificar que el módulo se compiló
./ns3 show modules | grep drl-routing

# Ejecutar ejemplo
./ns3 run drl-routing-example
```

**Salida esperada:**
```
[INFO] Agente DRL creado para nodo 0
[INFO]   Estado inicial: neighbors=4 pdr=1
[INFO] Agente DRL creado para nodo 1
...
[INFO] Simulación completada
```

---

## 🔧 PASO 7: Configurar Comunicación Python-C++

### 7.1 Crear Script de Prueba

```python
# test_ns3_ai_communication.py
import sys
sys.path.insert(0, 'build/lib/python3')

from ns3_ai import Ns3AiMsgInterface
import numpy as np
import time

# Definir estructuras (deben coincidir con C++)
class EnvState:
    def __init__(self):
        self.buffer_occupancy = 0.0
        self.num_neighbors = 0.0
        self.recent_pdr = 0.0
        self.recent_delay = 0.0
        self.distance_to_dest = 0.0
        self.hops_to_dest = 0.0
        self.energy_level = 0.0
        self.avg_neighbor_load = 0.0
        self.packet_priority = 0.0
        self.time_in_queue = 0.0

class AgentAction:
    def __init__(self):
        self.next_hop_id = 0
        self.tx_power = 1.0
        self.priority = 0

# Inicializar interfaz
interface = Ns3AiMsgInterface(
    "drl_routing_shm",
    size=4096,
    isMemoryCreator=False
)

print("✅ Interfaz ns3-ai inicializada")
print("🔄 Esperando mensajes desde NS-3...")

# Bucle de comunicación
for i in range(10):
    try:
        # Leer estado desde NS-3
        state = interface.GetCpp2PyStruct()
        print(f"\n📥 Estado recibido #{i+1}:")
        print(f"   Neighbors: {state.num_neighbors}")
        print(f"   PDR: {state.recent_pdr:.3f}")
        print(f"   Delay: {state.recent_delay:.1f}ms")
        
        # Tomar decisión (simple)
        action = AgentAction()
        action.next_hop_id = int(state.num_neighbors / 2)
        action.tx_power = 1.0
        action.priority = 0
        
        # Enviar acción a NS-3
        interface.SetPy2CppStruct(action)
        print(f"📤 Acción enviada: next_hop={action.next_hop_id}")
        
        time.sleep(0.1)
        
    except KeyboardInterrupt:
        print("\n🛑 Detenido por usuario")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        break

print("\n✅ Test completado")
```

### 7.2 Ejecutar Test

```bash
# Terminal 1: Ejecutar simulación NS-3
cd ~/ns-3-dev
./ns3 run drl-routing-example

# Terminal 2: Ejecutar agente Python
cd ~/ns-3-dev
python3 test_ns3_ai_communication.py
```

---

## 🔧 PASO 8: Integrar con Sistema A2A

### 8.1 Actualizar Configuración

```python
# config/settings.py

# Añadir configuración de ns3-ai
NS3_AI_ENABLED = True
NS3_AI_SHM_NAME = "drl_routing_shm"
NS3_AI_SHM_SIZE = 4096
```

### 8.2 Ejecutar Simulación con DRL

```bash
cd /ruta/a/sistema-a2a

# Activar entorno virtual
source venv/bin/activate

# Ejecutar con DRL habilitado
python main.py --task "Simular AODV con DRL, 20 nodos, 200 segundos"
```

---

## 🐛 Troubleshooting

### Error: "ns3-ai module not found"

**Solución:**
```bash
cd ~/ns-3-dev/contrib
ls -la | grep ns3-ai

# Si no existe, clonar:
git clone https://github.com/hust-diangroup/ns3-ai.git

# Recompilar NS-3
cd ~/ns-3-dev
./ns3 clean
./ns3 configure --enable-examples
./ns3 build
```

### Error: "Cannot import ns3_ai in Python"

**Solución:**
```bash
cd ~/ns-3-dev/contrib/ns3-ai/py_interface
pip install -e .

# Verificar
python3 -c "import ns3_ai; print(ns3_ai.__file__)"
```

### Error: "Shared memory not found"

**Solución:**
```bash
# Verificar que NS-3 esté corriendo primero
# NS-3 crea la memoria compartida, Python se conecta a ella

# Limpiar memoria compartida antigua
ipcs -m | grep drl_routing
# Si hay entradas, eliminarlas:
ipcrm -m <shmid>
```

### Error: "Timeout waiting for NS-3"

**Solución:**
- Asegurarse de que NS-3 esté corriendo
- Verificar que el nombre de memoria compartida coincida
- Aumentar timeout en código Python

---

## 📚 Recursos Adicionales

- **Documentación oficial ns3-ai:** https://github.com/hust-diangroup/ns3-ai/wiki
- **Ejemplos de ns3-ai:** `~/ns-3-dev/contrib/ns3-ai/examples/`
- **Paper original:** https://arxiv.org/abs/2003.10174

---

## ✅ Verificación Final

Ejecuta este checklist para verificar que todo está instalado:

```bash
# 1. NS-3 compilado
cd ~/ns-3-dev && ./ns3 --version

# 2. ns3-ai disponible
./ns3 show modules | grep ns3-ai

# 3. Interfaz Python instalada
python3 -c "import ns3_ai; print('OK')"

# 4. Módulo DRL instalado
./ns3 show modules | grep drl-routing

# 5. Ejemplo funciona
./ns3 run drl-routing-example
```

Si todos los pasos pasan: **✅ Instalación completa!**

---

**Última actualización:** Noviembre 2025  
**Versión:** 1.0  
**Autor:** Sistema A2A Team
