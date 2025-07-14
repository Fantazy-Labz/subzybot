from anticaptchaofficial.recaptchav2proxyless import *
from dotenv import load_dotenv
import os

class RecaptchaSolver:
    def __init__(self, website_url, website_key):
        load_dotenv()
        self.website_url = website_url
        self.website_key = website_key
    
    def solve(self):
        
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
