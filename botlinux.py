import time
import os
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

class SubzyBotLinuxOptimized:
    """
    Versión optimizada de SubzyBot para sistemas Linux
    Maneja automáticamente las dependencias y configuraciones necesarias
    """
    
    def __init__(self, headless=True):
        self.driver = None
        self.headless = headless
        self.wait_timeout = 10
        self.system_info = self._get_system_info()
        
    def _get_system_info(self):
        """Obtiene información del sistema para optimizar configuración"""
        return {
            'platform': platform.system(),
            'release': platform.release(),
            'machine': platform.machine(),
            'is_wsl': 'microsoft' in platform.release().lower(),
            'is_docker': os.path.exists('/.dockerenv')
        }
    
    def setup_driver(self):
        """
        Configuración robusta del driver para Linux
        Maneja automáticamente dependencias y problemas comunes
        """
        try:
            print(f"🔧 Configurando driver para {self.system_info['platform']}...")
            
            # Configurar opciones de Chrome optimizadas para Linux
            chrome_options = Options()
            
            # Opciones esenciales para Linux headless
            if self.headless or self.system_info['is_docker']:
                chrome_options.add_argument("--headless=new")  # Nuevo modo headless más estable
                
            # Configuraciones críticas para Linux
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-javascript")  # Opcional para mayor velocidad
            
            # Configuraciones específicas para WSL
            if self.system_info['is_wsl']:
                chrome_options.add_argument("--disable-background-timer-throttling")
                chrome_options.add_argument("--disable-renderer-backgrounding")
                
            # Configuraciones para contenedores Docker
            if self.system_info['is_docker']:
                chrome_options.add_argument("--disable-crash-reporter")
                chrome_options.add_argument("--disable-logging")
                chrome_options.add_argument("--disable-background-networking")
                
            # User agent realista
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Configurar ventana
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")
            
            # Usar WebDriver Manager para manejo automático de ChromeDriver
            print("📥 Descargando/verificando ChromeDriver...")
            service = Service(ChromeDriverManager().install())
            
            # Crear instancia del driver
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Configuraciones adicionales
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            print("✅ Driver configurado exitosamente")
            return True
            
        except WebDriverException as e:
            if "Status code was: 127" in str(e):
                print("❌ Error 127 detectado - Faltan dependencias del sistema")
                self._suggest_dependency_fix()
                return False
            else:
                print(f"❌ Error de WebDriver: {e}")
                return False
        except Exception as e:
            print(f"❌ Error inesperado configurando driver: {e}")
            return False
    
    def _suggest_dependency_fix(self):
        """
        Sugiere soluciones para el error 127 (dependencias faltantes)
        """
        print("\n🔧 SOLUCIÓN REQUERIDA:")
        print("El error 127 indica que faltan dependencias del sistema.")
        print("Ejecuta estos comandos para solucionarlo:\n")
        
        if self.system_info['platform'] == 'Linux':
            print("# Para Ubuntu/Debian:")
            print("sudo apt update")
            print("sudo apt install -y libnss3 libgconf-2-4 libfontconfig1 libxcb1 libxss1 libgtk-3-0")
            print("sudo apt install -y google-chrome-stable")
            print("\n# Para CentOS/RHEL:")
            print("sudo yum install -y nss libXScrnSaver atk java-atk-wrapper at-spi2-atk gtk3 libXt xorg-x11-server-Xvfb")
            print("\n# Alternativa con Chromium:")
            print("sudo apt install -y chromium-browser chromium-chromedriver")
            
        print("\n💡 También puedes usar Docker para evitar problemas de dependencias")
        print("Ver: docker/Dockerfile en el proyecto para configuración completa")
    
    def test_driver_functionality(self):
        """
        Prueba básica para verificar que el driver funciona correctamente
        """
        try:
            print("🧪 Probando funcionalidad del driver...")
            
            # Navegar a una página simple
            self.driver.get("https://www.google.com")
            
            # Verificar que la página cargó
            assert "Google" in self.driver.title
            
            print("✅ Driver funcionando correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error en prueba del driver: {e}")
            return False
    
    def diagnose_system(self):
        """
        Ejecuta diagnósticos del sistema para identificar problemas
        """
        print("🔍 Ejecutando diagnósticos del sistema...")
        print(f"   Sistema: {self.system_info}")
        
        # Verificar si Chrome está instalado
        chrome_paths = [
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/usr/bin/chromium-browser',
            '/usr/bin/chromium'
        ]
        
        chrome_found = False
        for path in chrome_paths:
            if os.path.exists(path):
                print(f"✅ Chrome encontrado en: {path}")
                chrome_found = True
                break
                
        if not chrome_found:
            print("❌ Chrome/Chromium no encontrado")
            print("   Instala con: sudo apt install google-chrome-stable")
            
        # Verificar dependencias críticas
        critical_libs = [
            '/usr/lib/x86_64-linux-gnu/libnss3.so',
            '/usr/lib/x86_64-linux-gnu/libfontconfig.so.1',
            '/usr/lib/x86_64-linux-gnu/libglib-2.0.so.0'
        ]
        
        for lib in critical_libs:
            if os.path.exists(lib):
                print(f"✅ Librería encontrada: {lib}")
            else:
                print(f"❌ Librería faltante: {lib}")
    
    def login_spotify_robust(self, email, password):
        """
        Versión robusta del login para Spotify optimizada para Linux
        """
        try:
            print("🎵 Iniciando login en Spotify...")
            
            # Navegar a Spotify
            self.driver.get("https://accounts.spotify.com/login")
            
            # Esperar a que cargue la página
            wait = WebDriverWait(self.driver, self.wait_timeout)
            
            # Localizar campos con múltiples estrategias
            try:
                email_field = wait.until(
                    EC.presence_of_element_located((By.ID, "login-username"))
                )
            except TimeoutException:
                # Estrategia alternativa
                email_field = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-username']"))
                )
            
            password_field = self.driver.find_element(By.ID, "login-password")
            
            # Limpiar campos y escribir credenciales
            email_field.clear()
            password_field.clear()
            
            #buttonTertiary

            # Simular escritura humana
            self._type_human_like(email_field, email)
            time.sleep(0.5)
            self._type_human_like(password_field, password)
            
            # Hacer clic en login
            login_button = self.driver.find_element(By.ID, "login-button")
            self.driver.execute_script("arguments[0].click();", login_button)
            
            # Verificar éxito
            time.sleep(3)
            current_url = self.driver.current_url
            
            if "open.spotify.com" in current_url or "accounts.spotify.com/status" in current_url:
                print("✅ Login exitoso en Spotify")
                return True
            else:
                print("❌ Login falló - Verificar credenciales")
                return False
                
        except Exception as e:
            print(f"❌ Error durante login: {e}")
            return False
    
    def _type_human_like(self, element, text, delay_range=(0.05, 0.15)):
        """Simula escritura humana con delays aleatorios"""
        import random
        
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(*delay_range))
    
    def cleanup(self):
        """Limpia recursos del driver"""
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Driver cerrado correctamente")
            except Exception as e:
                print(f"⚠️ Error cerrando driver: {e}")

def main():
    """Función principal con manejo robusto de errores"""
    print("🤖 SubzyBot - Versión Linux Optimizada")
    print("=" * 50)
    
    bot = SubzyBotLinuxOptimized(headless=True)
    
    try:
        # Ejecutar diagnósticos
        bot.diagnose_system()
        print()
        
        # Configurar driver
        if not bot.setup_driver():
            print("❌ No se pudo configurar el driver. Ver sugerencias arriba.")
            return 1
        
        # Probar funcionalidad básica
        if not bot.test_driver_functionality():
            print("❌ El driver no funciona correctamente")
            return 1
        
        # Solicitar credenciales si el test básico pasó
        print("\n" + "=" * 50)
        email = input("📧 Email de Spotify: ")
        password = input("🔐 Contraseña: ")
        
        # Intentar login
        if bot.login_spotify_robust(email, password):
            print("🎉 ¡SubzyBot funcionando correctamente!")
            input("Presiona Enter para continuar...")
        else:
            print("❌ No se pudo completar el login")
            return 1
            
    except KeyboardInterrupt:
        print("\n🛑 Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return 1
    finally:
        bot.cleanup()
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)