from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


github_user = input('Input GitHub User: ')
url = f'https://github.com/{github_user}'

driver.get(url)

try:
    profile_image = driver.find_element(By.XPATH, "//img[contains(@class, 'avatar-user')]").get_attribute("src")
    print(profile_image)
except:
    print("Profile image not found!")

driver.quit()
