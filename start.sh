#!/bin/bash
# Script para iniciar la interfaz en un servidor HTTP local

echo ""
echo "🚀 Iniciando servidor de interfaz de casos..."
echo ""
echo "📂 Directorio: $(pwd)"
echo "🌐 URL: http://localhost:8000/index.html"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""
echo "---"
echo ""

python3 -m http.server 8000

