class Group:
    def __init__(self, rowCells, indexMap, headerDict, headerOrder):
        self.rowCount = 0
        self.properties = dict()
        self.indexMap = indexMap
        self.headerDict = headerDict
        self.headerOrder = headerOrder
        self.convertRowCellsList(rowCells, indexMap)
