import os
import csv
import logging
from myvariables import CSVvariables

class CSVOperations:
    def __init__(self):
        self.FolderPath = CSVvariables.FolderPath
        self.CSVfiles = []
        self.CSVinStringForm = []
    
    def GetListOfCSVFiles(self):
        for file in os.listdir(self.FolderPath):
            if file.endswith(".csv"):
                self.CSVfiles.append(file)

    def CreateStringFromCSV(self):
        for file in self.CSVfiles:
            file=self.FolderPath+file
            with open(file) as csv_file:
                csv_reader = csv.reader(csv_file,delimiter=',')
                line_count = 0
                header = []
                content = ""
                for row in csv_reader:
                    if line_count == 0:
                        if isinstance(row,list):
                            header = row
                        else:
                            header=[row]
                        line_count+=1
                        if not header:
                            logging.warning("Empty header, skipping file: %s",file)
                            break
                    else:
                        try:
                            if content != "":
                                content=content+";"
                            for item in row:
                                if content == "":
                                    content=content+item
                                else:
                                    if content.endswith(";"):
                                        content=content+item
                                    else:
                                        content=content+","+item
                        except:
                            logging.error("error in the logic of creating string from a CSV file")
                            exit(1)
                CSVinStringForm = [header,content]
                self.CSVinStringForm.append(CSVinStringForm)
                csv_file.close()


