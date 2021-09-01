import wx
import wx.dataview as dv
from settings import STOCKLIST_DATA_PATH, stocks_footer_columns
from functions.funcs import load_data_from, dump_data
from model.stocklist import DVIListModel


class StockList(wx.Panel):
    """"""

    def __init__(self, name, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.name = name

        self.stocks_dvc = dv.DataViewCtrl(
            self,
            size=(1600, 680),
            style=wx.BORDER_THEME | dv.DV_ROW_LINES | dv.DV_VERT_RULES | dv.DV_MULTIPLE
        )
        self.stocks_dvc.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.stocks_dvc_context_menu)
        self.stocks_dvc.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.stock_selected)

        stocks = load_data_from(STOCKLIST_DATA_PATH)
        self.stocks_data_header = stocks[0]
        self.stocks_data = stocks[1:]
        self.stocks_dvc_model = DVIListModel(self.stocks_data)
        self.stocks_dvc.AssociateModel(self.stocks_dvc_model)

        for idx, val in enumerate(self.stocks_data_header):
            self.stocks_dvc.AppendTextColumn(
                val, idx, width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE
            )
        for col in self.stocks_dvc.Columns:
            col.Sortable = True
            col.Reorderable = True

        self.stocks_footer_dvlc = dv.DataViewListCtrl(self, size=(1600, 10), style=dv.DV_VERT_RULES)
        for val in stocks_footer_columns:
            self.stocks_footer_dvlc.AppendTextColumn(val, width=wx.COL_WIDTH_AUTOSIZE)
        self.stocks_footer_dvlc.AppendItem(['0' for _ in range(len(stocks_footer_columns))])

        stocklist_sizer = wx.BoxSizer(wx.VERTICAL)
        stocklist_sizer.Add(self.stocks_dvc, 0, wx.EXPAND)
        stocklist_sizer.Add(self.stocks_footer_dvlc, 1, wx.EXPAND)
        self.SetSizerAndFit(stocklist_sizer)
        self.SetMinSize((1600, 765))

    def stocks_dvc_context_menu(self, event):
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
        col_count = self.stocks_dvc.GetColumnCount()
        values = ['0' for _ in range(col_count)]
        self.stocks_dvc_model.add_row(values)

    def delete_rows(self, event):
        selected = self.stocks_dvc.GetSelections()
        rows = [self.stocks_dvc_model.GetRow(item) for item in selected]
        self.stocks_dvc_model.delete_rows(rows)

    def save_stocks_data(self, event):
        data = [self.stocks_data_header] + self.stocks_data
        dump_data(data, STOCKLIST_DATA_PATH)
        self.parent.GetTopLevelParent().dashboard.update_passive_income()

    def stock_selected(self, event):
        pass
