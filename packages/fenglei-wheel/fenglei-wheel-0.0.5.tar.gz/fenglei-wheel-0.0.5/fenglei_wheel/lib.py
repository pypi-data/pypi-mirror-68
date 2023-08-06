import xlrd

class ExcelUtil:
    def __init__(self, filename):
        self.workbook = xlrd.open_workbook(filename)

    def sheet(self, index, skip = 0):
        self._sheet = self.workbook.sheet_by_index(index)
        content = []
        for row_index in range(skip, self._sheet.nrows):
            for cell in self._sheet.row(row_index):
                content.append(cell.value)
        return content