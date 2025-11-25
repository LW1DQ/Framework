#!/bin/bash
# Script para ejecutar el Dashboard del Sistema A2A

echo "🚀 Iniciando Dashboard del Sistema A2A..."
echo ""

# Verificar que streamlit esté instalado
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit no está instalado"
    echo "   Instalar con: pip install streamlit"
    exit 1
fi

# Verificar que el archivo dashboard.py existe
if [ ! -f "dashboard.py" ]; then
    echo "❌ Archivo dashboard.py no encontrado"
    exit 1
fi

echo "✅ Streamlit encontrado"
echo "✅ Dashboard encontrado"
echo ""
echo "📊 Abriendo dashboard en el navegador..."
echo "   URL: http://localhost:8501"
echo ""
echo "💡 Tip: Ejecuta 'python main.py' en otra terminal para ver el sistema en acción"
echo ""
echo "🛑 Presiona Ctrl+C para detener el dashboard"
echo ""

# Ejecutar streamlit
streamlit run dashboard.py
