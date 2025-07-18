from .config import mongo_host, mongo_username, mongo_password, mongo_port, options
from .ScrapeSession import ScrapeSession

session = None
def start():
    """This function should be called from outside when the scraping session should start"""
    global session
    # Initialize the ScrapeSession
    session = ScrapeSession(
        mongo_host=mongo_host,
        mongo_username=mongo_username,
        mongo_password=mongo_password,
        mongo_port=mongo_port,
        chrome_options=options # Generated at config.py
    )