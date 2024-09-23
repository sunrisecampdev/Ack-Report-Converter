from pprint import pprint
from eventdict import *

class Donor:
    def __init__(self, rowCells, indexMap, headerDict, headerOrder):
        self.rowIndex = 0
        self.properties = dict()
        self.indexMap = indexMap
        self.headerDict = headerDict
        self.headerOrder = headerOrder
        self.convertRowCellsList(rowCells, indexMap)

    def incRowIndex(self):
        self.rowIndex += 1

    def processStatus(self, eventStatus): 
        if eventStatus in event_dict:
            return event_dict[eventStatus]
        return eventStatus

    def getValueFromKey(self, key, rowCells):
        if (key == "FIRST_NAME") or (key == "LAST_NAME") or (key == "PAID"):
            return
        
        headerKeyValuePair = self.headerDict[key]

        index = self.indexMap[headerKeyValuePair["name"]]
        value = rowCells[index]

        if (key == "EVENT_STATUS"):
            return self.processStatus(value)
        return value
    
    def getNames(self, rowCells):
        """Additional processing to check if last names are different
        Takes a list of row cell values and returns a dict of First and Last name"""
        primaryLastIndex = self.indexMap[self.headerDict["PRIMARY_LAST"]["name"]]
        primaryLastValue = rowCells[primaryLastIndex]
        spouseLastIndex = self.indexMap[self.headerDict["SPOUSE_LAST"]["name"]]
        spouseLastValue = rowCells[spouseLastIndex]

        primaryFirstIndex = self.indexMap[self.headerDict["PRIMARY_FIRST"]["name"]]
        primaryFirstValue = rowCells[primaryFirstIndex]
        spouseFirstIndex = self.indexMap[self.headerDict["SPOUSE_FIRST"]["name"]]
        spouseFirstValue = rowCells[spouseFirstIndex]

        if primaryFirstValue is None and primaryLastValue is None:
            return
        
        firstNameList = []
        # no spouse
        if spouseFirstValue is None and spouseLastValue is None:
            return {"first" : primaryFirstValue, "last" : primaryLastValue}
        # same last name
        elif primaryLastValue == spouseLastValue:
            firstNameList.append(spouseFirstValue)
            firstNameList.append("&")
            firstNameList.append(primaryFirstValue)
        # different last name
        elif primaryLastValue != spouseLastValue:
            firstNameList.append(spouseFirstValue)
            firstNameList.append(spouseLastValue)
            firstNameList.append("&")
            firstNameList.append(primaryFirstValue)

        firstName = " ".join(firstNameList)
        lastName = primaryLastValue

        return {"first" : firstName, "last" : lastName}
    
    def getCompany(self, rowCells):
        """Additional processing for sub donors to get the company name if there is none"""
        donorIDIndex = self.indexMap[self.headerDict["DONOR_ID"]["name"]]
        donorIDValue = rowCells[donorIDIndex]

        # Check if this is sub-donor based on donor ID
        if (":" not in donorIDValue):
            return

        # Extract raw data from column cell
        subdonorIndex = self.indexMap[self.headerDict["DONOR"]["name"]]
        subdonorValue = rowCells[subdonorIndex]

        # Split based on colon delimiter
        subdonorList = subdonorValue.split(":")

        # Get list for company and list for sub donor full name
        companyRaw = subdonorList[0]
        subdonorFullName = subdonorList[-1]

        # Extract company name from company string list
        companyList = companyRaw.split(" ")[1:]
        companyActual = " ".join(companyList)

        # Extract full name from sub donor name string list and remove the first donorID element
        subdonorProcessedName = subdonorFullName.split(" ")
        subdonorProcessedName.pop(0)

        # Extract first and last names from raw full name string slice
        # subdonorFirstName = subdonorFullName.split(" ")[1:][0]
        # subdonorLastName = subdonorFullName.split(" ")[2:][0]

        subdonorLastName = "".join(subdonorProcessedName[-1])
        subdonorFirstName = " ".join(subdonorProcessedName[0:-1])

        self.properties["COMPANY"] = companyActual

        self.properties["FIRST_NAME"] = subdonorFirstName

        self.properties["LAST_NAME"] = subdonorLastName

        # print(self.properties["FIRST_NAME"])
        # print(self.properties["LAST_NAME"])
        # print(self.properties["COMPANY"])

        return

    def convertRowCellsList(self, rowCells, indexMap):
        """Instantiates the respective Donor properties based on the list of row cell values"""
        # Fills in property values based on raw cell data
        for header in self.headerOrder:
            self.properties[header] = self.getValueFromKey(header, rowCells)

        # Processes spouse and primary names and adjusts first/last names accordingly
        namePair = self.getNames(rowCells)
        if namePair:
            self.properties["FIRST_NAME"] = namePair["first"]
            self.properties["LAST_NAME"] = namePair["last"]

        # Processes data for sub-donors using the raw data from Household column
        self.getCompany(rowCells)

        # test to check donor properties
        # for key, value in list(self.properties.items()):
        #     print(key, value)

        return
    
    
