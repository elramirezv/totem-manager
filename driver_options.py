from selenium.webdriver.chrome.options import Options
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication
import sys

cwd = os.getcwd()
chromedriver_path = r"{}/chromedriver".format(cwd)
extension_path = "{}/block-site-extension.0.8.1.crx".format(cwd)

options = Options()
options.add_extension(extension_path)
# options.add_argument("--kiosk")
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
