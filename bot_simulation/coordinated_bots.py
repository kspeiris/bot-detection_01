from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import time

BASE_URL = "http://127.0.0.1:5000"
ENTRY_URL = f"{BASE_URL}/?actor_type=bot&bot_type=coordinated&reset_session=1"


def run_bot(bot_name):
    driver = webdriver.Chrome()
    try:
        driver.get(ENTRY_URL)
        time.sleep(0.8)

        driver.get(f"{BASE_URL}/login")
        time.sleep(0.8)
        driver.find_element(By.ID, "inputBox").send_keys(f"{bot_name}@example.com")
        driver.find_element(By.NAME, "password").send_keys("coord123")
        driver.find_element(By.ID, "btn").click()

        driver.get(f"{BASE_URL}/search")
        time.sleep(0.6)
        driver.find_element(By.ID, "inputBox").send_keys(bot_name)
        driver.find_element(By.ID, "btn").click()
        driver.find_element(By.ID, "link1").click()
        time.sleep(0.3)
        driver.find_element(By.ID, "link2").click()

        driver.get(f"{BASE_URL}/browse")
        time.sleep(0.6)
        driver.find_element(By.ID, "link1").click()
        time.sleep(0.3)
        driver.execute_script("window.scrollTo(0, 650);")
        time.sleep(0.3)
        driver.find_element(By.ID, "link2").click()
        time.sleep(0.3)
        driver.execute_script("window.scrollTo(0, 1200);")

        driver.get(f"{BASE_URL}/form")
        time.sleep(0.6)
        driver.find_element(By.ID, "inputBox").send_keys(bot_name)
        text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
        if len(text_inputs) > 1:
            text_inputs[1].send_keys("Coordinated Operations")
        driver.find_element(By.TAG_NAME, "textarea").send_keys("Coordinated submission pattern.")
        time.sleep(0.3)
        driver.find_element(By.ID, "btn").click()

        time.sleep(1.2)

    finally:
        driver.quit()


threads = []

for index in range(3):
    thread = threading.Thread(target=run_bot, args=(f"coord_bot_{index}",))
    threads.append(thread)

for thread in threads:
    thread.start()
    time.sleep(0.2)

for thread in threads:
    thread.join()
