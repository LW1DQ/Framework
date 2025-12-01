# 🚀 A2A Framework - Instalador de Sandbox

Este directorio contiene las herramientas necesarias para desplegar un entorno de investigación completo (Sandbox) en cualquier máquina Ubuntu/Debian.

## 📋 Contenido

- `install_a2a.sh`: Script maestro de instalación.
- `docs/`: Documentación completa del proyecto (Manual de Usuario, Guías, etc.).

## 🛠️ Instrucciones de Uso

Para instalar el framework en una nueva máquina:

1. **Descargar el script** (si no has clonado el repo):
   ```bash
   wget https://raw.githubusercontent.com/LW1DQ/Framework/main/sandbox_install/install_a2a.sh
   chmod +x install_a2a.sh
   ```

2. **Ejecutar el instalador**:
   ```bash
   ./install_a2a.sh
   ```

   El script realizará automáticamente:
   - Verificación e instalación de dependencias del sistema.
   - Creación de la carpeta `~/A2A_Research_Sandbox`.
   - Descarga del código fuente más reciente.
   - Instalación/Detección del simulador NS-3.
   - Configuración del entorno Python.

3. **Iniciar una investigación**:
   ```bash
   cd ~/A2A_Research_Sandbox
   ./launch.sh --task "Comparar protocolos AODV y OLSR"
   ```

## 📚 Documentación

Toda la documentación necesaria se encuentra en la carpeta `docs/` dentro de tu Sandbox instalado.

- **Manual de Usuario**: `docs/MANUAL_USUARIO.md`
- **Guía de Contribución**: `docs/CONTRIBUTING.md`
