from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from src.platforms.spotify.spotify_bot_login import SpotifyLogin
from dotenv import load_dotenv
import os
import time

class SpotifyBotAssignSpace:

    def __init__(self, invitation_link=None, admin_address=None):
        self.invitation_link = invitation_link
        self.admin_address = admin_address

        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def assign_space(self, email, password, has_paid):
        try:
            if  has_paid:
                spotify_login = SpotifyLogin()  
                logged_in = spotify_login.login(email, password) 

                if logged_in:
                    self.driver.get("https://www.spotify.com/mx/account/family/")
                    
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, "invite-link"))
                    )

                    invite_input = self.driver.find_element(By.ID, "invite-link")
                    self.invitation_link = invite_input.get_attribute("value")
                    self.admin_address = email  

        except TimeoutException:
            raise Exception("Timeout while trying to access family page")

        finally:
            self.driver.quit()

        return self.invitation_link, self.admin_address
    
if __name__ == "__main__":
    load_dotenv()
    bot = SpotifyBotAssignSpace()
    email = os.getenv("SPOTIFY_CLIENT_EMAIL")
    password = os.getenv("SPOTIFY_CLIENT_PASSWORD")
    link, admin = bot.assign_space(email, password, has_paid=True)
    print(f"Link de invitación: {link}")
    print(f"Admin: {admin}")


