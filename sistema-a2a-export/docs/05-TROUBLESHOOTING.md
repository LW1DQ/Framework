# 🔧 Troubleshooting - Sistema A2A

## Guía de Solución de Problemas

Esta guía te ayudará a resolver los problemas más comunes del sistema.

---

## 🚨 Problemas Comunes

### Índice Rápido

1. [Ollama no responde](#ollama-no-responde)
2. [NS-3 no compila](#ns-3-no-compila)
3. [Python bindings fallan](#python-bindings-fallan)
4. [Simulación falla](#simulación-falla)
5. [Memoria insuficiente](#memoria-insuficiente)
6. [Timeout en simulaciones](#timeout-en-simulaciones)
7. [Modelos no encontrados](#modelos-no-encontrados)
8. [Errores de dependencias](#errores-de-dependencias)

---

## Ollama no responde

### Síntomas

```
❌ Ollama no responde en: http://localhost:11434
Error: Connection refused
```

### Diagnóstico

```bash
# Verificar si Ollama está corriendo
ps aux | grep ollama

# Verificar puerto
curl http://localhost:11434/api/tags
```

### Soluciones

#### Solución 1: Reiniciar Ollama

```bash
# Detener Ollama
pkill ollama

# Esperar 2 segundos
sleep 2

# Iniciar Ollama
ollama serve &

# Esperar 5 segundos
sleep 5

# Verificar
curl http://localhost:11434/api/tags
```

#### Solución 2: Verificar Puerto

```bash
# Ver qué está usando el puerto 11434
sudo lsof -i :11434

# Si otro proceso lo usa, cambiar puerto en config/settings.py
# OLLAMA_BASE_URL = "http://localhost:8080"

# Iniciar Ollama en otro puerto
OLLAMA_HOST=0.0.0.0:8080 ollama serve &
```

#### Solución 3: Reinstalar Ollama

```bash
# Desinstalar
sudo rm -rf /usr/local/bin/ollama
sudo rm -rf ~/.ollama

# Reinstalar
curl -fsSL https://ollama.com/install.sh | sh

# Descargar modelos nuevamente
ollama pull llama3.1:8b
ollama pull deepseek-coder-v2:16b
```

---

## NS-3 no compila

### Síntomas

```
❌ NS-3 no encontrado en: /home/usuario/tesis-a2a/ns-allinone-3.43/ns-3.43
Error: No such file or directory
```

### Diagnóstico

```bash
# Verificar si NS-3 existe
ls ~/tesis-a2a/ns-allinone-3.43/ns-3.43

# Verificar ejecutable ns3
ls ~/tesis-a2a/ns-allinone-3.43/ns-3.43/ns3
```

### Soluciones

#### Solución 1: Ajustar Ruta en Configuración

```python
# Editar config/settings.py
# Línea ~18

# Encontrar dónde está NS-3
find ~ -name "ns3" -type f 2>/dev/null

# Ajustar NS3_ROOT con la ruta correcta
NS3_ROOT = Path("/ruta/correcta/a/ns-3.43")
```

#### Solución 2: Limpiar y Recompilar

```bash
cd ~/tesis-a2a/ns-allinone-3.43/ns-3.43

# Limpiar compilación anterior
./ns3 clean

# Reconfigurar
./ns3 configure --enable-python-bindings --enable-examples

# Recompilar
./ns3 build --jobs=$(nproc)

# Verificar
./ns3 run hello-simulator
```

#### Solución 3: Reinstalar NS-3

```bash
cd ~/tesis-a2a

# Eliminar instalación anterior
rm -rf ns-allinone-3.43

# Descargar nuevamente
wget https://www.nsnam.org/releases/ns-allinone-3.43.tar.bz2
tar xjf ns-allinone-3.43.tar.bz2

# Compilar
cd ns-allinone-3.43/ns-3.43
./ns3 configure --enable-python-bindings
./ns3 build
```

---

## Python bindings fallan

### Síntomas

```python
ImportError: No module named 'ns.core'
ModuleNotFoundError: No module named 'ns'
```

### Diagnóstico

```bash
cd ~/tesis-a2a/ns-allinone-3.43/ns-3.43

# Verificar que bindings estén habilitados
./ns3 show config | grep python

# Debe mostrar: Python Bindings: enabled
```

### Soluciones

#### Solución 1: Reconfigurar con Python Específico

```bash
cd ~/tesis-a2a/ns-allinone-3.43/ns-3.43

# Especificar Python explícitamente
./ns3 configure \
  --enable-python-bindings \
  --with-python=/usr/bin/python3.10

# Recompilar
./ns3 build

# Probar
python3 << EOF
import sys
sys.path.insert(0, 'build/lib/python3')
import ns.core
print("✓ Bindings OK")
EOF
```

#### Solución 2: Instalar Dependencias Python

```bash
# Instalar python3-dev
sudo apt install python3-dev python3-pip

# Reinstalar pybindgen
pip install pybindgen

# Reconfigurar NS-3
cd ~/tesis-a2a/ns-allinone-3.43/ns-3.43
./ns3 configure --enable-python-bindings
./ns3 build
```

#### Solución 3: Verificar Versión de Python

```bash
# NS-3 requiere Python 3.6+
python3 --version

# Si es menor, actualizar
sudo apt install python3.10 python3.10-dev

# Reconfigurar NS-3 con nueva versión
./ns3 configure \
  --enable-python-bindings \
  --with-python=/usr/bin/python3.10
```

---

## Simulación falla

### Síntomas

```
❌ Simulación falló (código: 1)
NS-3 Error: AttributeError: module 'ns.network' has no attribute 'MobilityHelper'
```

### Diagnóstico

```bash
# Ver logs completos
cat logs/sistema_a2a.log | grep ERROR

# Ver código generado
cat simulations/scripts/tesis_sim.py
```

### Soluciones

#### Solución 1: Código Generado Incorrecto

El sistema intentará auto-corregir. Si falla después de 5 intentos:

```bash
# Ejecutar con más iteraciones
python main.py --task "Tu tarea" --max-iterations 10

# O simplificar la tarea
python main.py --task "Simular AODV con 10 nodos (simple)"
```

#### Solución 2: Módulos NS-3 Faltantes

```bash
cd ~/tesis-a2a/ns-allinone-3.43/ns-3.43

# Ver módulos disponibles
./ns3 show modules

# Si falta alguno, recompilar con todos los módulos
./ns3 configure --enable-python-bindings --enable-modules=all
./ns3 build
```

#### Solución 3: Editar Código Manualmente

```bash
# Ver código generado
nano simulations/scripts/tesis_sim.py

# Corregir errores manualmente

# Ejecutar directamente en NS-3
cd ~/tesis-a2a/ns-allinone-3.43/ns-3.43
./ns3 run scratch/tesis_sim.py
```

---

## Memoria insuficiente

### Síntomas

```
MemoryError: Unable to allocate array
Killed (OOM)
```

### Diagnóstico

```bash
# Ver uso de memoria
free -h

# Ver procesos que usan más memoria
ps aux --sort=-%mem | head -10
```

### Soluciones

#### Solución 1: Usar Modelos Más Pequeños

```python
# Editar config/settings.py

# Cambiar a modelos más ligeros
MODEL_REASONING = "llama3.1:8b"  # En lugar de 70b
MODEL_CODING = "qwen2.5-coder:7b"  # En lugar de deepseek 16b
```

#### Solución 2: Cerrar Otros Programas

```bash
# Cerrar navegadores, IDEs, etc.

# Liberar caché
sudo sync
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

#### Solución 3: Usar Swap

```bash
# Crear archivo swap de 8GB
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Verificar
free -h
```

#### Solución 4: Usar Google Colab

Si tu hardware es muy limitado, usa Colab para offloading:

```python
# Ver docs/04-USO-AVANZADO.md
# Sección: Integración con Google Colab
```

---

## Timeout en simulaciones

### Síntomas

```
❌ Timeout: Simulación excedió 900 segundos
```

### Diagnóstico

```bash
# Ver cuánto tardó
grep "Timeout" logs/sistema_a2a.log
```

### Soluciones

#### Solución 1: Aumentar Timeout

```python
# Editar config/settings.py
# Línea ~49

# Aumentar timeout (en segundos)
SIMULATION_TIMEOUT = 1800  # 30 minutos
```

#### Solución 2: Simplificar Simulación

```bash
# Reducir número de nodos
python main.py --task "Simular AODV con 20 nodos"  # En lugar de 100

# Reducir duración
python main.py --task "Simular AODV con 50 nodos durante 100 segundos"  # En lugar de 300
```

#### Solución 3: Optimizar NS-3

```bash
cd ~/tesis-a2a/ns-allinone-3.43/ns-3.43

# Recompilar en modo optimizado
./ns3 configure --enable-python-bindings --build-profile=optimized
./ns3 build
```

---

## Modelos no encontrados

### Síntomas

```
Error: model 'llama3.1:8b' not found
```

### Diagnóstico

```bash
# Listar modelos instalados
ollama list
```

### Soluciones

#### Solución 1: Descargar Modelos

```bash
# Descargar modelos necesarios
ollama pull llama3.1:8b
ollama pull deepseek-coder-v2:16b
ollama pull nomic-embed-text

# Verificar
ollama list
```

#### Solución 2: Verificar Nombres

```bash
# Ver nombres exactos de modelos instalados
ollama list

# Ajustar en config/settings.py si el nombre es diferente
# Por ejemplo, si aparece como "llama3.1:latest"
MODEL_REASONING = "llama3.1:latest"
```

---

## Errores de dependencias

### Síntomas

```
ModuleNotFoundError: No module named 'langgraph'
ImportError: cannot import name 'ChatOllama'
```

### Diagnóstico

```bash
# Verificar entorno virtual
which python
# Debe mostrar: /ruta/a/sistema-a2a-tesis/venv/bin/python

# Listar paquetes instalados
pip list | grep -E "langgraph|langchain|chromadb"
```

### Soluciones

#### Solución 1: Activar Entorno Virtual

```bash
# Asegurarse de estar en el entorno virtual
source venv/bin/activate

# Verificar
which python
# Debe mostrar la ruta del venv
```

#### Solución 2: Reinstalar Dependencias

```bash
# Activar entorno
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt

# Verificar
pip list
```

#### Solución 3: Crear Nuevo Entorno

```bash
# Eliminar entorno anterior
rm -rf venv

# Crear nuevo
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Problemas con ChromaDB

### Síntomas

```
Error: ChromaDB connection failed
sqlite3.OperationalError: database is locked
```

### Soluciones

#### Solución 1: Eliminar Base de Datos Corrupta

```bash
# Eliminar base de datos
rm -rf data/vector_db/*

# El sistema la recreará automáticamente
```

#### Solución 2: Cerrar Otros Procesos

```bash
# Ver procesos usando ChromaDB
lsof data/vector_db/chroma.sqlite3

# Cerrar procesos si es necesario
kill -9 <PID>
```

---

## Problemas con Gráficos

### Síntomas

```
Error: No display found
matplotlib.pyplot error
```

### Soluciones

#### Solución 1: Configurar Backend

```python
# Añadir al inicio de agents/visualizer.py
import matplotlib
matplotlib.use('Agg')  # Backend sin display
import matplotlib.pyplot as plt
```

#### Solución 2: Instalar Dependencias

```bash
sudo apt install python3-tk
pip install matplotlib --upgrade
```

---

## Comandos de Diagnóstico

### Verificación Completa

```bash
# Ejecutar verificador del sistema
python scripts/check_system.py
```

### Ver Logs Detallados

```bash
# Ver últimas 50 líneas de logs
tail -50 logs/sistema_a2a.log

# Ver solo errores
grep "ERROR" logs/sistema_a2a.log

# Ver logs en tiempo real
tail -f logs/sistema_a2a.log
```

### Verificar Componentes Individuales

```bash
# Ollama
curl http://localhost:11434/api/tags

# NS-3
cd ~/tesis-a2a/ns-allinone-3.43/ns-3.43
./ns3 run hello-simulator

# Python
python3 -c "import sys; print(sys.version)"

# Dependencias
pip list | grep -E "langgraph|langchain"
```

---

## Resetear el Sistema

### Reset Completo

```bash
# 1. Detener Ollama
pkill ollama

# 2. Limpiar datos temporales
rm -rf logs/*
rm -rf data/vector_db/*
rm -rf simulations/results/*
rm -rf simulations/plots/*

# 3. Eliminar entorno virtual
rm -rf venv

# 4. Reinstalar
./scripts/install.sh
```

### Reset Parcial (Solo Datos)

```bash
# Limpiar solo resultados
rm -rf simulations/results/*
rm -rf simulations/plots/*
rm -rf logs/*

# Mantener configuración y código
```

---

## Obtener Ayuda

### Información para Reportar Problemas

Cuando pidas ayuda, incluye:

```bash
# 1. Versión del sistema
cat PROYECTO-COMPLETO.txt | head -5

# 2. Salida del verificador
python scripts/check_system.py > diagnostico.txt

# 3. Últimos logs
tail -100 logs/sistema_a2a.log > ultimos_logs.txt

# 4. Configuración
cat config/settings.py > mi_config.txt

# 5. Comando que falló
# Copia el comando exacto que ejecutaste
```

### Recursos Adicionales

- **Documentación NS-3**: https://www.nsnam.org/documentation/
- **Documentación Ollama**: https://ollama.com/docs
- **Documentación LangGraph**: https://langchain-ai.github.io/langgraph/

---

## Problemas No Resueltos

Si ninguna solución funciona:

1. **Revisa los logs**: `logs/sistema_a2a.log`
2. **Ejecuta diagnóstico**: `python scripts/check_system.py`
3. **Simplifica la tarea**: Prueba con algo más simple
4. **Contacta al administrador**: Con la información de diagnóstico

---

**¿Encontraste un problema nuevo?** Documéntalo y compártelo con el grupo para ayudar a otros.
