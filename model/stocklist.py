import wx.dataview as dv


class DVIListModel(dv.DataViewIndexListModel):
    def __init__(self, data):
        dv.DataViewIndexListModel.__init__(self, len(data))
        self.data = data

    def add_row(self, value):
        self.data.append(value)
        self.RowAppended()

    def delete_rows(self, rows):
        rows = sorted(rows, reverse=True)

        for row in rows:
            del self.data[row]
            self.RowDeleted(row)

    def GetColumnType(self, col):
        return 'string'

    def GetValueByRow(self, row, col):
        return self.data[row][col]

    def SetValueByRow(self, value, row, col):
        self.data[row][col] = value
        return True

    def GetColumnCount(self):
        try:
            return len(self.data[0])
        except IndexError:
            return 1

    def GetCount(self):
        return len(self.data)

    def Compare(self, item1, item2, col, ascending):
        if not ascending:  # swap sort order?
            item2, item1 = item1, item2
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        a = self.data[row1][col]
        b = self.data[row2][col]
        if col == 0:
            a = int(a)
            b = int(b)
        if a < b: return -1
        if a > b: return 1
        return 0
