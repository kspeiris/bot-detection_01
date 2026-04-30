import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://127.0.0.1:5000"
ENTRY_URL = f"{BASE_URL}/?actor_type=bot&bot_type=coordinated&reset_session=1"
WAIT_SECONDS = 10


def wait_for(driver, by, value):
    return WebDriverWait(driver, WAIT_SECONDS).until(EC.presence_of_element_located((by, value)))


def run_bot(bot_name):
    driver = webdriver.Chrome()
    try:
        driver.get(ENTRY_URL)
        time.sleep(0.8)

        driver.get(f"{BASE_URL}/login")
        time.sleep(0.8)
        wait_for(driver, By.ID, "loginEmail").send_keys(f"{bot_name}@example.com")
        wait_for(driver, By.ID, "loginPassword").send_keys("coord123")
        wait_for(driver, By.ID, "loginSubmit").click()

        driver.get(f"{BASE_URL}/search")
        time.sleep(0.6)
        wait_for(driver, By.ID, "searchQuery").send_keys(bot_name)
        wait_for(driver, By.ID, "searchAction").click()
        wait_for(driver, By.ID, "searchResultAlertDigest").click()
        time.sleep(0.3)
        wait_for(driver, By.ID, "searchResultCoordinationReview").click()

        driver.get(f"{BASE_URL}/browse")
        time.sleep(0.6)
        wait_for(driver, By.ID, "browseOpenBrief").click()
        time.sleep(0.3)
        driver.execute_script("window.scrollTo(0, 650);")
        time.sleep(0.3)
        wait_for(driver, By.ID, "browseReviewTimeline").click()
        time.sleep(0.3)
        wait_for(driver, By.ID, "bookmarkInsight").click()
        time.sleep(0.3)
        driver.execute_script("window.scrollTo(0, 1200);")

        driver.get(f"{BASE_URL}/form")
        time.sleep(0.6)
        wait_for(driver, By.ID, "fullName").send_keys(bot_name)
        wait_for(driver, By.ID, "organisation").send_keys("Coordinated Operations")
        wait_for(driver, By.ID, "useCase").send_keys("Coordinated submission pattern.")
        time.sleep(0.3)
        wait_for(driver, By.ID, "formSubmit").click()

        time.sleep(1.2)

    finally:
        driver.quit()


def main():
    threads = []

    for index in range(3):
        thread = threading.Thread(target=run_bot, args=(f"coord_bot_{index}",))
        threads.append(thread)

    for thread in threads:
        thread.start()
        time.sleep(0.2)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
