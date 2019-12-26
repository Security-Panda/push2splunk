from CSVOperations import CSVOperations
from splunkrestapi import SplunkLookupActions
from splunkrestapi import SplunkAPISearch

def main():
    CSVOperate = CSVOperations()
    CSVOperate.GetListOfCSVFiles()
    CSVOperate.CreateStringFromCSV()

    Lookuppush = SplunkLookupActions()
    Lookuppush.pushCSVStringToLookup(CSVOperate.CSVfiles,CSVOperate.CSVinStringForm)

    SplunkSearch = SplunkAPISearch()
    SplunkSearch.DoSearchOnSplunk(Lookuppush.SplunkSearch)



if __name__ == "__main__":
    main()