from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import random
import time

BASE_URL = "http://127.0.0.1:5000"
ENTRY_URL = f"{BASE_URL}/?actor_type=bot&bot_type=human_like&reset_session=1"


def slow_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.08, 0.25))


driver = webdriver.Chrome()

try:
    actions = ActionChains(driver)

    driver.get(ENTRY_URL)
    time.sleep(random.uniform(1.0, 1.8))

    driver.get(f"{BASE_URL}/login")
    time.sleep(random.uniform(0.8, 1.5))
    email = driver.find_element(By.ID, "inputBox")
    password = driver.find_element(By.NAME, "password")
    remember = driver.find_element(By.NAME, "remember_me")
    submit = driver.find_element(By.ID, "btn")

    actions.move_to_element(email).perform()
    time.sleep(random.uniform(0.3, 0.8))
    slow_type(email, "humanlikebot@example.com")
    actions.move_to_element(password).perform()
    time.sleep(random.uniform(0.3, 0.8))
    slow_type(password, "research123")
    time.sleep(random.uniform(0.2, 0.6))
    remember.click()
    time.sleep(random.uniform(0.4, 0.9))
    actions.move_to_element(submit).perform()
    time.sleep(random.uniform(0.3, 0.8))
    submit.click()

    driver.get(f"{BASE_URL}/search")
    time.sleep(random.uniform(0.8, 1.4))
    search_box = driver.find_element(By.ID, "inputBox")
    search_button = driver.find_element(By.ID, "btn")
    link1 = driver.find_element(By.ID, "link1")
    link2 = driver.find_element(By.ID, "link2")

    actions.move_to_element(search_box).perform()
    time.sleep(random.uniform(0.4, 0.9))
    slow_type(search_box, "behavioural fingerprint coordination")
    time.sleep(random.uniform(0.4, 1.0))
    search_button.click()
    time.sleep(random.uniform(0.4, 0.9))
    actions.move_to_element(link1).perform()
    time.sleep(random.uniform(0.3, 0.7))
    link1.click()
    time.sleep(random.uniform(0.4, 0.8))
    actions.move_to_element(link2).perform()
    time.sleep(random.uniform(0.3, 0.7))
    link2.click()

    driver.get(f"{BASE_URL}/browse")
    time.sleep(random.uniform(0.8, 1.4))
    browse_link1 = driver.find_element(By.ID, "link1")
    browse_link2 = driver.find_element(By.ID, "link2")
    bookmark = driver.find_element(By.ID, "btn")
    actions.move_to_element(browse_link1).perform()
    time.sleep(random.uniform(0.4, 0.8))
    browse_link1.click()
    time.sleep(random.uniform(0.5, 1.0))
    driver.execute_script("window.scrollTo(0, 450);")
    time.sleep(random.uniform(0.4, 0.8))
    driver.execute_script("window.scrollTo(0, 980);")
    time.sleep(random.uniform(0.4, 0.9))
    actions.move_to_element(browse_link2).perform()
    time.sleep(random.uniform(0.4, 0.8))
    browse_link2.click()
    time.sleep(random.uniform(0.4, 0.8))
    bookmark.click()

    driver.get(f"{BASE_URL}/form")
    time.sleep(random.uniform(0.8, 1.3))
    name_box = driver.find_element(By.ID, "inputBox")
    text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
    org_box = text_inputs[1] if len(text_inputs) > 1 else text_inputs[0]
    textarea = driver.find_element(By.TAG_NAME, "textarea")
    submit = driver.find_element(By.ID, "btn")

    actions.move_to_element(name_box).perform()
    time.sleep(random.uniform(0.4, 0.9))
    slow_type(name_box, "Human Like Bot")
    time.sleep(random.uniform(0.4, 0.9))
    slow_type(org_box, "Behaviour Research Group")
    time.sleep(random.uniform(0.4, 0.9))
    slow_type(textarea, "Reviewing behaviour patterns with slower, varied interaction.")
    time.sleep(random.uniform(0.5, 1.0))
    submit.click()

    time.sleep(1.5)

finally:
    driver.quit()
