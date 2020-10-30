from scrapers.ecotourisme import Scraper
from scrapers.helpers.writer import XLWriter

def main():
    cols = ["name", "owner", "address", "phone", "contact", "details"]
    xl_writer = XLWriter()
    
    scraper = Scraper("https://www.ecotourisme-pays-alo.com/vos-vacances-chez-nous/h%C3%A9bergements/")
    data = scraper.run()
    
    
    xl_writer.create("eco_tourisme_2.xlsx")
    xl_writer.init_sheet()
    xl_writer.batch_add_row(data)
    # xl_writer.new_sheet(cols)
    # xl_writer.batch_put(data)
    xl_writer.save()

if __name__ == "__main__":
    main()


