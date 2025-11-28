# 📦 Guía de Instalación Completa (Paso a Paso)

Esta guía está diseñada para usuarios nuevos que desean instalar el Sistema A2A desde cero en un sistema Linux (Ubuntu/Debian).

---

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#1-requisitos-previos)
2. [Paso 1: Preparación del Sistema](#2-paso-1-preparación-del-sistema)
3. [Paso 2: Instalación de Python](#3-paso-2-instalación-de-python)
4. [Paso 3: Instalación del Framework](#4-paso-3-instalación-del-framework)
5. [Paso 4: Instalación de NS-3](#5-paso-4-instalación-de-ns-3)
6. [Paso 5: Configuración de IA (Ollama)](#6-paso-5-configuración-de-ia-ollama)
7. [Paso 6: Verificación](#7-paso-6-verificación)

---

## 1. Requisitos Previos

Antes de comenzar, asegúrate de tener:
- **Sistema Operativo**: Ubuntu 22.04 LTS (Recomendado) o superior.
- **Acceso a Internet**: Para descargar paquetes y modelos.
- **Permisos de Administrador (sudo)**: Necesarios para instalar dependencias.
- **Espacio en Disco**: Al menos 20 GB libres.

---

## 2. Paso 1: Preparación del Sistema

Abre una terminal (`Ctrl+Alt+T`) y ejecuta los siguientes comandos para actualizar tu sistema e instalar herramientas básicas:

```bash
# 1. Actualizar lista de paquetes
sudo apt update

# 2. Actualizar paquetes instalados
sudo apt upgrade -y

# 3. Instalar herramientas esenciales
sudo apt install -y git curl wget build-essential htop
```

---

## 3. Paso 2: Instalación de Python

El sistema requiere Python 3.10 o superior.

```bash
# 1. Verificar versión actual
python3 --version

# 2. Si es menor a 3.10, instalar Python 3.10
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3.10-dev
```

---

## 4. Paso 3: Instalación del Framework

Ahora descargaremos y configuraremos el código del Sistema A2A.

```bash
# 1. Clonar el repositorio (descargar código)
cd ~
git clone https://github.com/LW1DQ/Framework.git

# 2. Entrar al directorio
cd Framework

# 3. Crear un entorno virtual (para aislar las librerías)
python3.10 -m venv venv

# 4. Activar el entorno virtual
source venv/bin/activate
# (Verás que tu terminal ahora dice (venv))

# 5. Instalar las dependencias del proyecto
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. Paso 4: Instalación de NS-3

NS-3 es el simulador de redes. Esta es la parte que más tiempo toma (15-30 minutos).

```bash
# 1. Instalar dependencias de NS-3
sudo apt install -y g++ python3-dev cmake libsqlite3-dev libboost-all-dev libssl-dev libxml2-dev libgtk-3-dev wireshark tcpdump

# 2. Descargar NS-3 (versión 3.45)
cd ~
wget https://www.nsnam.org/releases/ns-3.45.tar.bz2
tar xjf ns-3.45.tar.bz2

# 3. Renombrar carpeta para facilitar acceso
mv ns-3.45 ns3
cd ns3

# 4. Configurar NS-3 (habilitando ejemplos y tests)
./ns3 configure --enable-examples --enable-tests --build-profile=optimized

# 5. Compilar (esto tardará varios minutos)
./ns3 build
```

**Nota**: Si ves mensajes de "Build finished successfully", todo salió bien.

---

## 6. Paso 5: Configuración de IA (Ollama)

Ollama es el motor que ejecuta los modelos de Inteligencia Artificial localmente.

```bash
# 1. Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Iniciar el servicio (si no se inició automáticamente)
sudo systemctl start ollama

# 3. Descargar el modelo Llama 3.1 (8B)
# Este es el cerebro del sistema. La descarga son ~4.7 GB.
ollama pull llama3.1:8b
```

---

## 7. Paso 6: Verificación

Vamos a comprobar que todo funciona correctamente.

```bash
# 1. Volver al directorio del Framework
cd ~/Framework

# 2. Asegurarse de que el entorno virtual esté activo
source venv/bin/activate

# 3. Configurar la ruta de NS-3 en el sistema
# Edita el archivo de configuración
nano config/settings.py

# Busca la línea que dice:
# NS3_ROOT = Path("/home/usuario/ns-3-dev")
# Y cámbiala por tu ruta real, por ejemplo:
# NS3_ROOT = Path("/home/tu_usuario/ns3")
# (Presiona Ctrl+O para guardar y Ctrl+X para salir)

# 4. Ejecutar script de verificación
python verify-system-complete.py
```

Si ves un mensaje en verde diciendo **"VERIFICACIÓN COMPLETA: 100%"**, ¡felicidades! Has instalado el sistema correctamente.

---

## 🚀 Primeros Pasos

Para ejecutar tu primer experimento:

```bash
python main.py --task "Comparar protocolo AODV y OLSR en una red de 20 nodos"
```

El sistema comenzará a trabajar: buscará información, generará el código de simulación, lo ejecutará en NS-3 y te mostrará los resultados.

---

## 🆘 ¿Problemas?

Si encuentras algún error:
1. Revisa la guía de [Solución de Problemas](TROUBLESHOOTING.md).
2. Asegúrate de haber activado el entorno virtual (`source venv/bin/activate`).
3. Verifica que Ollama esté corriendo (`ollama list`).
