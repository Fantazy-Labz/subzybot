from anticaptchaofficial.recaptchav2proxyless import *
from dotenv import load_dotenv
import os

load_dotenv()


solver = recaptchaV2Proxyless()
solver.set_verbose(1)
solver.set_key("c5e932f34fb92d6cc9d5eb6a441afbee")
solver.set_website_url(os.getenv("CAPTCHA_API_KEY"))
solver.set_website_key("SITE_KEY")
#set optional custom parameter which Google made for their search page Recaptcha v2
#solver.set_data_s('"data-s" token from Google Search results "protection"')

# Specify softId to earn 10% commission with your app.
# Get your softId here: https://anti-captcha.com/clients/tools/devcenter
solver.set_soft_id(0)

g_response = solver.solve_and_return_solution()
if g_response != 0:
    print("g-response: "+g_response)
else:
    print("task finished with error "+solver.error_code)