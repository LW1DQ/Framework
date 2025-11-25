# 🤖 Instalación de ns3-ai para Deep Reinforcement Learning

## Fecha: 24 de Noviembre de 2025

---

## 📋 Descripción

ns3-ai es un módulo de NS-3 que permite la integración de algoritmos de Deep Learning
y Reinforcement Learning con simulaciones de red. Es esencial para la optimización
avanzada de protocolos de enrutamiento.

---

## 🎯 Requisitos Previos

### Software Requerido

- **NS-3 3.36 o superior** (instalado y funcionando)
- **Python 3.8+**
- **PyTorch 1.10+ o TensorFlow 2.x**
- **Git**
- **Compilador C++ con soporte C++17**

### Verificar NS-3

```bash
cd ~/ns-3-dev
./ns3 --version
```

Debe mostrar versión 3.36 o superior.

---

## 📦 Instalación Paso a Paso

### 1. Clonar ns3-ai

```bash
# Navegar al directorio contrib de NS-3
cd ~/ns-3-dev/contrib

# Clonar repositorio
git clone https://github.com/hust-diangroup/ns3-ai.git

# Verificar que se clonó correctamente
ls -la ns3-ai/
```

### 2. Instalar Dependencias Python

```bash
# Activar entorno virtual (si usas uno)
source ~/venv/bin/activate

# Instalar PyTorch (CPU version)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# O TensorFlow
pip install tensorflow

# Instalar dependencias adicionales
pip install gym numpy pandas matplotlib
```

### 3. Configurar NS-3 con ns3-ai

```bash
# Volver al directorio raíz de NS-3
cd ~/ns-3-dev

# Limpiar configuración anterior
./ns3 clean

# Configurar con ns3-ai
./ns3 configure --enable-examples --enable-tests

# Verificar que ns3-ai fue detectado
# Debe aparecer en la lista de módulos habilitados
```

### 4. Compilar NS-3

```bash
# Compilar (puede tardar varios minutos)
./ns3 build

# Verificar compilación exitosa
echo $?
# Debe retornar 0
```

### 5. Verificar Instalación

```bash
# Ejecutar test de ns3-ai
./ns3 run "ns3-ai-gym-test"

# Si pasa el test, la instalación es exitosa
```

---

## 🧪 Prueba de Funcionamiento

### Script de Prueba Básico

Crear archivo `test-ns3-ai.py`:

```python
#!/usr/bin/env python3
"""
Prueba básica de ns3-ai
"""

import sys
sys.path.insert(0, 'build/lib/python3')

try:
    import ns.core
    import ns.ai
    print("✅ ns3-ai importado correctamente")
    print(f"   Versión NS-3: {ns.core.Version()}")
    print(f"   ns3-ai disponible: True")
except ImportError as e:
    print(f"❌ Error importando ns3-ai: {e}")
    sys.exit(1)

print("\n🎉 ns3-ai está correctamente instalado")
```

Ejecutar:

```bash
cd ~/ns-3-dev
python3 test-ns3-ai.py
```

---

## 🔧 Configuración para Sistema A2A

### 1. Actualizar settings.py

Añadir configuración de ns3-ai:

```python
# En sistema-a2a-export/config/settings.py

# ns3-ai Configuration
NS3_AI_ENABLED = True
NS3_AI_GYM_PORT = 5555
NS3_AI_MEMORY_SIZE = 4096  # Tamaño de memoria compartida en bytes
```

### 2. Verificar Integración

```bash
cd sistema-a2a-export
python -c "from agents.ns3_ai_integration import generate_ns3_ai_code; print('✅ Integración OK')"
```

---

## 📚 Uso con Sistema A2A

### Habilitar DRL en Simulaciones

El sistema detecta automáticamente si ns3-ai está disponible y genera código compatible.

#### Opción 1: Automático

El optimizer decide si usar DRL basándose en las métricas:

```bash
python main.py
# El optimizer usará DRL si:
# - PDR < 80%
# - Delay > 150ms
# - Success rate < 70%
```

#### Opción 2: Forzar DRL

```bash
python main.py --force-drl
```

### Archivos Generados

Cuando se usa DRL, el sistema genera:

