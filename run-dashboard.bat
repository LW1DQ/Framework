@echo off
REM Script para ejecutar el Dashboard del Sistema A2A en Windows

echo.
echo ========================================
echo   Dashboard Sistema A2A
echo ========================================
echo.

REM Verificar que streamlit este instalado
where streamlit >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Streamlit no esta instalado
    echo         Instalar con: pip install streamlit
    pause
    exit /b 1
)

REM Verificar que el archivo dashboard.py existe
if not exist "dashboard.py" (
    echo [ERROR] Archivo dashboard.py no encontrado
    pause
    exit /b 1
)

echo [OK] Streamlit encontrado
echo [OK] Dashboard encontrado
echo.
echo Abriendo dashboard en el navegador...
echo URL: http://localhost:8501
echo.
echo Tip: Ejecuta 'python main.py' en otra terminal
echo      para ver el sistema en accion
echo.
echo Presiona Ctrl+C para detener el dashboard
echo.

REM Ejecutar streamlit
streamlit run dashboard.py
