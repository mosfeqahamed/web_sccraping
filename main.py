import os
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from pymongo import MongoClient


API_KEY = os.getenv("API_KEY")

save_dir = "github_profile_images"
os.makedirs(save_dir, exist_ok=True)

excel_path = "github_profile_data.xlsx"


MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://mosfeqahamednayim:whijxe6krx2ISHw8@cluster0.lqxizda.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

client = MongoClient(MONGO_URI)
db = client["web_scraping"]
collection = db["scraping"]


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_text_or_none(by, value):
    """Helper function to get text from an element."""
    try:
        return driver.find_element(by, value).text.strip()
    except:
        return None

def get_attr_or_none(by, value, attr):
    """Helper function to get attribute value from an element."""
    try:
        return driver.find_element(by, value).get_attribute(attr)
    except:
        return None

while True:
    github_user = input('Input GitHub User (Press "y" to exit): ')

    if github_user.lower() == 'y':
        print("Exiting program...")
        break

 
    df_existing = pd.read_excel(excel_path) if os.path.exists(excel_path) else pd.DataFrame()
    
    checker = 0

    
    if "Username" in df_existing.columns and github_user.lower() in df_existing["Username"].str.lower().values:
        existing_row = df_existing[df_existing["Username"].str.lower() == github_user.lower()].iloc[0]
        checker = 1
        print("User already exists. Checking for updates...")

   
    url = f'https://github.com/{github_user}'

    driver.get(url)

    new_data = {
        "Username": github_user,
        "ImagePath": get_attr_or_none(By.XPATH, "//img[contains(@class,'avatar-user')]", "src"),
        "RepositoryCount": get_text_or_none(By.XPATH, '//a[contains(@href, "?tab=repositories")]/span'),
        "GitHubLink": url,
        "Location": get_text_or_none(By.XPATH, "//li[@itemprop='homeLocation']/span[@class='p-label']"),
        "WebsiteLink": get_attr_or_none(By.XPATH, "//li[@itemprop='url']/a[@rel='nofollow me']", "href"),
        "LastUpdated": datetime.utcnow()
    }

    
    social_links = []
    social_platforms = ["twitter", "linkedin", "facebook", "instagram"]
    links = driver.find_elements(By.XPATH, "//a[@rel='nofollow me']")
    for link in links:
        href = link.get_attribute("href")
        if any(platform in href for platform in social_platforms):
            social_links.append(href)

    new_data["Social Media"] = ", ".join(social_links)
    
    

  
    if "Username" in df_existing.columns and github_user.lower() in df_existing["Username"].str.lower().values:
        has_changes = False
        for key, value in new_data.items():
            if key in existing_row and str(existing_row[key]) != str(value):
                has_changes = True
                break

        if has_changes:
           
            collection.update_one({"Username": github_user}, {"$set": new_data})
            print(f"✅ User '{github_user}' data updated in MongoDB.")

           
            df_existing.loc[df_existing["Username"].str.lower() == github_user.lower(), new_data.keys()] = new_data.values()
            df_existing.to_excel(excel_path, index=False)
            print("✅ Excel file updated with new data.")

        else:
            print(f"No changes detected for '{github_user}'.")

    else:
        
        collection.insert_one(new_data)
        print(f"New user '{github_user}' data saved to MongoDB.")

        
        df_new = pd.DataFrame([new_data])
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_excel(excel_path, index=False)
        print("New user data appended to 'github_profile_data.xlsx'")

driver.quit()
client.close()
