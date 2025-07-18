from pymongo import MongoClient
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import logging
import os
import time

class ScrapeSession:
    """The session as a class"""
    def __init__(
        self,
        mongo_host,
        mongo_username,
        mongo_password,
        mongo_port,
        chrome_options,
        db_name="reddit_scrapes", # Default database name
        chrome_log_output=os.devnull 
    ):
        self.mongo_host = mongo_host
        self.mongo_username = mongo_username
        self.mongo_password = mongo_password
        self.mongo_port = mongo_port
        self.db_name = db_name
        self.chrome_options = chrome_options
        self.chrome_log_output = chrome_log_output

        self.driver = None
        self.mongo_client = None
        self.database = None
        self.collection = None
        self.total_links_inserted_count = 0
        self.total_links_to_scrape_for_session = 0
        self.post_sequence_current = 0
        
        self.setup_resources()

    def setup_reddit(self):
        """This functions clicks the potential button to accept cookies, never seen one, but good to keep"""
        self.driver.get("https://www.reddit.com")
        try:
            cookie_accept_button = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree') or contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cookie') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cookie')]"))
            )
            if cookie_accept_button.is_displayed() and cookie_accept_button.is_enabled():
                self.driver.execute_script("arguments[0].click();", cookie_accept_button)
                logging.info("Clicked cookie consent button.")
                time.sleep(1)
        except TimeoutException as e:
            pass # Ignore if the button is not found, it probs doesn't exist
        except Exception as e:
            logging.error(f"Error handling cookie consent: {e}")

    def setup_resources(self):
        """Sets selenium and mongodb, credentials are from .env file"""
        chromepath = ChromeDriverManager().install()
        corrected_path = chromepath
        
        # Fix if it's the wrong file
        if "THIRD_PARTY_NOTICES" in chromepath:
            corrected_path = os.path.join(os.path.dirname(chromepath), "chromedriver")
            
        service = Service(corrected_path, log_output=self.chrome_log_output)
        try:
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
            self.setup_reddit()
        except Exception as e:
            logging.error(f"Error initializing Selenium Chrome driver: {e}")
            logging.error("Please ensure webdriver_manager is installed.")
            self.cleanup()
            return

        MONGO_URI = f"mongodb://{self.mongo_username}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/"
        try:
            self.mongo_client = MongoClient(MONGO_URI)
            self.database = self.mongo_client[self.db_name]
        except Exception as e:
            logging.error("Couldn't connect to mongodb. Please ensure credentials are correct.")
            self.cleanup()

    def set_collection_name(self, query=None, subreddit=None, post_id=None, is_search=None):
        """Sets collection name, if from search: 'search_query'; else: 'subreddit_postid'"""
        if is_search and query:
            COLLECTION_NAME = f"search_{query}"
            self.collection = self.database[COLLECTION_NAME]
        elif not is_search and not query and subreddit and post_id:
            COLLECTION_NAME = f"{subreddit}_{post_id}"
            self.collection = self.database[COLLECTION_NAME]
        else:
            logging.error("Improper parameters when setting collection name.")
            self.cleanup()

    def set_total_links_to_scrape_for_session(self, total):
        self.total_links_to_scrape_for_session = total

    def increment_inserted_count(self):
        self.total_links_inserted_count += 1

    def increment_post_sequence(self):
        self.post_sequence_current += 1

    def reset_counters(self):
        self.total_links_inserted_count = 0
        self.total_links_to_scrape_for_session = 0
        self.post_sequence_current = 0

    def cleanup(self):
        """Cleaning up after the session is used"""
        if self.driver:
            self.driver.quit()
            self.driver = None
        if self.mongo_client:
            self.mongo_client.close()
            self.mongo_client = None