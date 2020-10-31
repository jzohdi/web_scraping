import os
from private.ecotourisme import Scraper
from helpers.writer import XLWriter
from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only

load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

def main():
    cols = ["name", "owner", "address", "phone", "contact", "details"]
    output_filename = "eco_tourisme_2.xlsx"
    endpoint = os.getenv("URL")

    if endpoint is None:
        print("endpoint url is None")

        exit(1)

    xl_writer = XLWriter()
    scraper = Scraper(endpoint)
    data = scraper.run()
    
    
    xl_writer.create(output_filename)
    xl_writer.init_sheet()
    xl_writer.batch_add_row(data)
    # xl_writer.new_sheet(cols)
    # xl_writer.batch_put(data)
    xl_writer.save()

if __name__ == "__main__":
    main()


