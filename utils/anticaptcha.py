from anticaptchaofficial.recaptchav2proxyless import * #See more documentation at https://anti-captcha.com/es/apidoc
from dotenv import load_dotenv
import os

class RecaptchaSolver:
    """
    This class is a reutilizable component for solving reCAPTCHA.
    Its intended to persist acrosss multimple platforms and applications.
    """
    def __init__(self, website_url, website_key):
        load_dotenv()
        self.website_url = website_url
        self.website_key = website_key
    
    def solve(self):
        """
        This method solves the reCAPTCHA using AntiCaptcha's service.
        It initializes the solver with the website URL and key, sets the API key,
        and attempts to solve the reCAPTCHA. If successful, it returns the g-response.
        If there is an error, it prints the error code and returns None.
        """
        solver = recaptchaV2Proxyless()
        solver.set_verbose(1)
        solver.set_key(os.getenv('ANTICAPTCHA_API_KEY'))
        solver.set_website_url(self.website_url)
        solver.set_website_key(self.website_key)

        g_response = solver.solve_and_return_solution()
        if g_response != 0:
            print("g-response: " + g_response)
            return g_response
        else:
            print("Error: " + solver.error_code)
            return None
