import wx
import wx.dataview as dv
from settings import STOCKLIST_DATA_PATH, stocks_columns, stocks_footer_columns
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

        self.stocks_dvc_model = DVIListModel(load_data_from(STOCKLIST_DATA_PATH))
        self.stocks_dvc.AssociateModel(self.stocks_dvc_model)

        for i in range(3):
            self.stocks_dvc.AppendTextColumn(
                stocks_columns[i], i, width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE
            )
        for idx, val in enumerate(stocks_columns[3:-2]):
            self.stocks_dvc.AppendTextColumn(val, idx+3, width=wx.COL_WIDTH_AUTOSIZE)
        col_count = self.stocks_dvc.GetColumnCount()
        self.stocks_dvc.AppendTextColumn(
            stocks_columns[-2], col_count, width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE
        )
        self.stocks_dvc.AppendTextColumn(
            stocks_columns[-1], col_count+1, width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE
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
        dump_data(self.stocks_dvc_model.data, STOCKLIST_DATA_PATH)
        self.parent.GetTopLevelParent().dashboard.update_passive_income()

    def stock_selected(self, event):
        selected = self.stocks_dvc.GetSelections()
        count = len(selected)
        cost_basis = 0
        market_value = 0
        gain_lost = 0
        annual_dividend = 0
        dividend_received = 0

        for i in selected:
            row = self.stocks_dvc_model.GetRow(i)
            row_data = self.stocks_dvc_model.GetRowData(row)
            cost_basis += float(row_data[4])
            market_value += float(row_data[5])
            gain_lost += float(row_data[6])
            annual_dividend += float(row_data[9])
            dividend_received += float(row_data[10])

        row_count = self.stocks_dvc_model.GetRowCount()
        account_total = sum([float(self.stocks_dvc_model.GetValueByRow(i, 5)) for i in range(row_count)])

        try:
            gain_lost_percentage = gain_lost / cost_basis * 100
            yield_percentage = annual_dividend / market_value * 100
            account_percentage = market_value / account_total * 100
        except ZeroDivisionError:
            gain_lost_percentage = 0
            yield_percentage = 0
            account_percentage = 0

        footer_data = [
            count, cost_basis, market_value,
            gain_lost, gain_lost_percentage,
            yield_percentage, annual_dividend, dividend_received,
            account_percentage
        ]
        footer_data = [str(round(i, 2)) for i in footer_data]

        self.stocks_footer_dvlc.DeleteItem(0)
        self.stocks_footer_dvlc.AppendItem(footer_data)
