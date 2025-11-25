# Script de Preparación para GitHub Release
# Este script inicializa el repositorio, añade los archivos y prepara el commit.

Write-Host "🚀 Iniciando preparación para GitHub Release..." -ForegroundColor Cyan

# 1. Verificar si git está instalado
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git no está instalado. Por favor instálalo primero." -ForegroundColor Red
    exit 1
}

# 2. Inicializar repositorio si no existe
if (-not (Test-Path ".git")) {
    Write-Host "📦 Inicializando repositorio git..." -ForegroundColor Yellow
    git init
} else {
    Write-Host "ℹ️  Repositorio git ya inicializado." -ForegroundColor Green
}

# 3. Configurar remoto
$remoteUrl = "https://github.com/LW1DQ/Framework.git"
$currentRemote = git remote get-url origin 2>$null

if (-not $currentRemote) {
    Write-Host "🔗 Añadiendo remoto origin: $remoteUrl" -ForegroundColor Yellow
    git remote add origin $remoteUrl
} elseif ($currentRemote -ne $remoteUrl) {
    Write-Host "⚠️  Remoto origin actual es diferente: $currentRemote" -ForegroundColor Yellow
    Write-Host "🔗 Actualizando remoto a: $remoteUrl" -ForegroundColor Yellow
    git remote set-url origin $remoteUrl
} else {
    Write-Host "✅ Remoto origin configurado correctamente." -ForegroundColor Green
}

# 4. Añadir archivos
Write-Host "➕ Añadiendo archivos al stage..." -ForegroundColor Yellow
git add .

# 5. Mostrar estado
Write-Host "`n📊 Estado del repositorio:" -ForegroundColor Cyan
git status

Write-Host "`n✅ Preparación completada." -ForegroundColor Green
Write-Host "📝 Para subir los cambios, ejecuta:" -ForegroundColor Cyan
Write-Host "   git commit -m 'Release v1.4: NS-3 AI Integration & Structured Error Handling'"
Write-Host "   git push -u origin master"