1. **Código de simulación con ns3-ai**
   - `simulations/scripts/optimized_YYYYMMDD_HHMMSS.py`
   - Incluye integración con ns3-ai
   - Memoria compartida configurada

2. **Script de entrenamiento**
   - `simulations/scripts/train_drl_YYYYMMDD_HHMMSS.py`
   - Entrena el modelo DRL
   - Guarda modelo entrenado

3. **Experiencias de DRL**
   - `drl_experiences.json`
   - Transiciones (estado, acción, recompensa)
   - Usado para entrenamiento

---

## 🎓 Conceptos de DRL para Enrutamiento

### Espacio de Estados

El estado del nodo incluye:
- Número de vecinos
- Buffer ocupado
- Paquetes enviados/recibidos
- Energía restante
- Distancia al destino

### Espacio de Acciones

Acciones posibles:
- Seleccionar siguiente salto
- Ajustar potencia de transmisión
- Establecer prioridad de paquete

### Función de Recompensa

```
R(t) = w1 * PDR_improvement 
     - w2 * normalized_delay 
     - w3 * energy_consumption
     + w4 * throughput_gain
     - w5 * routing_overhead
```

Pesos por defecto:
- w1 = 0.4 (PDR)
- w2 = 0.3 (delay)
- w3 = 0.1 (energía)
- w4 = 0.15 (throughput)
- w5 = 0.05 (overhead)

---

## 🐛 Troubleshooting

### Error: "No module named 'ns.ai'"

**Causa**: ns3-ai no está compilado correctamente

**Solución**:
```bash
cd ~/ns-3-dev
./ns3 clean
./ns3 configure --enable-examples
./ns3 build
```

### Error: "Shared memory error"

**Causa**: Memoria compartida no configurada

**Solución**:
```bash
# Aumentar límite de memoria compartida (Linux)
sudo sysctl -w kernel.shmmax=4294967296
sudo sysctl -w kernel.shmall=1048576
```

### Error: "Gym environment not found"

**Causa**: Falta instalar gym

**Solución**:
```bash
pip install gym
```

### Simulación muy lenta con DRL

**Causa**: Overhead de comunicación Python-C++

**Solución**:
- Reducir frecuencia de decisiones
- Usar batch de acciones
- Entrenar offline primero

---

## 📖 Referencias

### Documentación Oficial

- [ns3-ai GitHub](https://github.com/hust-diangroup/ns3-ai)
- [ns3-ai Wiki](https://github.com/hust-diangroup/ns3-ai/wiki)
- [NS-3 Documentation](https://www.nsnam.org/documentation/)

### Papers Relevantes

1. **ns3-ai: Integrating AI with Network Simulators**
   - Autores: Hao Yin, et al.
   - Año: 2020
   - [Link](https://arxiv.org/abs/2003.13826)

2. **Deep Reinforcement Learning for Routing in MANETs**
   - Autores: Various
   - Año: 2019-2023
   - Múltiples papers en IEEE/ACM

### Tutoriales

- [ns3-ai Tutorial](https://github.com/hust-diangroup/ns3-ai/tree/master/examples)
- [DRL for Networking](https://github.com/topics/deep-reinforcement-learning-networking)

---

## 🎯 Próximos Pasos

Después de instalar ns3-ai:

1. **Ejecutar simulación de prueba**
   ```bash
   cd sistema-a2a-export
   python main.py
   ```

2. **Verificar generación de código DRL**
   - Revisar `simulations/scripts/optimized_*.py`
   - Debe incluir `import ns.ai`

3. **Entrenar modelo**
   ```bash
   python simulations/scripts/train_drl_*.py
   ```

4. **Evaluar resultados**
   - Comparar métricas antes/después de DRL
   - Verificar mejora en PDR, delay, throughput

---

## ✅ Checklist de Instalación

- [ ] NS-3 3.36+ instalado
- [ ] Python 3.8+ disponible
- [ ] PyTorch o TensorFlow instalado
- [ ] ns3-ai clonado en contrib/
- [ ] NS-3 reconfigurado y compilado
- [ ] Test de ns3-ai pasado
- [ ] Integración con Sistema A2A verificada
- [ ] Script de prueba ejecutado exitosamente

---

**Versión**: 1.0  
**Fecha**: 24 de Noviembre de 2025  
**Estado**: ✅ Documentación Completa
