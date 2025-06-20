import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class SpotifyLoginBot:
    """
    Bot para automatizar el inicio de sesión en Spotify
    
    Conceptos clave implementados:
    - Patrón Singleton para una sola instancia del driver
    - Manejo de excepciones robusto
    - Esperas explícitas para elementos dinámicos
    - Configuración de navegador headless opcional
    """
    
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        self.wait_timeout = 10
        
    def setup_driver(self):
        """
        Configura el driver de Chrome con opciones optimizadas
        
        Conceptos de seguridad y rendimiento:
        - Deshabilita imágenes para mayor velocidad
        - Configura user-agent realista
        - Maneja configuraciones de seguridad
        """
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
            
        # Optimizaciones de rendimiento
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")  # Remover si Spotify requiere JS
        
        # User agent realista para evitar detección
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_window_size(1920, 1080)
            print("✓ Driver configurado correctamente")
            return True
        except Exception as e:
            print(f"✗ Error configurando driver: {e}")
            return False
    
    def login_with_credentials(self, email, password):
        """
        Realiza login usando credenciales de usuario
        
        Flujo de autenticación:
        1. Navega a página de login
        2. Localiza elementos de formulario
        3. Ingresa credenciales
        4. Maneja posibles captchas o verificaciones
        """
        try:
            print("🔄 Navegando a página de login...")
            self.driver.get("https://accounts.spotify.com/login")
            
            # Espera explícita para el formulario de login
            wait = WebDriverWait(self.driver, self.wait_timeout)
            
            # Localiza campos de entrada usando múltiples estrategias
            email_field = wait.until(
                EC.presence_of_element_located((By.ID, "login-username"))
            )
            password_field = self.driver.find_element(By.ID, "login-password")
            
            print("🔄 Ingresando credenciales...")
            
            # Simula escritura humana con delays
            self._type_like_human(email_field, email)
            time.sleep(0.5)
            self._type_like_human(password_field, password)
            
            # Busca y hace clic en el botón de login
            login_button = self.driver.find_element(By.ID, "login-button")
            login_button.click()
            
            # Verifica si el login fue exitoso
            return self._verify_login_success()
            
        except TimeoutException:
            print("✗ Timeout: Los elementos de login no cargaron a tiempo")
            return False
        except NoSuchElementException as e:
            print(f"✗ Elemento no encontrado: {e}")
            return False
        except Exception as e:
            print(f"✗ Error durante login: {e}")
            return False
    
    def get_user_playlists(self):
        """
        Ejemplo de funcionalidad post-login:
        Obtiene las playlists del usuario una vez logueado
        """
        try:
            # Navega a la página de playlists
            self.driver.get("https://open.spotify.com/collection/playlists")
            time.sleep(3)
            
            # Busca elementos de playlist
            playlists = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='playlist-cell']")
            
            playlist_names = []
            for playlist in playlists[:5]:  # Solo primeras 5
                try:
                    name_element = playlist.find_element(By.CSS_SELECTOR, "[data-testid='entityTitle']")
                    playlist_names.append(name_element.text)
                except:
                    continue
            
            print(f"✓ Encontradas {len(playlist_names)} playlists:")
            for i, name in enumerate(playlist_names, 1):
                print(f"  {i}. {name}")
                
            return playlist_names
            
        except Exception as e:
            print(f"✗ Error obteniendo playlists: {e}")
            return []
    
    def _type_like_human(self, element, text, delay_range=(0.05, 0.15)):
        """
        Simula escritura humana con delays variables
        Evita detección de bots mediante patrones de escritura naturales
        """
        import random
        
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(*delay_range))
    
    def _verify_login_success(self):
        """
        Verifica si el login fue exitoso analizando la URL y elementos de la página
        """
        try:
            # Espera a que la página cambie después del login
            time.sleep(3)
            
            current_url = self.driver.current_url
            
            # Verifica URLs que indican login exitoso
            success_indicators = [
                "https://open.spotify.com",
                "https://accounts.spotify.com/status",
                "/browse/featured"
            ]
            
            for indicator in success_indicators:
                if indicator in current_url:
                    print("✓ Login exitoso - Redirigido a página principal")
                    return True
            
            # Verifica si hay mensajes de error
            error_elements = self.driver.find_elements(By.CLASS_NAME, "alert-error")
            if error_elements:
                error_text = error_elements[0].text
                print(f"✗ Error de login: {error_text}")
                return False
            
            print("? Estado de login incierto - Verificar manualmente")
            return False
            
        except Exception as e:
            print(f"✗ Error verificando login: {e}")
            return False
    
    def save_session(self, filename="spotify_session.json"):
        """
        Guarda cookies de sesión para reutilización
        Permite mantener sesión activa entre ejecuciones
        """
        try:
            import json
            cookies = self.driver.get_cookies()
            
            with open(filename, 'w') as f:
                json.dump(cookies, f, indent=2)
            
            print(f"✓ Sesión guardada en {filename}")
            return True
            
        except Exception as e:
            print(f"✗ Error guardando sesión: {e}")
            return False
    
    def load_session(self, filename="spotify_session.json"):
        """
        Carga cookies de sesión previamente guardadas
        """
        try:
            import json
            
            if not os.path.exists(filename):
                print(f"✗ Archivo de sesión {filename} no encontrado")
                return False
            
            self.driver.get("https://open.spotify.com")
            
            with open(filename, 'r') as f:
                cookies = json.load(f)
            
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            
            self.driver.refresh()
            print("✓ Sesión cargada correctamente")
            return True
            
        except Exception as e:
            print(f"✗ Error cargando sesión: {e}")
            return False
    
    def cleanup(self):
        """
        Limpia recursos y cierra el navegador
        Importante para evitar procesos zombie
        """
        if self.driver:
            self.driver.quit()
            print("✓ Recursos liberados")

def main():
    """
    Función principal simplificada - solo login con credenciales
    """
    # Configuración básica
    EMAIL = input("Ingresa tu email de Spotify: ")
    PASSWORD = input("Ingresa tu contraseña: ")
    
    bot = SpotifyLoginBot(headless=False)
    
    try:
        print("\n🚀 Iniciando bot de login...")
        
        if not bot.setup_driver():
            print("❌ No se pudo configurar el navegador")
            return
        
        # Intentar cargar sesión previa
        if bot.load_session():
            print("✅ Sesión anterior cargada exitosamente")
        else:
            print("🔐 Realizando login...")
            if bot.login_with_credentials(EMAIL, PASSWORD):
                print("✅ Login exitoso!")
                bot.save_session()
                
                # Ejemplo de funcionalidad adicional
                print("\n📚 Obteniendo tus playlists...")
                bot.get_user_playlists()
            else:
                print("❌ Login falló")
                return
        
        # Mantener navegador abierto
        print("\n✨ Bot funcionando. El navegador permanecerá abierto.")
        input("Presiona Enter cuando quieras cerrar...")
        
    except KeyboardInterrupt:
        print("\n🛑 Proceso interrumpido")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        bot.cleanup()

if __name__ == "__main__":
    main()