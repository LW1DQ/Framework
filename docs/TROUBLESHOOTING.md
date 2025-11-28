# 🔧 Troubleshooting - Sistema A2A

Guía de solución de problemas comunes del Sistema Multi-Agente A2A.

---

## 📋 Tabla de Contenidos

1. [Problemas de Instalación](#problemas-de-instalación)
2. [Problemas de Ejecución](#problemas-de-ejecución)
3. [Problemas con NS-3](#problemas-con-ns-3)
4. [Problemas con Ollama](#problemas-con-ollama)
5. [Problemas con Dependencias](#problemas-con-dependencias)
6. [Problemas de Rendimiento](#problemas-de-rendimiento)

---

## 🔧 Problemas de Instalación

### Error: "No module named 'langgraph'"

**Síntoma:**
```
ModuleNotFoundError: No module named 'langgraph'
```

**Solución:**
```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

---

### Error: "Python version incompatible"

**Síntoma:**
```
ERROR: Package requires Python >=3.10
```

**Solución:**
```bash
# Verificar versión de Python
python --version

# Si es < 3.10, instalar Python 3.10+
# Ubuntu:
sudo apt install python3.10 python3.10-venv

# Crear nuevo entorno virtual
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Problemas de Ejecución

### Error: "Ollama no responde"

**Síntoma:**
```
❌ No se puede conectar a Ollama: Connection refused
```

**Solución:**
```bash
# 1. Verificar que Ollama esté corriendo
ollama list

# 2. Si no está corriendo, iniciar Ollama
ollama serve

# 3. En otra terminal, verificar modelos
ollama list

# 4. Si faltan modelos, descargarlos
ollama pull llama3.1:8b
# 4. Si faltan modelos, descargarlos
ollama pull llama3.1:8b
# deepseek-coder-v2:16b ya no es el default por consumo de recursos
```

**Verificación:**
```bash
# Test de conexión
curl http://localhost:11434/api/tags
```

---

### Error: "NS-3 no encontrado"

**Síntoma:**
```
❌ NS-3 no encontrado en: /home/usuario/ns-3-dev
```

**Solución:**
```bash
# 1. Verificar ruta de NS-3
ls ~/ns-3-dev

# 2. Si no existe, instalar NS-3
cd ~
git clone https://gitlab.com/nsnam/ns-3-dev.git
cd ns-3-dev
./ns3 configure --enable-examples
./ns3 build

# 3. Actualizar config/settings.py
nano config/settings.py
# Cambiar NS3_ROOT a la ruta correcta
```

---

### Error: "Simulación timeout"

**Síntoma:**
```
⚠️ Timeout: Simulación excedió 900 segundos
```

**Solución:**
```bash
# Opción 1: Aumentar timeout en config/settings.py
nano config/settings.py
# Cambiar SIMULATION_TIMEOUT = 1800  # 30 minutos

# Opción 2: Reducir complejidad de simulación
# - Menos nodos
# - Menor tiempo de simulación
# - Área más pequeña
```

---

### Error: "Código inválido tras múltiples intentos"

**Síntoma:**
```
⚠️ Límite de iteraciones alcanzado (5)
❌ Código inválido: Falta función main()
```

**Solución:**
```bash
# 1. Revisar logs detallados
cat logs/sistema_a2a.log

# 2. Verificar que Ollama tenga los modelos correctos
ollama list

# 3. Intentar con tarea más simple
python main.py
# Tarea: "Simular AODV con 5 nodos en área pequeña"

# 4. Si persiste, limpiar memoria episódica
python -c "from utils.memory import memory; memory.clear()"

---

### Error: "Validation Failed"

**Síntoma:**
```
❌ Validación falló: Error de sintaxis en línea 10
```

**Solución:**
El sistema ahora valida el código antes de ejecutarlo.
1. **Revisar el error específico**: El mensaje indica la línea exacta.
2. **Verificar imports**: Asegurar que `ns.core`, `ns.network` estén presentes.
3. **Verificar estructura**: Debe existir `def main()` o `if __name__ == "__main__"`.

---

### Error: "CodeGenerationError"

**Síntoma:**
```
CodeGenerationError: Error en generación LLM
```

**Solución:**
1. **Verificar Ollama**: Asegurar que el modelo `llama3.1:8b` esté cargado.
2. **Recursos**: Verificar RAM disponible.
3. **Logs**: Revisar `logs/sistema_a2a.log` para el traceback completo.
```

---

## 🔬 Problemas con NS-3

### Error: "ImportError: No module named 'ns'"

**Síntoma:**
```
ImportError: No module named 'ns'
```

**Solución:**
```bash
# 1. Verificar que NS-3 esté compilado con Python bindings
cd ~/ns-3-dev
./ns3 configure --enable-python-bindings
./ns3 build

# 2. Verificar que el path sea correcto
python3 -c "import sys; sys.path.insert(0, 'build/lib/python3'); import ns.core; print('OK')"

# 3. Si falla, recompilar NS-3
./ns3 clean
./ns3 configure --enable-python-bindings --enable-examples
./ns3 build
```

---

### Error: "AttributeError: module 'ns' has no attribute 'aodv'"

**Síntoma:**
```
AttributeError: module 'ns' has no attribute 'aodv'
```

**Solución:**
```bash
# AODV es un módulo opcional en NS-3
cd ~/ns-3-dev

# Verificar que esté habilitado
./ns3 configure --enable-modules=aodv,olsr,dsdv
./ns3 build

# Verificar instalación
python3 -c "import sys; sys.path.insert(0, 'build/lib/python3'); import ns.aodv; print('AODV OK')"
```

---

### Error: "Simulación no genera archivos PCAP"

**Síntoma:**
```
⚠️ No se encontraron archivos PCAP (patrón: simulacion-*.pcap)
```

**Solución:**

1. Verificar que el código generado incluya:
```python
phy.EnablePcapAll("simulacion", True)
```

2. Verificar permisos de escritura:
```bash
ls -la ~/ns-3-dev/
# Debe tener permisos de escritura
```

3. Ejecutar simulación manualmente para debug:
```bash
cd ~/ns-3-dev
python3 scratch/tesis_sim_YYYYMMDD_HHMMSS.py
ls -la simulacion-*.pcap
```

---

## 🤖 Problemas con Ollama

### Error: "Model not found"

**Síntoma:**
```
Error: model 'llama3.1:8b' not found
```

**Solución:**
```bash
# Descargar modelo (Default actual)
ollama pull llama3.1:8b

# Verificar
ollama list

# Si el modelo es muy grande y falla, usar versión más pequeña
ollama pull llama3.1:7b
# Actualizar config/settings.py con el nuevo modelo
```

---

### Error: "Ollama responde muy lento"

**Síntoma:**
- Respuestas tardan >2 minutos
- CPU al 100%

**Solución:**
```bash
# 1. Verificar recursos del sistema
htop

# 2. Usar modelo más pequeño
ollama pull llama3.1:7b

# 3. Ajustar configuración en config/settings.py
MODEL_REASONING = "llama3.1:7b"  # En lugar de 8b

# 4. Aumentar timeout de LLM
LLM_TIMEOUT = 300  # 5 minutos
```

---

## 📦 Problemas con Dependencias

### Error: "tshark not found"

**Síntoma:**
```
⚠️ tshark no está disponible en el sistema
```

**Solución:**
```bash
# Ubuntu/Debian
sudo apt install tshark wireshark-common

# Fedora
sudo dnf install wireshark-cli

# macOS
brew install wireshark

# Verificar instalación
tshark --version
```

---

### Error: "ChromaDB error"

**Síntoma:**
```
Error: Could not connect to ChromaDB
```

**Solución:**
```bash
# Reinstalar ChromaDB
pip uninstall chromadb
pip install chromadb==0.5.5

# Limpiar base de datos corrupta
rm -rf data/vector_db/
mkdir -p data/vector_db/

# Reintentar
python main.py
```

---

### Error: "scikit-learn not found"

**Síntoma:**
```
⚠️ scikit-learn no disponible. Memoria episódica usará búsqueda simple.
```

**Solución:**
```bash
# Instalar scikit-learn
pip install scikit-learn>=1.3.0

# Verificar
python -c "from sklearn.feature_extraction.text import TfidfVectorizer; print('OK')"
```

---

## ⚡ Problemas de Rendimiento

### Sistema muy lento

**Síntomas:**
- Cada agente tarda >5 minutos
- Uso de CPU constante al 100%

**Soluciones:**

1. **Reducir complejidad de tareas:**
```python
# En lugar de:
"Simular MANET con AODV, 100 nodos, área 2000x2000m, 500 segundos"

# Usar:
"Simular MANET con AODV, 20 nodos, área 500x500m, 100 segundos"
```

2. **Usar modelos LLM más pequeños:**
```python
# config/settings.py
MODEL_REASONING = "llama3.1:7b"  # En lugar de 8b
MODEL_CODING = "deepseek-coder:6.7b"  # En lugar de 16b
```

3. **Deshabilitar búsqueda de papers:**
```python
# Si no necesitas búsqueda académica, comentar en researcher.py
# papers_ss = search_semantic_scholar(...)
papers_ss = []
```

4. **Aumentar recursos del sistema:**
- Cerrar aplicaciones innecesarias
- Aumentar RAM disponible
- Usar SSD en lugar de HDD

---

### Memoria insuficiente

**Síntoma:**
```
MemoryError: Unable to allocate array
```

**Solución:**
```bash
# 1. Verificar uso de memoria
free -h

# 2. Limpiar caché
sudo sync; echo 3 | sudo tee /proc/sys/vm/drop_caches

# 3. Reducir tamaño de batch en DRL
# En agents/ns3_ai_integration.py
BATCH_SIZE = 16  # En lugar de 64

# 4. Limitar número de papers en memoria
# En agents/researcher.py
SEMANTIC_SCHOLAR_MAX_RESULTS = 5  # En lugar de 10
```

---

## 🔍 Debugging Avanzado

### Habilitar logs detallados

```bash
# Editar config/settings.py
LOG_LEVEL = "DEBUG"  # En lugar de "INFO"

# Ejecutar y revisar logs
python main.py
tail -f logs/sistema_a2a.log
```

### Ejecutar tests

```bash
# Tests unitarios
pytest tests/test_agents.py -v

# Tests con cobertura
pytest tests/ --cov=agents --cov=utils --cov-report=html

# Ver reporte
open htmlcov/index.html
```

### Verificar estado del sistema

```bash
# Script de verificación
python scripts/check_system.py

# O manualmente:
python -c "from config.settings import validate_configuration; print(validate_configuration())"
```

---

## 📞 Obtener Ayuda

Si ninguna de estas soluciones funciona:

1. **Revisar logs completos:**
```bash
cat logs/sistema_a2a.log | grep ERROR
```

2. **Ejecutar test de integración:**
```bash
python test_integration.py
```

3. **Verificar versiones:**
```bash
python --version
pip list | grep -E "langgraph|langchain|ollama"
```

4. **Crear issue en GitHub** con:
   - Descripción del problema
   - Logs relevantes
   - Versiones de software
   - Sistema operativo

---

## ✅ Checklist de Verificación

Antes de reportar un problema, verifica:

- [ ] Python >= 3.10 instalado
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Ollama corriendo (`ollama list`)
- [ ] Modelos descargados (`llama3.1:8b`, `deepseek-coder-v2:16b`)
- [ ] NS-3 instalado y compilado
- [ ] Ruta de NS-3 correcta en `config/settings.py`
- [ ] Permisos de escritura en directorios
- [ ] Espacio en disco suficiente (>10GB)

---

**Última actualización:** Noviembre 2025  
**Versión:** 1.4
