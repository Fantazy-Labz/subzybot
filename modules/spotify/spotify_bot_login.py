from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random
import os
from dotenv import load_dotenv

class SpotifyLogin:
    def __init__(self):
        # Configurar opciones de Chrome para evitar detección de bot
        chrome_options = Options()
        
        # Opciones para parecer más humano
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Configuraciones adicionales
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized")
        
        # User agent más realista
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Inicializar driver
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Ejecutar script para ocultar webdriver
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def human_typing(self, element, text, delay_range=(0.05, 0.15)):
        """Simula escritura humana con delays variables"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(*delay_range))
    
    def human_click(self, element):
        """Simula click humano con movimiento de mouse"""
        actions = ActionChains(self.driver)
        actions.move_to_element(element).pause(random.uniform(0.1, 0.3)).click().perform()
        
    def wait_and_find_element(self, locator, timeout=15):
        """Espera y encuentra elemento con mejor manejo de errores"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except Exception as e:
            print(f"❌ No se pudo encontrar elemento {locator}: {e}")
            return None
    
    def login(self, email, password):
        try:
            print("🔄 Navegando a Spotify...")
            self.driver.get("https://open.spotify.com/")
            time.sleep(random.uniform(2, 4))
            
            # Buscar y hacer clic en "Log in"
            print("🔄 Buscando botón de login...")
            
            # Múltiples selectores posibles para el botón de login
            login_selectors = [
                '[data-testid="login-button"]',
                'button[data-encore-id="buttonSecondary"]',
                'a[href*="login"]',
                'button:contains("Log in")',
                '[aria-label*="log in" i]'
            ]
            
            login_button = None
            for selector in login_selectors:
                try:
                    login_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not login_button:
                # Si no encuentra botón, ir directamente a login
                print("🔄 Navegando directamente a página de login...")
                self.driver.get("https://accounts.spotify.com/login")
            else:
                print("🔄 Haciendo clic en botón de login...")
                self.human_click(login_button)
            
            time.sleep(random.uniform(3, 5))
            
            # Buscar campo de email/username con múltiples selectores
            print("🔄 Buscando campo de email...")
            email_selectors = [
                '#login-username',
                '[data-testid="login-username"]',
                'input[name="username"]',
                'input[type="text"]',
                'input[placeholder*="email" i]',
                'input[placeholder*="username" i]'
            ]
            
            email_field = None
            for selector in email_selectors:
                try:
                    email_field = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not email_field:
                raise Exception("No se pudo encontrar el campo de email")
            
            print("✅ Campo de email encontrado")
            self.human_typing(email_field, email)
            time.sleep(random.uniform(1, 2))
            
            # Buscar y hacer clic en continuar
            print("🔄 Buscando botón continuar...")
            continue_selectors = [
                '#login-button',
                'button[type="submit"]',
                'button[data-encore-id="buttonPrimary"]',
                'button:contains("Continue")',
                'button:contains("Continuar")',
                '[data-testid="login-button"]'
            ]
            
            continue_button = None
            for selector in continue_selectors:
                try:
                    continue_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not continue_button:
                raise Exception("No se pudo encontrar el botón continuar")
            
            print("🔄 Haciendo clic en continuar...")
            self.human_click(continue_button)
            time.sleep(random.uniform(3, 5))
            
            # Buscar opción "Iniciar sesión con contraseña"
            print("🔄 Buscando opción de contraseña...")
            password_option_selectors = [
                'button[data-encore-id="buttonTertiary"]',
                'button:contains("contraseña")',
                'button:contains("password")',
                '[data-testid="password-login"]',
                'a[href*="password"]'
            ]
            
            password_option = None
            for selector in password_option_selectors:
                try:
                    password_option = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if password_option:
                print("🔄 Haciendo clic en 'Iniciar sesión con contraseña'...")
                self.human_click(password_option)
                time.sleep(random.uniform(2, 4))
            
            # Buscar campo de contraseña
            print("🔄 Buscando campo de contraseña...")
            password_selectors = [
                '#login-password',
                '[data-testid="login-password"]',
                'input[name="password"]',
                'input[type="password"]'
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not password_field:
                raise Exception("No se pudo encontrar el campo de contraseña")
            
            print("✅ Campo de contraseña encontrado")
            self.human_typing(password_field, password)
            time.sleep(random.uniform(1, 2))
            
            # Buscar botón de login final
            print("🔄 Buscando botón de login final...")
            final_login_selectors = [
                'button[type="submit"]',
                'button[data-encore-id="buttonPrimary"]',
                '#login-button',
                'button:contains("Log in")',
                'button:contains("Iniciar sesión")'
            ]
            
            final_login_button = None
            for selector in final_login_selectors:
                try:
                    final_login_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not final_login_button:
                raise Exception("No se pudo encontrar el botón de login final")
            
            print("🔄 Haciendo clic en login final...")
            self.human_click(final_login_button)
            
            # Esperar a completar login
            print("🔄 Esperando completar login...")
            success = WebDriverWait(self.driver, 20).until(
                lambda driver: any([
                    "open.spotify.com" in driver.current_url,
                    "spotify.com/collection" in driver.current_url,
                    driver.current_url.endswith("spotify.com/")
                ]) and "login" not in driver.current_url
            )
            
            if success:
                print("✅ Login exitoso!")
                return True
            else:
                print("❌ Login no se completó correctamente")
                return False
                
        except Exception as e:
            print(f"❌ Error durante login: {e}")
            print(f"🔍 URL actual: {self.driver.current_url}")
            
            # Debug: imprimir elementos disponibles
            try:
                print("🔍 Elementos botón disponibles:")
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                for i, btn in enumerate(buttons[:10]):  # Solo primeros 10
                    try:
                        text = btn.text.strip()
                        if text:
                            print(f"  Botón {i}: '{text}'")
                    except:
                        pass
            except:
                pass
            
            # Capturar screenshot
            try:
                screenshot_name = f"error_screenshot_{int(time.time())}.png"
                self.driver.save_screenshot(screenshot_name)
                print(f"📸 Screenshot guardado como '{screenshot_name}'")
            except:
                pass
                
            return False
    
    def cerrar(self):
        try:
            self.driver.quit()
        except:
            pass

# Uso mejorado:
if __name__ == "__main__":
    load_dotenv
    spotify = SpotifyLogin()

    email = os.getenv("SPOTIFY_CLIENT_EMAIL")
    password = os.getenv("SPOTIFY_CLIENT_PASSWORD")
    
    try:
        print("🚀 Iniciando proceso de login automatizado...")
        if spotify.login(email, password):
            print("✅ Login completado exitosamente!")
            print("🎵 Puedes continuar con tu automatización...")
            time.sleep(10)  # Tiempo para verificar resultado
        else:
            print("❌ Login falló - revisar logs y screenshot")
    
    except KeyboardInterrupt:
        print("🛑 Proceso interrumpido por el usuario")
    
    finally:
        spotify.cerrar()
        print("🔄 Navegador cerrado")