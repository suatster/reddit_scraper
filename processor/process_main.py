from scrape_processor.ProcessSession import ProcessSession

def main():
    """Main function to run the ProcessSession."""
    session = ProcessSession()
    session.constantly_process()
        
if __name__ == "__main__":
    main()