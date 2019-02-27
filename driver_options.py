from selenium.webdriver.chrome.options import Options
import os

cwd = os.getcwd()
chromedriver_path = r"{}/chromedriver".format(cwd)

options = Options()
options.add_argument("--kiosk")
options.add_argument("--disable-infobars")
