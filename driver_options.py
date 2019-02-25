
from selenium.webdriver.chrome.options import Options

chromedriver_path = r"/home/alekhan/trabajo/TotemManager/chromedriver"


options = Options()
# options.headless = True
# options.add_argument("--headless")
options.add_argument("--kiosk")
options.add_argument("--disable-infobars")
