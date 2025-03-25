import os
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint
import pandas as pd

API_KEY = os.getenv("API_KEY")



save_dir = "github_profile_images"
os.makedirs(save_dir, exist_ok=True)

excel_path = "github_profile_data.xlsx"

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


github_user = input('Input GitHub User: ')

if os.path.exists(excel_path):
    df_existing = pd.read_excel(excel_path)
    if github_user.lower() in df_existing["Username"].str.lower().values:
        print("User already exists.")
        exit() 
        
url = f'https://github.com/{github_user}'

driver.get(url)

"""try:
    profile_image = driver.find_element(By.XPATH, "//img[contains(@class, 'avatar-user')]").get_attribute("src")
    print(profile_image)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
    image_filename = f"profile_{timestamp}.jpg" 
    image_path = os.path.join(save_dir, image_filename)
    img_data = requests.get(profile_image).content
    with open(image_path, 'wb') as f:
        f.write(img_data)

    print(f"Profile image saved at: {image_path}")
except:
    print("Profile image not found!")

driver.quit()

def rename_images():
    path = save_dir
    i = 0
    for filename in sorted(os.listdir(path)):  # Sort files for consistent numbering
        if filename.endswith(".jpg"):  # Process only image files
            my_dest = f"image{i}.jpg"
            my_source = os.path.join(path, filename)
            my_dest = os.path.join(path, my_dest)
            os.rename(my_source, my_dest)
            i += 1


rename_images()



city = input("Enter a city: ")

base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

response = requests.get(base_url)

if response.status_code == 200:
    weather_data = response.json()
    pprint(weather_data)
else:
    print(f"Error: Unable to fetch weather data (Status Code: {response.status_code})")"""

def get_text_or_none(by, value):
    try:
        return driver.find_element(by, value).text.strip()
    except:
        return None

def get_attr_or_none(by, value, attr):
    try:
        return driver.find_element(by, value).get_attribute(attr)
    except:
        return None

data = {
     "Username": github_user,
    "ImagePath": get_attr_or_none(By.XPATH, "//img[contains(@class,'avatar-user')]", "src"),
    "RepositoryCount": get_text_or_none(By.XPATH, '//a[contains(@href, "?tab=repositories")]/span'),
    "GitHubLink": url,
    "Location": get_text_or_none(By.XPATH, "//li[@itemprop='homeLocation']/span[@class='p-label']"),
    "WebsiteLink": get_attr_or_none(By.XPATH, "//li[@itemprop='url']/a[@rel='nofollow me']", "href"),
    #"SocialMediaLink": get_attr_or_none(By.XPATH, '//li[@itemprop="twitter"]//a', "href")
    
}
social_links = []
social_platforms = ["twitter", "linkedin", "facebook", "instagram"]
links = driver.find_elements(By.XPATH, "//a[@rel='nofollow me']")
for link in links:
    href = link.get_attribute("href")
    if any(platform in href for platform in social_platforms):
        social_links.append(href)

data["Social Media"] = ", ".join(social_links)

driver.quit()



df_new = pd.DataFrame([data])
if os.path.exists(excel_path):
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined.to_excel(excel_path, index=False)
    print(" New user data appended to 'github_profile_data.xlsx'")
else:
    df_new.to_excel(excel_path, index=False)
    print("File created and data saved to 'github_profile_data.xlsx'")