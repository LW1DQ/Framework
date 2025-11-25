# 📤 Instrucciones para Subir a GitHub

## Guía Paso a Paso para Subir el Sistema A2A v1.3 a GitHub

---

## 📋 Preparación Previa

### ✅ Archivos Preparados

Los siguientes archivos están listos para subir:

**Documentación Principal:**
- ✅ `README-GITHUB.md` → Renombrar a `README.md` antes de subir
- ✅ `GUIA-INVESTIGADORES-REDES.md` (55 KB)
- ✅ `INSTRUCCIONES-UBUNTU.md`
- ✅ `INDICE-GUIA-INVESTIGADORES.md`
- ✅ `LEEME-GUIA-INVESTIGADORES.md`

**Archivos de Configuración:**
- ✅ `.gitignore` (creado)
- ✅ `LICENSE` (MIT License)

**Código del Sistema:**
- ✅ `sistema-a2a-v1.3-final/` (carpeta completa)

**Paquete de Exportación:**
- ✅ `sistema-a2a-v1.3-ubuntu.zip`

---

## 🚀 Opción 1: Subir desde la Interfaz Web de GitHub (Más Fácil)

### Paso 1: Crear Repositorio en GitHub

1. Ve a https://github.com
2. Inicia sesión con tu cuenta
3. Click en el botón **"+"** (arriba derecha) → **"New repository"**
4. Configura el repositorio:
   - **Repository name**: `sistema-a2a` (o el nombre que prefieras)
   - **Description**: `Framework Multi-Agente para Simulación de Redes MANET/VANET con NS-3`
   - **Visibility**: 
     - ✅ **Public** (recomendado para tesis)
     - ⚪ Private (si prefieres mantenerlo privado)
   - **NO marques** "Initialize this repository with a README"
   - **NO añadas** .gitignore ni license (ya los tenemos)
5. Click en **"Create repository"**

### Paso 2: Preparar Archivos Localmente

Abre PowerShell o CMD en la carpeta del proyecto:

```powershell
# Renombrar README para GitHub
Move-Item README-GITHUB.md README.md -Force

# Verificar que todo esté listo
dir
```

### Paso 3: Inicializar Git Local

```bash
# Inicializar repositorio Git
git init

# Configurar tu identidad (si no lo has hecho antes)
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"

# Añadir todos los archivos
git add .

# Verificar qué se va a subir
git status

# Crear primer commit
git commit -m "Initial commit: Sistema A2A v1.3 con documentación completa"
```

### Paso 4: Conectar con GitHub

```bash
# Conectar con tu repositorio (reemplaza TU-USUARIO y TU-REPO)
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git

# Verificar conexión
git remote -v
```

### Paso 5: Subir a GitHub

```bash
# Subir archivos (primera vez)
git branch -M main
git push -u origin main
```

**Si te pide autenticación:**
- Usuario: tu nombre de usuario de GitHub
- Contraseña: usa un **Personal Access Token** (no tu contraseña)

### Paso 6: Verificar en GitHub

1. Ve a tu repositorio en GitHub
2. Verifica que todos los archivos estén subidos
3. Verifica que el README se vea correctamente

---

## 🔧 Opción 2: Usar GitHub Desktop (Interfaz Gráfica)

### Paso 1: Instalar GitHub Desktop

1. Descarga desde: https://desktop.github.com/
2. Instala y abre GitHub Desktop
3. Inicia sesión con tu cuenta de GitHub

### Paso 2: Crear Repositorio

1. En GitHub Desktop: **File** → **New Repository**
2. Configura:
   - **Name**: `sistema-a2a`
   - **Local Path**: Selecciona la carpeta actual
   - **Git Ignore**: None (ya tenemos .gitignore)
   - **License**: None (ya tenemos LICENSE)
3. Click **Create Repository**

### Paso 3: Preparar Archivos

```powershell
# Renombrar README
Move-Item README-GITHUB.md README.md -Force
```

### Paso 4: Commit y Push

1. En GitHub Desktop verás todos los archivos en "Changes"
2. Escribe un mensaje de commit: `Initial commit: Sistema A2A v1.3`
3. Click **Commit to main**
4. Click **Publish repository**
5. Elige:
   - ✅ Public o Private
   - Descripción: `Framework Multi-Agente para Simulación de Redes`
6. Click **Publish repository**

---

## 📝 Opción 3: Crear Personal Access Token (Para git push)

Si `git push` te pide contraseña:

### Paso 1: Crear Token en GitHub

1. Ve a GitHub → Settings (tu perfil)
2. Developer settings → Personal access tokens → Tokens (classic)
3. Generate new token (classic)
4. Configura:
   - **Note**: `Sistema A2A`
   - **Expiration**: 90 days (o lo que prefieras)
   - **Scopes**: Marca `repo` (todos los permisos de repositorio)
5. Click **Generate token**
6. **COPIA EL TOKEN** (solo se muestra una vez)

### Paso 2: Usar Token

Cuando `git push` pida contraseña:
- **Username**: tu usuario de GitHub
- **Password**: pega el token (no tu contraseña)

---

## 🔄 Actualizaciones Futuras

Cuando hagas cambios y quieras actualizarlos en GitHub:

```bash
# Ver qué cambió
git status

# Añadir cambios
git add .

# Commit con mensaje descriptivo
git commit -m "Descripción de los cambios"

# Subir a GitHub
git push
```

---

## 📂 Estructura que se Subirá

