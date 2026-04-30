import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://127.0.0.1:5000"
ENTRY_URL = f"{BASE_URL}/?actor_type=bot&bot_type=fast&reset_session=1"
WAIT_SECONDS = 10


def wait_for(driver, by, value):
    return WebDriverWait(driver, WAIT_SECONDS).until(EC.presence_of_element_located((by, value)))


def main():
    driver = webdriver.Chrome()

    try:
        driver.get(ENTRY_URL)
        time.sleep(0.8)

        driver.get(f"{BASE_URL}/login")
        time.sleep(0.5)
        wait_for(driver, By.ID, "loginEmail").send_keys("fastbot@example.com")
        wait_for(driver, By.ID, "loginPassword").send_keys("fastpass123")
        wait_for(driver, By.NAME, "remember_me").click()
        wait_for(driver, By.ID, "loginSubmit").click()

        driver.get(f"{BASE_URL}/search")
        time.sleep(0.5)
        wait_for(driver, By.ID, "searchQuery").send_keys("coordinated bot alert")
        wait_for(driver, By.ID, "searchAction").click()
        wait_for(driver, By.ID, "searchResultAlertDigest").click()
        wait_for(driver, By.ID, "searchResultCoordinationReview").click()

        driver.get(f"{BASE_URL}/browse")
        time.sleep(0.5)
        wait_for(driver, By.ID, "browseOpenBrief").click()
        wait_for(driver, By.ID, "browseReviewTimeline").click()
        wait_for(driver, By.ID, "bookmarkInsight").click()
        driver.execute_script("window.scrollTo(0, 700);")
        driver.execute_script("window.scrollTo(0, 1400);")

        driver.get(f"{BASE_URL}/form")
        time.sleep(0.5)
        wait_for(driver, By.ID, "fullName").send_keys("Fast Bot")
        wait_for(driver, By.ID, "organisation").send_keys("Automation Lab")
        wait_for(driver, By.ID, "useCase").send_keys("Submitting robotic application flow.")
        wait_for(driver, By.ID, "formSubmit").click()

        time.sleep(1.5)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
