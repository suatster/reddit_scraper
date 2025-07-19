from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
import time

from .scrape_site import scrape_site

def scrape_search(session, query, num_links_to_find):
    """Returns true if nothing goes wrong. In case of a critical non-exceptional error, returns false."""
    clean_query = ' '.join(query.split()).replace(' ', '+')
    if num_links_to_find <= 0:
        logging.error("Number of links must be positive.")
        return False

    search_url = "https://www.reddit.com/search/?q=" + query
    session.driver.get(search_url)
    links = set()

    try:
        WebDriverWait(session.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="post-title"]'))
        )
        logging.info("Search results loaded.")
    except TimeoutException:
        logging.error("Timeout waiting for search results.")
        
        """The following code captures the current state of 
        the page and saves it within docker, useful when we
        get detected as a bot and it's time to reset/change
        VPNs."""
        # --- START DIAGNOSTIC CAPTURE ---
        timestamp = int(time.time()) # To make filenames unique
        screenshot_path = f"/app/debug_screenshot_search_timeout_{timestamp}.png"
        page_source_path = f"/app/debug_page_source_search_timeout_{timestamp}.html"

        logging.error(f"Attempting to capture diagnostics for URL: {session.driver.current_url}")

        try:
            session.driver.save_screenshot(screenshot_path)
            logging.error(f"Saved screenshot to {screenshot_path}")
        except WebDriverException as e:
            logging.error(f"Failed to save screenshot (WebDriverException): {e}")
        except Exception as e:
            logging.error(f"Failed to save screenshot (General Error): {e}")

        try:
            with open(page_source_path, "w", encoding="utf-8") as f:
                f.write(session.driver.page_source)
            logging.error(f"Saved page source to {page_source_path}")
        except WebDriverException as e:
            logging.error(f"Failed to save page source (WebDriverException): {e}")
        except Exception as e:
            logging.error(f"Failed to save page source (General Error): {e}")
        # --- END DIAGNOSTIC CAPTURE ---
        return False

    last_height = session.driver.execute_script("return document.body.scrollHeight")
    while len(links) < num_links_to_find:
        session.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        new_height = session.driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            logging.warning("No new content loaded. Breaking scroll loop.")
            break
        last_height = new_height

        link_tags = session.driver.find_elements(By.CSS_SELECTOR, '[data-testid="post-title"]')
        for link_tag in link_tags:
            link_to_add = link_tag.get_attribute("href")
            if "/comments/" in link_to_add:
                links.add(link_to_add)

        logging.info(f"Currently found {len(links)} unique links on the page. Target: {num_links_to_find}")

    final_links = list(links)[:num_links_to_find]
    total_links_to_scrape_for_session = len(final_links)
    logging.info(f"\nInitiating scraping for {total_links_to_scrape_for_session} links for the query '{query}'.")

    session.total_links_to_scrape_for_session = total_links_to_scrape_for_session


    curr_link = 1
    failed_links_count = 0   
    for link in final_links:
        logging.info(f"Scraping link #{curr_link} with url: {link}.")
        if not scrape_site(session, link, total_links_to_scrape_for_session, query=clean_query.replace('+', '_')):
            logging.error(f"Error on link #{curr_link} with url: {link}.")
            failed_links_count += 1
        curr_link += 1

    if failed_links_count == total_links_to_scrape_for_session:
        logging.error("Found results, but couldn't scrape any.")
        return False
    
    
    return True