import wx
import wx.dataview as dv
from settings import STOCKLIST_DATA_PATH, stocks_list_columns
from functions.funcs import load_data_from, dump_data
from model.stocklist import DVIListModel


class StockList(wx.Panel):
    """"""

    def __init__(self, name, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.name = name

        self.stock_list_model, self.stock_list = self.generate_stock_list()
        self.stock_list.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.stock_list_context_menu)

        stocklist_sizer = wx.BoxSizer(wx.VERTICAL)
        stocklist_sizer.Add(self.stock_list, 1, wx.EXPAND)
        self.SetSizerAndFit(stocklist_sizer)

    def generate_stock_list(self):
        stock_list = dv.DataViewCtrl(
            self,
            size=(1300, 640),
            style=wx.BORDER_THEME | dv.DV_ROW_LINES | dv.DV_VERT_RULES | dv.DV_MULTIPLE
        )
        self.stock_data = load_data_from(STOCKLIST_DATA_PATH)
        stock_list_model = DVIListModel(self.stock_data)
        stock_list.AssociateModel(stock_list_model)

        for idx, val in enumerate(stocks_list_columns):
            stock_list.AppendTextColumn(
                val, idx, width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE
            )

        for col in stock_list.Columns:
            col.Sortable = True
            col.Reorderable = True

        return stock_list_model, stock_list

    def stock_list_context_menu(self, event):
        context_menu = wx.Menu()
        item1 = wx.MenuItem(context_menu, wx.NewIdRef(), 'Add Row')
        item2 = wx.MenuItem(context_menu, wx.NewIdRef(), 'Delete Rows')
        item9 = wx.MenuItem(context_menu, wx.NewIdRef(), 'Save Stocks Data')
        context_menu.Append(item1)
        context_menu.Append(item2)
        context_menu.Append(item9)

        self.Bind(wx.EVT_MENU, self.add_row, id=item1.GetId())
        self.Bind(wx.EVT_MENU, self.delete_rows, id=item2.GetId())
        self.Bind(wx.EVT_MENU, self.save_stocks_data, id=item9.GetId())

        self.PopupMenu(context_menu)
        context_menu.Destroy()

    def add_row(self, event):
        col_count = self.stock_list.GetColumnCount()
        values = ['0' for _ in range(col_count)]
        self.stock_list_model.add_row(values)

    def delete_rows(self, event):
        selected = self.stock_list.GetSelections()
        rows = [self.stock_list_model.GetRow(item) for item in selected]
        self.stock_list_model.delete_rows(rows)

    def save_stocks_data(self, event):
        dump_data(self.stock_data, STOCKLIST_DATA_PATH)
        self.parent.GetTopLevelParent().dashboard.update_passive_income()
