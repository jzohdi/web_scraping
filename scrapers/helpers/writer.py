class WriterHelper:
    def __init__(self, start_index, writer):
        self.index = start_index
        self.xlwriter = writer

    def init_xl(self, header):
        self.xlwriter.add_sheet(header)

    def add_to_xl(self, result):
        to_list = self.format_result(self.index, result)
        if to_list:
            self.xlwriter.add_row(to_list)
            self.index += 1

    def add_row(self, row):
        if row:
            self.xlwriter.add_row(row)
            self.index += 1

    def save(self, name):
        self.xlwriter.save_as(name)

    def format_result(self, index, result):
        try:
            new_list = [index]
            new_list.append(result["type"])
            new_list.append(result["name"])
            new_list.append(result["address"])
            new_list.append(result["info"])
            new_list.append(result["Characteristiques"])
            return new_list
        except:
            print("one or more fields not given in result")
            print("input was :")
            print(result)
            return []
