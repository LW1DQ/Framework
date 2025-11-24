# Script para Preparar el Proyecto para GitHub
# Sistema A2A v1.3

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  PREPARAR PROYECTO PARA GITHUB" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Paso 1: Renombrar README
Write-Host "Paso 1: Renombrando README..." -ForegroundColor Yellow
if (Test-Path "README-GITHUB.md") {
    Move-Item "README-GITHUB.md" "README.md" -Force
    Write-Host "  [OK] README.md creado" -ForegroundColor Green
} else {
    Write-Host "  [AVISO] README-GITHUB.md no encontrado" -ForegroundColor Red
}

# Paso 2: Verificar archivos importantes
Write-Host ""
Write-Host "Paso 2: Verificando archivos importantes..." -ForegroundColor Yellow

$archivos_importantes = @(
    "README.md",
    "GUIA-INVESTIGADORES-REDES.md",
    "INSTRUCCIONES-UBUNTU.md",
    "INDICE-GUIA-INVESTIGADORES.md",
    "LEEME-GUIA-INVESTIGADORES.md",
    ".gitignore",
    "LICENSE"
)

foreach ($archivo in $archivos_importantes) {
    if (Test-Path $archivo) {
        $size = (Get-Item $archivo).Length / 1KB
        $sizeStr = [math]::Round($size, 1)
        Write-Host "  [OK] $archivo ($sizeStr KB)" -ForegroundColor Green
    } else {
        Write-Host "  [X] $archivo NO ENCONTRADO" -ForegroundColor Red
    }
}

# Paso 3: Verificar carpetas importantes
Write-Host ""
Write-Host "Paso 3: Verificando carpetas..." -ForegroundColor Yellow

$carpetas_importantes = @(
    "sistema-a2a-v1.3-final",
    "versiones-anteriores"
)

foreach ($carpeta in $carpetas_importantes) {
    if (Test-Path $carpeta) {
        $count = (Get-ChildItem $carpeta -Recurse -File).Count
        Write-Host "  [OK] $carpeta ($count archivos)" -ForegroundColor Green
    } else {
        Write-Host "  [X] $carpeta NO ENCONTRADA" -ForegroundColor Red
    }
}

# Paso 4: Verificar Git
Write-Host ""
Write-Host "Paso 4: Verificando Git..." -ForegroundColor Yellow
try {
    $git_version = git --version 2>&1
    Write-Host "  [OK] Git instalado: $git_version" -ForegroundColor Green
    $git_instalado = $true
} catch {
    Write-Host "  [X] Git NO instalado" -ForegroundColor Red
    Write-Host "    Descarga desde: https://git-scm.com/" -ForegroundColor Yellow
    $git_instalado = $false
}

# Paso 5: Mostrar siguiente paso
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  PREPARACION COMPLETADA" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "SIGUIENTE PASO:" -ForegroundColor Yellow
Write-Host "  1. Abre INSTRUCCIONES-SUBIR-GITHUB.md" -ForegroundColor White
Write-Host "  2. Sigue las instrucciones paso a paso" -ForegroundColor White
Write-Host "  3. O ejecuta los siguientes comandos:" -ForegroundColor White
Write-Host ""

Write-Host "     git init" -ForegroundColor Cyan
Write-Host "     git add ." -ForegroundColor Cyan
Write-Host "     git commit -m `"Initial commit: Sistema A2A v1.3`"" -ForegroundColor Cyan
Write-Host "     git remote add origin https://github.com/TU-USUARIO/TU-REPO.git" -ForegroundColor Cyan
Write-Host "     git branch -M main" -ForegroundColor Cyan
Write-Host "     git push -u origin main" -ForegroundColor Cyan
Write-Host ""

Write-Host "NOTA: Reemplaza TU-USUARIO y TU-REPO con tus datos reales" -ForegroundColor Yellow
Write-Host ""

# Paso 6: Preguntar si quiere inicializar Git
if ($git_instalado) {
    Write-Host "Quieres inicializar Git ahora? (S/N): " -ForegroundColor Yellow -NoNewline
    $respuesta = Read-Host

    if ($respuesta -eq "S" -or $respuesta -eq "s") {
        Write-Host ""
        Write-Host "Inicializando Git..." -ForegroundColor Yellow
        
        # Inicializar Git
        git init
        
        # Configurar usuario (si no esta configurado)
        Write-Host ""
        Write-Host "Configura tu identidad Git:" -ForegroundColor Yellow
        Write-Host "Nombre: " -NoNewline
        $nombre = Read-Host
        Write-Host "Email: " -NoNewline
        $email = Read-Host
        
        git config user.name "$nombre"
        git config user.email "$email"
        
        # Anadir archivos
        Write-Host ""
        Write-Host "Anadiendo archivos..." -ForegroundColor Yellow
        git add .
        
        # Mostrar estado
        Write-Host ""
        Write-Host "Estado de Git:" -ForegroundColor Yellow
        git status
        
        # Preguntar si hacer commit
        Write-Host ""
        Write-Host "Hacer commit inicial? (S/N): " -ForegroundColor Yellow -NoNewline
        $commit = Read-Host
        
        if ($commit -eq "S" -or $commit -eq "s") {
            git commit -m "Initial commit: Sistema A2A v1.3 con documentacion completa"
            Write-Host ""
            Write-Host "[OK] Commit realizado" -ForegroundColor Green
            
            Write-Host ""
            Write-Host "Ahora necesitas:" -ForegroundColor Yellow
            Write-Host "  1. Crear repositorio en GitHub" -ForegroundColor White
            Write-Host "  2. Ejecutar:" -ForegroundColor White
            Write-Host "     git remote add origin https://github.com/TU-USUARIO/TU-REPO.git" -ForegroundColor Cyan
            Write-Host "     git branch -M main" -ForegroundColor Cyan
            Write-Host "     git push -u origin main" -ForegroundColor Cyan
        }
    } else {
        Write-Host ""
        Write-Host "Puedes inicializar Git manualmente mas tarde." -ForegroundColor White
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
