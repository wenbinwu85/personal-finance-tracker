import os
import wx
import wx.dataview as dv
from settings import DATA_PATH
from functions.funcs import load_data

class AssetsDebts():
    """"""

    def __init__(self, panel, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        self.panel = panel

        dvlc = dv.DataViewListCtrl(self.panel, size=(520, 580))
        dvlc.AppendTextColumn('Item', width=120)
        dvlc.AppendTextColumn('Value', width=100, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Type', width=100, mode=dv.DATAVIEW_CELL_EDITABLE | dv.DATAVIEW_COL_SORTABLE)
        dvlc.AppendTextColumn('Note', width=200, mode=dv.DATAVIEW_CELL_EDITABLE)

        data = load_data(os.path.join(DATA_PATH, 'assets_debts.csv'))
        for item in data:
            dvlc.AppendItem(item)

        asset_debt_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Assets & Debts')
        asset_debt_sizer.Add(dvlc, 0, wx.EXPAND)

        dvlc2 = dv.DataViewListCtrl(self.panel, size=(650, 580))
        dvlc2.AppendTextColumn('Item', width=120)
        dvlc2.AppendTextColumn('Amount', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc2.AppendTextColumn('Time', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc2.AppendTextColumn('Date', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc2.AppendTextColumn('Type', width=60, mode=dv.DATAVIEW_CELL_EDITABLE | dv.DATAVIEW_COL_SORTABLE)
        dvlc2.AppendTextColumn('Payment Plan', width=225, mode=dv.DATAVIEW_CELL_EDITABLE)

        data = load_data(os.path.join(DATA_PATH, 'budget.csv'))
        for item in data:
            dvlc2.AppendItem(item)

        budget_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Budget Plan')
        budget_sizer.Add(dvlc2, 0, wx.EXPAND)

        dvlc3 = dv.DataViewListCtrl(self.panel, size=(350, 580))
        dvlc3.AppendTextColumn('Account', width=150, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc3.AppendTextColumn('Type', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc3.AppendTextColumn('Status', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)

        data = load_data(os.path.join(DATA_PATH, 'accounts.csv'))
        for item in data:
            dvlc3.AppendItem(item)

        accounts_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Financial Accounts')
        accounts_sizer.Add(dvlc3, 0, wx.EXPAND)

        widget_sizer = wx.BoxSizer(wx.HORIZONTAL)
        widget_sizer.AddMany((asset_debt_sizer, budget_sizer, accounts_sizer))
        self.panel.SetSizer(widget_sizer)
