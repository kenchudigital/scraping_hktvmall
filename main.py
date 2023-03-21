from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.get("https://www.hktvmall.com/")

elem = driver.find_element(By.CSS_SELECTOR, '.SuggestionSearch-input')

elem.send_keys("魚")
elem.send_keys(Keys.ENTER)

time.sleep(5)

all_products = []

while True:
    product_brief_list = driver.find_element(By.CSS_SELECTOR, '.product-brief-list')

    for product_brief in product_brief_list.find_elements(By.CSS_SELECTOR, '.product-brief-wrapper'):
        title = product_brief.find_element(By.CSS_SELECTOR, '.brand-product-name>h4').text
        price = product_brief.find_element(By.CSS_SELECTOR, '.price').text
        all_products.append([title, price])

    next_btn = driver.find_element(By.CSS_SELECTOR, "#paginationMenu_nextBtn")

    if next_btn.get_attribute("class") == "disabled":
        break

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    next_btn.click()

    time.sleep(5)


df = pd.DataFrame()
df['product'] = all_products
df.to_csv('demo.csv')

