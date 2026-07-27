
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options

options = Options()
# options.debugger_address = "127.0.0.1:9222"
#
# driver = webdriver.Chrome(options=options)
driver = webdriver.Firefox(options=options)
