import logging
import requests

def scrape_site(session, req_address, total_links_to_scrape=None, coming_from_search=True, query=None):
    """Ready a Reddit post for scraping using Selenium WebDriver. Returns True if successful, False otherwise."""
    
    if coming_from_search and not query:
        logging.error("Query must be provided when coming from search.")
        return False

    if not coming_from_search:
        url_parts = req_address.split('/')
        if req_address.startswith("https://www.reddit.com") or not len(url_parts) >= 7 and url_parts[2] == 'www.reddit.com' and url_parts[3] == 'r' and url_parts[5] == 'comments':
            req_id = url_parts[6]
            subreddit = url_parts[4]
        else:
            logging.error("Invalid Reddit URL format, quitting...")
            return False
        test_req = requests.head(req_address)
        if test_req.status_code != 200:
            logging.error(f"Couldn't connect to URL: {req_address}. Status Code: {test_req.status_code}")
            logging.error("Please ensure the URL is correct and accessible.")
            return False

    session.collection = session.database["tmp_links"]
    # Save the html
    doc = {
        "url": req_address,
        "total_links_to_scrape": total_links_to_scrape,
        "destination_collection": f"search_{query}" if coming_from_search else f"{subreddit}_{req_id}"
    }
    session.collection.insert_one(doc)
    logging.info(f"Saved URL to DB: {req_address}")
    return True