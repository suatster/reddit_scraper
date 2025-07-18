# Main script for the Reddit Scraper CLI
import argparse
import logging
import sys # to check whether the script is run with -n or --num

import reddit_scraper
import reddit_scraper.scrape.scrape_site as scrape_site
import reddit_scraper.scrape.scrape_search as scrape_search


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# set arguments
parser  = argparse.ArgumentParser(description="Reddit Scraper CLI")
group = parser.add_mutually_exclusive_group(required=False)
group.add_argument("-u", "--url", type=str, help="The URL to scrape")
group.add_argument("-s", "--search", type=str, help="The search term to use")
parser.add_argument("-n", "--num", type=int, default=10, help="The number of results to return")
group2 = parser.add_mutually_exclusive_group(required=False)
group2.add_argument("--noui", action="store_true", help="Run the scraper in CLI mode.")
group2.add_argument("--ui", action="store_true", help="Run the scraper in UI mode (default).")
args = parser.parse_args()


def cli_mode():
    reddit_scraper.start()
    if args.search:
        logging.info(f"Running scraper with search term: {args.search} and number of results: {args.num}")
        if args.num == 10 and not any(arg in ['-n', '--num'] for arg in sys.argv):
            logging.warning("Using default number of results: 10. Use -n or --num to specify a different number.")
        if not scrape_search.scrape_search(reddit_scraper.session, args.search, args.num):
            logging.error("Failed to scrape search results.")
    elif args.url:
        logging.info(f"Running scraper with URL: {args.url}")
        if not scrape_site.scrape_site(reddit_scraper.session, args.url, coming_from_search=False):
            logging.error("Failed to scrape URL.")
    else:
        logging.error("No valid arguments provided. Please specify either a search term or a URL.")
        parser.print_help()


def ui_mode():
    try:
        reddit_scraper.start()
        
        # --- User Interface ---
        logging.info("Starting user interface.")
        print("""Welcome to a basic web scraper for Reddit!
            1- URL Scraping (scrape a single post by its URL)
            2- Search Scraping (search Reddit for posts and scrape multiple results)
            3- Profile Scraping (coming soon!)""")

        option = input("Please type the operation of your desires: ")

        if option == '1': # URL scraping
            req_url = input("Please enter the URL of the Reddit post: ")
            if not scrape_site.scrape_site(reddit_scraper.session, req_url, coming_from_search=False):
                logging.error("Failed to scrape url.")

        elif option == '2': # Search
            try:
                query = input("Please enter the search query: ")
                num_links = int(input("Number of links to find (e.g., 10): "))
                
                if not scrape_search.scrape_search(reddit_scraper.session, query, num_links):
                    logging.error("Failed to scrape search results.")

            except ValueError:
                logging.error("Invalid input for number of links. Please enter a valid integer.")

        elif option == '3': # Profile
            logging.error("Profile Scraping is still under development!")

        else:
            logging.error("Invalid option selected. Please choose 1, 2, or 3.")

        # Done
        logging.info("DONE!")
        input("Press enter to quit...")
        logging.info("Quitting...")
    except KeyboardInterrupt:
        logging.info("Quitting...")
    except Exception as e:
        logging.error(f"EXCEPTION: {e}")


def main():
    try:
        if args.noui:
            logging.info("Running in CLI mode.")
            cli_mode()
            
        else:
            logging.info("Running in UI mode.")
            ui_mode()
    except KeyboardInterrupt:
        logging.info("Process interrupted by user. Exiting gracefully...")
    except Exception as e:
        logging.error(f"An unexpected error occurred while setting up the parser: {e}")
    finally:
        if reddit_scraper.session:
            logging.info("Cleaning up the session.")
            reddit_scraper.session.cleanup()

if __name__ == "__main__":
    main()