from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

NAME = 'Julius Pacheco, Davison (Wrestling)'
BUTTON_TEXT = 'Vote'
URL = 'https://www.mlive.com/highschoolsports/2026/02/vote-honoring-our-flint-area-athlete-of-the-week-for-feb-2-8.html?gift=47ef2fd1-54e6-425f-8aff-d653ebe6ecd3'

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

iterations = int(input("Enter the number of iterations to run: \n"))

driver = webdriver.Chrome(options=options)

for i in range(iterations):
    print("Starting iteration: ", i + 1)
    driver.get(URL)

    answer_groups = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.css-answer-group.pds-answer-group")
        )
    )

    for answer in answer_groups:
        if NAME in answer.text.strip():
            # find the clickable span inside
            span = answer.find_element(By.CSS_SELECTOR, "span.css-answer-span.pds-answer-span")

            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", span)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(span))
            span.click()
            time.sleep(1)
            break
        
    vote_btn = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, f"//button[normalize-space()='{BUTTON_TEXT}']"))
    )

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", vote_btn)

    vote_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space()='{BUTTON_TEXT}']"))
    )
    vote_btn.click()

    feedback_element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "li.pds-feedback-group")
        )
    )

    print("Vote cast and feedback screen detected.")

driver.quit()
