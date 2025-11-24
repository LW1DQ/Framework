# 🐧 Instrucciones para Ubuntu - Sistema A2A v1.3

## Archivo: sistema-a2a-v1.3-ubuntu.zip

---

## 📋 Contenido del ZIP

El archivo `sistema-a2a-v1.3-ubuntu.zip` contiene la versión final completa del Sistema A2A v1.3.

---

## 🚀 Instalación en Ubuntu

### Paso 1: Transferir el Archivo

Transfiere `sistema-a2a-v1.3-ubuntu.zip` a tu máquina Ubuntu.

**Opciones:**
- USB
- SCP: `scp sistema-a2a-v1.3-ubuntu.zip usuario@ubuntu:/home/usuario/`
- Descarga directa

### Paso 2: Descomprimir

```bash
# Navegar al directorio donde está el ZIP
cd ~/

# Descomprimir
unzip sistema-a2a-v1.3-ubuntu.zip -d sistema-a2a-v1.3

# Navegar al directorio
cd sistema-a2a-v1.3
```

### Paso 3: Verificar Contenido

```bash
# Listar archivos
ls -la

# Deberías ver:
# - agents/
# - config/
# - utils/
# - docs/
# - main.py
# - supervisor.py
# - EMPIEZA-AQUI.txt
# - etc.
```

### Paso 4: Leer Documentación de Inicio

```bash
cat EMPIEZA-AQUI.txt
```

---

## 🔧 Instalación de Dependencias

### 1. Actualizar Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Instalar Python 3.10+

```bash
# Verificar versión
python3 --version

# Si es menor a 3.10, instalar:
sudo apt install python3.10 python3.10-venv python3-pip -y
```

### 3. Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar
source venv/bin/activate

# Verificar
which python
# Debe mostrar: /home/usuario/sistema-a2a-v1.3/venv/bin/python
```

### 4. Instalar Dependencias Python

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

---

## 🛠️ Instalación de NS-3

### Opción 1: Script Automático

```bash
# Dar permisos de ejecución
chmod +x install.sh

# Ejecutar (puede tardar 30-60 minutos)
./install.sh
```

### Opción 2: Manual

Seguir la guía completa:

```bash
cat docs/INSTALACION-COMPLETA.md
```

**Resumen:**

```bash
# Instalar dependencias
sudo apt install g++ python3-dev pkg-config sqlite3 \
  cmake ninja-build ccache -y

# Clonar NS-3
cd ~/
git clone https://gitlab.com/nsnam/ns-3-dev.git
cd ns-3-dev

# Configurar
./ns3 configure --enable-examples --enable-tests

# Compilar (tarda ~30 minutos)
./ns3 build

# Verificar
./ns3 --version
```

---

## 🤖 Instalación de Ollama

### 1. Instalar Ollama

```bash
# Descargar e instalar
curl -fsSL https://ollama.ai/install.sh | sh

# Verificar
ollama --version
```

### 2. Descargar Modelos

```bash
# Modelo para razonamiento
ollama pull llama3.1:8b

# Modelo para código
ollama pull deepseek-coder-v2:16b

# Verificar
ollama list
```

---

## 🧪 Verificación de Instalación

### 1. Test de Integración

```bash
# Activar entorno virtual (si no está activo)
source venv/bin/activate

# Ejecutar test
python test_integration.py
```

**Resultado Esperado:**
```
✅ PASS - Estructura de Archivos
✅ PASS - Imports
✅ PASS - Utilidades Estadísticas
✅ PASS - Supervisor
```

### 2. Verificar NS-3

```bash
# Verificar que NS-3 esté accesible
python3 -c "import sys; sys.path.insert(0, '~/ns-3-dev/build/lib/python3'); import ns.core; print('✅ NS-3 OK')"
```

### 3. Verificar Ollama

```bash
# Verificar que Ollama esté corriendo
curl http://localhost:11434/api/tags

# Debe retornar lista de modelos
```

---

## 🚀 Primera Ejecución

### 1. Configurar Rutas

Editar `config/settings.py`:

```bash
nano config/settings.py
```

Verificar/actualizar:
```python
# Ruta a NS-3
NS3_ROOT = Path.home() / "ns-3-dev"

# Ollama
OLLAMA_BASE_URL = "http://localhost:11434"
```

### 2. Ejecutar Primera Simulación

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar
python main.py
```

**Tarea de Ejemplo:**
```
Simular una red MANET con protocolo AODV, 20 nodos móviles,
área de 1000x1000 metros, durante 200 segundos
```

