from typing import List, Set, Dict, Tuple, Optional
from abc import ABCMeta, abstractmethod
import xlsxwriter

class XLWriterInterface:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0.0"

    """ creates a sheat with the header passed in as the first row """
    @abstractmethod
    def create(self, file_name: str): raise NotImplementedError 

    @abstractmethod
    def new_sheet(self, header:List): raise NotImplementedError

    """ 
        adds the row to the sheet. 
        should add the row to the lowest open row, 
        unless row_index, or col_index are given. 
    """
    @abstractmethod
    def add_row(self, row:List=None, row_index:int=None,col_index:int=None):
        raise NotImplementedError

    @abstractmethod
    def batch_add_row(self, rows: List[List]): raise NotImplementedError

    """
        Requires self.curr_cols
        takes a dict and puts the data into the
        self.curr_sheet by order of self.curr_cols
    """
    @abstractmethod
    def put(self, data: Dict): raise NotImplementedError

    @abstractmethod
    def batch_put(self, data: List[Dict]): raise NotImplementedError

    @abstractmethod
    def save(self): raise NotImplementedError

class XLWriter(XLWriterInterface):
    
    def __init__(self):
        self.__index = 0
        self.workbook = None 
        self.curr_sheet = None
        self.curr_cols: List = None

    def create(self, file_name):
        self.workbook = xlsxwriter.Workbook(file_name)
    
    def init_sheet(self):
        if self.workbook is None:
            raise Exception("no workbook has been initialized")
        self.curr_sheet = self.workbook.add_worksheet()

    def new_sheet(self, header: List=None):
        
        if self.workbook is None:
            raise Exception("no workbook has been initialized")

        self.curr_sheet = self.workbook.add_worksheet()
        self.curr_cols = header
        
        if header is None:
            return
        for i in range(len(header)):
            self.curr_sheet.write(self.__index, i, header[i])
        self.__index += 1

    def add_row(self, row: List, row_index:int=None, col_index:int=None):
        if self.workbook is None:
            raise Exception("no workbook has been initialized")
        if self.curr_sheet is None:
            raise Exception("no sheet found")

        if row_index is None:
            row_index = self.__index
            self.__index += 1

        for i in range(len(row)):
            item = row[i]

            if col_index is not None:
                i += col_index

            self.curr_sheet.write(row_index, i, item)
   
    
    def batch_add_row(self, rows: List[List]):
        for row in rows:
            self.add_row(row)

    def put(self, data: Dict):
        if self.curr_cols is None:
            raise Exception("not valid as new_sheet either has not been called, or was not called with initialize header arguement (arg 1)")
        
        for i in range(len(self.curr_cols)):
            col = self.curr_cols[i]
            item = data.get(col, "N/A")
            self.curr_sheet.write(self.__index, i, item)
        
        self.__index += 1

    def batch_put(self, data: List[Dict]):
        for item in data:
            self.put(item)

    def save(self):
        self.workbook.close()

class WriterHelper:
    def __init__(self, start_index, writer:XLWriterInterface=None):
        self.index = start_index
        self.xlwriter =  XLWriter()
        if writer is not None:
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
