from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to your ChromeDriver executable
PATH = "C:/Users/timch/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# Create a Service object with the path
service = Service(PATH)

# Initialize the Chrome webdriver with the Service object
driver = webdriver.Chrome(service=service)

driver.get("https://www.urbtix.hk/")
# Wait for and find the element
wait = WebDriverWait(driver, 10)

search = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "search")))
search.send_keys("演唱會")

