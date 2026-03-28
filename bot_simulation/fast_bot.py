from selenium import webdriver
from selenium.webdriver.common.by import By
import time

BASE_URL = "http://127.0.0.1:5000"
ENTRY_URL = f"{BASE_URL}/?actor_type=bot&bot_type=fast&reset_session=1"

driver = webdriver.Chrome()

try:
    driver.get(ENTRY_URL)
    time.sleep(0.8)

    driver.get(f"{BASE_URL}/login")
    time.sleep(0.5)
    driver.find_element(By.ID, "inputBox").send_keys("fastbot@example.com")
    driver.find_element(By.NAME, "password").send_keys("fastpass123")
    driver.find_element(By.NAME, "remember_me").click()
    driver.find_element(By.ID, "btn").click()

    driver.get(f"{BASE_URL}/search")
    time.sleep(0.5)
    driver.find_element(By.ID, "inputBox").send_keys("coordinated bot alert")
    driver.find_element(By.ID, "btn").click()
    driver.find_element(By.ID, "link1").click()
    driver.find_element(By.ID, "link2").click()

    driver.get(f"{BASE_URL}/browse")
    time.sleep(0.5)
    driver.find_element(By.ID, "link1").click()
    driver.find_element(By.ID, "link2").click()
    driver.find_element(By.ID, "btn").click()
    driver.execute_script("window.scrollTo(0, 700);")
    driver.execute_script("window.scrollTo(0, 1400);")

    driver.get(f"{BASE_URL}/form")
    time.sleep(0.5)
    driver.find_element(By.ID, "inputBox").send_keys("Fast Bot")
    text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    if len(text_inputs) > 1:
        text_inputs[1].send_keys("Automation Lab")
    driver.find_element(By.TAG_NAME, "textarea").send_keys("Submitting robotic application flow.")
    driver.find_element(By.ID, "btn").click()

    time.sleep(1.5)

finally:
    driver.quit()