```
sistema-a2a/
├── .gitignore                        ← Archivos a ignorar
├── LICENSE                           ← Licencia MIT
├── README.md                         ← Documentación principal
├── GUIA-INVESTIGADORES-REDES.md     ← Guía completa
├── INSTRUCCIONES-UBUNTU.md          ← Instalación Ubuntu
├── INDICE-GUIA-INVESTIGADORES.md    ← Navegación rápida
├── LEEME-GUIA-INVESTIGADORES.md     ← Inicio rápido
├── sistema-a2a-v1.3-final/          ← Código del sistema
│   ├── agents/
│   ├── config/
│   ├── utils/
│   ├── docs/
│   ├── main.py
│   ├── supervisor.py
│   └── requirements.txt
├── sistema-a2a-v1.3-ubuntu.zip      ← Paquete de exportación
└── versiones-anteriores/            ← Versiones previas
```

**Archivos que NO se subirán** (por .gitignore):
- `__pycache__/`
- `venv/`
- `*.log`
- Archivos temporales de trabajo
- Resultados de simulaciones

---

## ✅ Verificación Post-Subida

Después de subir, verifica:

1. **README se ve bien**: https://github.com/TU-USUARIO/TU-REPO
2. **Archivos presentes**:
   - ✅ README.md
   - ✅ GUIA-INVESTIGADORES-REDES.md
   - ✅ INSTRUCCIONES-UBUNTU.md
   - ✅ sistema-a2a-v1.3-final/
   - ✅ LICENSE
3. **Badges funcionan** (en el README)
4. **Enlaces internos funcionan** (click en los enlaces del README)

---

## 🎨 Personalizar el Repositorio

### Añadir Topics (Etiquetas)

En GitHub, en tu repositorio:
1. Click en el ⚙️ junto a "About"
2. Añade topics:
   - `ns3`
   - `manet`
   - `vanet`
   - `multi-agent-system`
   - `deep-learning`
   - `network-simulation`
   - `routing-protocols`
   - `research`

### Añadir Descripción

En "About":
- **Description**: `Framework Multi-Agente para Simulación de Redes MANET/VANET con NS-3, Deep Learning y Análisis Estadístico`
- **Website**: (si tienes)
- **Topics**: (los que añadiste arriba)

---

## 🔒 Configuración de Seguridad

### Si el Repositorio es Público

1. **NO subas**:
   - Contraseñas
   - API keys
   - Tokens
   - Información personal

2. **Revisa** que `config/settings.py` no tenga información sensible

3. **Usa variables de entorno** para configuración sensible

---

## 📊 Hacer el Repositorio Atractivo

### README Badges

Ya incluidos en `README-GITHUB.md`:
- Version badge
- NS-3 badge
- Python badge
- License badge

### Añadir Screenshots

Puedes añadir capturas de pantalla:

```markdown
## 📸 Screenshots

### Dashboard de Resultados
![Dashboard](docs/images/dashboard.png)

### Gráficos Generados
![Graficos](docs/images/graficos.png)
```

---

## 🎓 Para Tesis Doctoral

### Hacer el Repositorio Citable

1. **Añade un archivo CITATION.cff**:

```yaml
cff-version: 1.2.0
message: "Si usas este software, por favor cítalo como se indica."
authors:
  - family-names: "Tu Apellido"
    given-names: "Tu Nombre"
title: "Sistema A2A: Framework Multi-Agente para Simulación de Redes"
version: 1.3
date-released: 2025-11-24
url: "https://github.com/TU-USUARIO/sistema-a2a"
```

2. **Obtén un DOI** (opcional):
   - Conecta tu repositorio con Zenodo
   - Zenodo te dará un DOI permanente
   - Útil para citas académicas

---

## 🆘 Problemas Comunes

### Error: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git
```

### Error: "failed to push some refs"

```bash
# Si el repositorio remoto tiene archivos que no tienes local
git pull origin main --allow-unrelated-histories
git push origin main
```

### Archivo muy grande (>100MB)

GitHub tiene límite de 100MB por archivo. Si tienes archivos grandes:

```bash
# Usar Git LFS (Large File Storage)
git lfs install
git lfs track "*.zip"
git add .gitattributes
git commit -m "Add Git LFS"
```

### Olvidé renombrar README-GITHUB.md

```bash
git mv README-GITHUB.md README.md
git commit -m "Rename README"
git push
```

---

## 📞 Ayuda Adicional

- **Documentación Git**: https://git-scm.com/doc
- **Guías GitHub**: https://guides.github.com/
- **GitHub Desktop**: https://docs.github.com/en/desktop

---

## ✅ Checklist Final

Antes de subir, verifica:

- [ ] Renombré `README-GITHUB.md` a `README.md`
- [ ] Revisé que no haya información sensible
- [ ] Verifiqué el `.gitignore`
- [ ] Creé el repositorio en GitHub
- [ ] Configuré mi identidad Git
- [ ] Hice el commit inicial
- [ ] Conecté con el repositorio remoto
- [ ] Hice push exitosamente
- [ ] Verifiqué que todo se vea bien en GitHub
- [ ] Añadí topics y descripción
- [ ] El README se ve correctamente

---

## 🎉 ¡Listo!

Una vez subido, tu repositorio estará disponible en:
```
https://github.com/TU-USUARIO/sistema-a2a
```

Comparte el enlace con:
- Tu director de tesis
- Colaboradores
- La comunidad de investigación

---

**¡Éxito con tu repositorio!** 🚀

---

**Nota**: Reemplaza `TU-USUARIO` y `TU-REPO` con tus datos reales de GitHub.
