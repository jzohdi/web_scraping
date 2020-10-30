import csv
import json
from excel_writer import XLWriter
from scraper import WriterHelper

index = 1

cache = set()
xl_helper = WriterHelper(1, XLWriter())
xl_helper.init_xl(["Index", "City", "Name", "Region", "Address", "Phone"])

with open("detailed_output.txt", "r") as file:
    curr_line = [index]

    for line in file:
        if not line.strip():

            string = json.dumps(curr_line[1:])

            if not (string in cache):
                cache.add(string)
                xl_helper.add_row(curr_line)
                index += 1
                curr_line = [index]

        else:
            info = line.split(":", 1)[1].strip()
            curr_line.append(info)

xl_helper.save("Veovert")
