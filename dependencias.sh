#!/bin/bash
# SubzyBot - Script de configuración para Linux
# Soluciona el error "chromedriver unexpectedly exited. Status code was: 127"

echo "🔧 Configurando SubzyBot para Linux..."

# 1. Actualizar el sistema
echo "📦 Actualizando paquetes del sistema..."
sudo apt update

# 2. Instalar dependencias críticas para ChromeDriver
echo "🔗 Instalando dependencias de ChromeDriver..."
sudo apt install -y \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxcb1 \
    libxss1 \
    libgconf-2-4 \
    libxtst6 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxext6 \
    libxfixes3 \
    libxrender1 \
    libcairo2 \
    libcups2 \
    libdrm2 \
    libgtk-3-0 \
    libgtk2.0-0

# 3. Instalar Google Chrome (recomendado)
echo "🌐 Instalando Google Chrome..."
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install -y google-chrome-stable

# 4. Verificar instalación
echo "✅ Verificando instalación..."
google-chrome --version

# 5. Instalar dependencias de Python
echo "🐍 Instalando dependencias de Python..."
pip install selenium webdriver-manager

echo "🎉 Configuración completada!"
echo ""
echo "💡 Consejos adicionales:"
echo "   - Si usas WSL, asegúrate de tener acceso a X11"
echo "   - Para servidores sin GUI, usa siempre --headless"
echo "   - Considera usar Docker para mayor consistencia"