### 3. Verificar Resultados

```bash
# Ver archivos PCAP generados
ls -lh simulations/results/*.pcap

# Ver reporte estadístico
cat simulations/analysis/statistical_report_*.md

# Ver dashboard (si tienes GUI)
xdg-open simulations/visualizations/dashboard.html
```

---

## 📚 Documentación

### Documentos Esenciales

```bash
# Punto de entrada
cat EMPIEZA-AQUI.txt

# Inicio rápido
cat QUICK-START-v1.3.txt

# README completo
cat README.md

# Índice de documentación
cat INDICE-DOCUMENTACION.md
```

### Documentación Técnica

```bash
# Guía de uso completa
cat docs/GUIA-USO-NUEVAS-FUNCIONALIDADES.md

# Instalación NS-3
cat docs/INSTALACION-COMPLETA.md

# Instalación ns3-ai (opcional)
cat docs/INSTALACION-NS3-AI.md

# Flujo del sistema
cat docs/FLUJO-ACTUALIZADO-v1.3.txt
```

---

## 🔧 Configuración Adicional

### Permisos de Ejecución

```bash
# Dar permisos a scripts
chmod +x install.sh
chmod +x scripts/*.sh

# Verificar
ls -l *.sh
```

### Variables de Entorno (Opcional)

```bash
# Añadir a ~/.bashrc
echo 'export NS3_ROOT=~/ns-3-dev' >> ~/.bashrc
echo 'export SISTEMA_A2A=~/sistema-a2a-v1.3' >> ~/.bashrc

# Recargar
source ~/.bashrc
```

---

## 🆘 Troubleshooting

### Problema: Python no encuentra NS-3

**Solución:**
```bash
# Verificar ruta en config/settings.py
nano config/settings.py

# Actualizar NS3_ROOT a la ruta correcta
NS3_ROOT = Path.home() / "ns-3-dev"
```

### Problema: Ollama no responde

**Solución:**
```bash
# Verificar que Ollama esté corriendo
systemctl status ollama

# Si no está corriendo, iniciar
ollama serve &

# Verificar
curl http://localhost:11434/api/tags
```

### Problema: Error de permisos

**Solución:**
```bash
# Dar permisos al directorio
chmod -R 755 ~/sistema-a2a-v1.3

# Dar permisos a scripts
chmod +x *.sh
```

### Problema: Dependencias faltantes

**Solución:**
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall

# Verificar
pip list
```

---

## 📊 Estructura del Proyecto

```
sistema-a2a-v1.3/
├── agents/                 # 8 agentes especializados
├── config/                 # Configuración
├── utils/                  # Utilidades
├── docs/                   # Documentación
├── data/                   # Datos de investigación
├── examples/               # Ejemplos
├── scripts/                # Scripts auxiliares
├── tests/                  # Tests
├── simulations/            # Resultados (vacío inicialmente)
├── logs/                   # Logs (vacío inicialmente)
├── main.py                 # Punto de entrada
├── supervisor.py           # Orquestador
├── requirements.txt        # Dependencias
├── install.sh              # Instalación automática
└── EMPIEZA-AQUI.txt       # Guía de inicio
```

---

## 🎓 Para Tesis Doctoral

El sistema está listo para:

- ✅ Simulaciones reproducibles
- ✅ Análisis estadístico riguroso
- ✅ Captura de trazas PCAP
- ✅ Cálculo de overhead
- ✅ Optimización con DRL (opcional)

---

## 📞 Soporte

Para más ayuda:

1. **Documentación**: Consultar `INDICE-DOCUMENTACION.md`
2. **Tests**: Ejecutar `python test_integration.py`
3. **Guías**: Leer archivos en `docs/`

---

## ✅ Checklist de Instalación

- [ ] Archivo ZIP transferido a Ubuntu
- [ ] Archivo descomprimido
- [ ] Python 3.10+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias Python instaladas
- [ ] NS-3 instalado y compilado
- [ ] Ollama instalado
- [ ] Modelos LLM descargados
- [ ] Test de integración pasado
- [ ] Primera simulación ejecutada exitosamente

---

## 🎉 ¡Listo!

Una vez completados todos los pasos, el sistema estará listo para usar en tu tesis doctoral.

**¡Éxito en tu investigación!** 🎓🚀

---

**Versión**: 1.3  
**Fecha**: 24 de Noviembre de 2025  
**Sistema**: Ubuntu 20.04+ / 22.04+
