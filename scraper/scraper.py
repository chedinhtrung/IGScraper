from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pickle
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os

from .creds import USERNAME, PASSWORD, TARGET_A, TARGET_B, DRIVER

current_dir = os.path.dirname(__file__)

class IGScraper:
    def __init__(self, username=USERNAME, passwd=PASSWORD, target_A=TARGET_A, target_B=TARGET_B):
        self.username = username
        self.password = passwd
        self.target_A = target_A
        self.target_B = target_B

        options = Options()
        options.add_argument("--disable-save-password-bubble")
        options.add_argument("--headless")

        self.service = Service(DRIVER)
        self.driver = webdriver.Chrome(service=self.service, options=options)
        self.login()

    
    def save_cookies(self, cookies_file=f"{current_dir}/cookies/cookies.pkl"):
        with open(cookies_file, "wb") as f:
            pickle.dump(self.driver.get_cookies(), f)
    
    def load_cookies(self, cookies_file=f"{current_dir}/cookies/cookies.pkl"):
        with open(cookies_file, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            #print(cookies)
    
    def poll_known_storynames(self):
        """
        polls the record of sus story names to check
        """
        pass

    def login(self):
        """
        login with cookies. if there isn't any, record and save the cookies
        """
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(4)
        try:
            self.load_cookies()
            self.driver.get("https://www.instagram.com")  
            time.sleep(3)  # Give it time to load the session
            print("Session loaded from cookies")
        except Exception as e:
            print("Cant load cookies", e)
            # Login manually if cookies don't exist or session is expired
            # Find the username and password input fields and login
            time.sleep(6)
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")

            # Enter credentials
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)

            # Submit the login form
            password_field.send_keys(Keys.RETURN)

            # Wait for the page to load
            time.sleep(5)

            # Save cookies for next session
            self.save_cookies()
            print("Logged in and cookies saved")

    def check_cookie(self):
        """
        check cookies expiration time against current time, if expired login again before returning results
        """
        pass

    def get_profile_image(self, profile:str):
        pass

    def get_highlights(self, profile:str):
        pass

    def get_follow(self, profile_A, profile_B):
        """
        determines if A follows B
        """
        pass

    def periodic_update_data(self):
        profile_A_url = f"https://www.instagram.com/{self.target_A}/"
        profile_B_url = f"https://www.instagram.com/{self.target_B}/"
        try:
            self.driver.get(profile_A_url)
            time.sleep(5)
            bio = self.driver.page_source
            with open(f"./{self.target_A}.html", "w", encoding='utf-8') as file:
                file.write(bio)
            print(f"Bio of {self.target_A} saved")
        except Exception as e:
            print("Error extracting bio:", e)
