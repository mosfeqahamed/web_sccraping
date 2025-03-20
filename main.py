import os
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


save_dir = "github_profile_images"
os.makedirs(save_dir, exist_ok=True)

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


github_user = input('Input GitHub User: ')
url = f'https://github.com/{github_user}'

driver.get(url)

try:
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