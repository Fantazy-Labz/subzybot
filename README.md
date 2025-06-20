


# SpotifyLoginBot - Automatización de Inicio de Sesión en Spotify

##  Requisitos del Entorno

Asegúrate de tener las siguientes versiones o superiores instaladas:

| Paquete                    | Versión Recomendada                                           |
| -------------------------- | ------------------------------------------------------------- |
| Python                     | >= 3.8                                                        |
| selenium                   | >= 4.10                                                       |
| Google Chrome              | >= 114                                                        |
| ChromeDriver               | Compatible con tu versión de Chrome                           |
| chromedriver-autoinstaller | *(opcional, si deseas automatizar la instalación del driver)* |

Instalación:

```bash
pip install selenium
```

---

##  Objetivo del Proyecto

Automatizar el proceso de login en **Spotify** de forma segura y robusta, aplicando buenas prácticas de automatización con Selenium, como:

* Patrón Singleton para evitar múltiples instancias del navegador.
* Login automático con escritura simulada.
* Carga y guardado de cookies para mantener sesiones activas.
* Manejo de excepciones comunes y errores de UI.
* Recuperación de las playlists del usuario una vez logueado.

---

##  Diagrama de Flujo del Bot

```plaintext
        +-------------------+
        | Iniciar Script    |
        +-------------------+
                 |
                 v
     +------------------------+
     | Solicitar credenciales |
     +------------------------+
                 |
                 v
     +--------------------------+
     | Configurar navegador     |
     +--------------------------+
                 |
                 v
     +------------------------------+
     | ¿Existe sesión guardada?     |
     +---------------+--------------+
                     | Sí
                     v
           +---------------------+
           | Cargar sesión       |
           +---------------------+
                     |
                     v
             +---------------+
             | Verificar     |
             +---------------+
                     |
                     v
             +---------------+
             | Obtener datos |
             +---------------+

                     |
                  No v
     +------------------------------+
     | Realizar login con usuario   |
     +------------------------------+
                 |
                 v
        +---------------------+
        | Guardar sesión      |
        +---------------------+
                 |
                 v
        +----------------------+
        | Obtener playlists    |
        +----------------------+
```
---

##  Uso Paso a Paso

### 1. Clona o descarga el repositorio

```bash
git clone https://github.com/tuusuario/SpotifyLoginBot.git
cd SpotifyLoginBot
```

### 2. Instala las dependencias

```bash
pip install selenium
```

> Asegúrate de tener `chromedriver` en tu PATH o en la misma carpeta que el script.

### 3. Ejecuta el bot

```bash
python spotify_login_bot.py
```

### 4. Ingresa tus credenciales cuando se soliciten:

* Email de Spotify
* Contraseña

Si el login es exitoso:

* Se guarda una sesión en `spotify_session.json`
* Se extraen las primeras 5 playlists del usuario
* El navegador se queda abierto para inspección manual

---

##  Estructura del Código

```
spotify_login_bot.py
│
├── SpotifyLoginBot
│   ├── __init__()              → Inicializa configuración
│   ├── setup_driver()         → Configura Chrome con opciones headless
│   ├── login_with_credentials() → Realiza el login
│   ├── _type_like_human()     → Simula escritura humana
│   ├── _verify_login_success() → Valida que el login fue exitoso
│   ├── get_user_playlists()   → Extrae los nombres de las playlists
│   ├── save_session()         → Guarda cookies en un archivo
│   ├── load_session()         → Carga cookies si existen
│   └── cleanup()              → Cierra navegador
│
└── main() → Función principal para iniciar el flujo completo
```







