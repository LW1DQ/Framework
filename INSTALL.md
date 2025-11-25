# Guía de Instalación: Sistema AGENTES A2A v1.4

Esta guía detalla el proceso de instalación del sistema en entornos **Ubuntu Linux** (nativo o WSL2) y **Windows**.

---

## 📋 Requisitos del Sistema

- **Sistema Operativo**: 
  - Ubuntu 20.04 LTS / 22.04 LTS (Recomendado)
  - Windows 10/11 (vía WSL2 o nativo con limitaciones)
- **Python**: 3.8 o superior
- **RAM**: 8GB mínimo (16GB recomendado para LLMs locales)
- **Espacio en Disco**: 10GB (incluyendo modelos LLM y NS-3)

---

## 🐧 Instalación en Ubuntu (Recomendado)

### 1. Preparar el Sistema

Actualiza los repositorios e instala las dependencias del sistema necesarias para Python y NS-3.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git build-essential cmake
```

### 2. Instalar NS-3 (Simulador de Redes)

El sistema requiere NS-3 para ejecutar las simulaciones.

```bash
# Descargar e instalar dependencias de NS-3
sudo apt install -y g++ python3-dev pkg-config sqlite3 python3-setuptools
sudo apt install -y qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools

# Descargar NS-3 (versión recomendada 3.35 o superior)
cd ~
wget https://www.nsnam.org/release/ns-allinone-3.35.tar.bz2
tar xjf ns-allinone-3.35.tar.bz2
cd ns-allinone-3.35/ns-3.35

# Configurar y compilar
./waf configure --enable-examples --enable-tests
./waf build
```

> **Nota**: Anota la ruta de instalación (ej. `/home/usuario/ns-allinone-3.35/ns-3.35`), la necesitarás más adelante.

### 3. Instalar Ollama (LLM Local)

Ollama es necesario para ejecutar los modelos de lenguaje localmente.

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Una vez instalado, descarga los modelos necesarios:

```bash
ollama pull llama3
ollama pull qwen2.5-coder
```

### 4. Instalar Sistema A2A

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/sistema-a2a.git
cd sistema-a2a

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configuración

Edita el archivo `config/settings.py` para apuntar a tu instalación de NS-3.

```bash
nano config/settings.py
```

Busca la variable `NS3_ROOT` y actualízala:

```python
# config/settings.py
from pathlib import Path

# Actualiza esta ruta
NS3_ROOT = Path("/home/tu-usuario/ns-allinone-3.35/ns-3.35")
```

### 6. Verificación

Ejecuta el script de integración para verificar que todo funciona:

```bash
python test_integration.py
```

---

## 🪟 Instalación en Windows

### Opción A: WSL2 (Recomendada)

Sigue los pasos de la instalación de Ubuntu dentro de tu terminal WSL2. Esta es la forma más robusta de correr NS-3 en Windows.

### Opción B: Nativa

1.  **Instalar Python**: Descarga e instala Python 3.10+ desde python.org.
2.  **Instalar NS-3**: NS-3 en Windows nativo es complejo y requiere Visual Studio. Se recomienda encarecidamente usar WSL2. Si ya tienes NS-3 compilado, configura `NS3_ROOT` en `config/settings.py`.
3.  **Instalar Ollama**: Descarga el instalador de Windows desde [ollama.com](https://ollama.com).
4.  **Instalar Proyecto**:
    ```powershell
    git clone https://github.com/tu-usuario/sistema-a2a.git
    cd sistema-a2a
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

---

## 🔧 Solución de Problemas

### Error: `ns3 module not found`
Asegúrate de que `NS3_ROOT` en `config/settings.py` apunte a la carpeta que contiene el script `waf` y la carpeta `build`.

### Error: `Ollama connection refused`
Asegúrate de que Ollama esté corriendo. En una terminal separada ejecuta `ollama serve`.

### Error: `torch not found`
Si tienes problemas con PyTorch, instálalo manualmente según tu sistema (CPU o CUDA):
[https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)
