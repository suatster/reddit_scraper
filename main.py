# Orchestrator script for ease usage

import argparse
import logging
import subprocess
import sys #to check if the script is run with -n or --num


logging.basicConfig(level=logging.INFO, filename='orchestrator_log.txt', filemode='a', format='%(asctime)s %(levelname)s: %(message)s')
# Add console handler to print logs to console as well
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

def main():
    logging.info("Starting orchestrator script...")
    try:
        parser = argparse.ArgumentParser(description="Orchestrator for running scripts with specified parameters.")
        group = parser.add_mutually_exclusive_group(required=False)
        group.add_argument("-u", "--url", type=str, help="The URL to scrape")
        group.add_argument("-s", "--search", type=str, help="The search term to use")
        parser.add_argument("-n", "--num", type=int, default=10, help="Number of results to return (default: 10)")
        group2 = parser.add_mutually_exclusive_group(required=False)
        group2.add_argument("--noui", action="store_true", help="Run the scraper in CLI mode.")
        group2.add_argument("--ui", action="store_true", help="Run the scraper in UI mode (default).")
        args = parser.parse_args()
        
        
        container_name = "reddit_scraper_explorer"  # Adjust if your container name is different
        def is_container_running(name):
            try:
                result = subprocess.run([
                    "docker", "inspect", "-f", "{{.State.Running}}", name
                ], capture_output=True, text=True, check=True)
                return result.stdout.strip() == "true"
            except subprocess.CalledProcessError:
                return False

        if not is_container_running(container_name):
            logging.error(f"Container '{container_name}' is not running. Please start it with 'docker-compose up -d' before running this script.")
            return

        if args.noui:
            if args.search:
                logging.info(f"Running scraper with search term: {args.search} and number of results: {args.num}")
                subprocess.run([
                    "docker", "exec", "-i", container_name,
                    "python", "explorer/explorer_main.py",
                    "-s", args.search,
                    "-n", str(args.num), "--noui"
                ], check=True)
                if args.num == 10 and not any(arg in ['-n', '--num'] for arg in sys.argv):
                    logging.warning("Using default number of results: 10, use -n or --num to specify number.")
            elif args.url:
                logging.info(f"Running scraper with URL: {args.url}")
                subprocess.run([
                    "docker", "exec", "-i", container_name,
                    "python", "explorer/explorer_main.py",
                    "-u", args.url, "--noui"
                ], check=True)
            else:
                logging.error("No valid arguments provided. Please specify either a search term or a URL.")
                parser.print_help()
        else:
            subprocess.run([
                "docker", "exec", "-it", container_name,
                "python", "explorer/explorer_main.py", "--ui"
            ], check=True)

    except argparse.ArgumentError as e:
        logging.error(f"Argument parsing error: {e}")
        parser.print_help()
    except subprocess.CalledProcessError as e:
        logging.error(f"An error occurred while running the subprocess: {e}")
    except KeyboardInterrupt:
        logging.info("Process interrupted by user. Exiting gracefully...")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        logging.info("Orchestrator script finished execution.")

if __name__ == "__main__":
    main()