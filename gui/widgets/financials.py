import wx
import wx.dataview as dv
from settings import ASSETS_DEBTS_DATA_PATH, BUDGET_PLAN_DATA_PATH, ACCOUNTS_DATA_PATH
from functions.funcs import load_data_from


class Financials():
    """"""

    def __init__(self, panel, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        self.panel = panel

        ##### assets and debts #####
        dvlc = dv.DataViewListCtrl(self.panel, size=(520, 800))
        dvlc.AppendTextColumn('Item', width=120)
        dvlc.AppendTextColumn('Value', width=100, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Type', width=100, mode=dv.DATAVIEW_CELL_EDITABLE | dv.DATAVIEW_COL_SORTABLE)
        dvlc.AppendTextColumn('Note', width=200, mode=dv.DATAVIEW_CELL_EDITABLE)

        for item in load_data_from(ASSETS_DEBTS_DATA_PATH):
            dvlc.AppendItem(item)

        asset_debt_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Assets and Debts')
        asset_debt_sizer.Add(dvlc, 0, wx.EXPAND)

        ##### budget plan #####
        dvlc2 = dv.DataViewListCtrl(self.panel, size=(630, 800))
        dvlc2.AppendTextColumn('Item', width=120)
        dvlc2.AppendTextColumn('Amount', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc2.AppendTextColumn('Time', width=70, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc2.AppendTextColumn('Date', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc2.AppendTextColumn('Type', width=60, mode=dv.DATAVIEW_CELL_EDITABLE | dv.DATAVIEW_COL_SORTABLE)
        dvlc2.AppendTextColumn('Payment Plan', width=225, mode=dv.DATAVIEW_CELL_EDITABLE)

        for item in load_data_from(BUDGET_PLAN_DATA_PATH):
            dvlc2.AppendItem(item)

        budget_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Budget Plan')
        budget_sizer.Add(dvlc2, 0, wx.EXPAND)

        ##### financial account #####
        dvlc3 = dv.DataViewListCtrl(self.panel, size=(340, 800))
        dvlc3.AppendTextColumn('Account', width=150, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc3.AppendTextColumn('Type', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc3.AppendTextColumn('Status', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)

        for item in load_data_from(ACCOUNTS_DATA_PATH):
            dvlc3.AppendItem(item)

        accounts_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Financial Accounts')
        accounts_sizer.Add(dvlc3, 0, wx.EXPAND)

        widget_sizer = wx.BoxSizer(wx.HORIZONTAL)
        widget_sizer.AddMany((asset_debt_sizer, budget_sizer, accounts_sizer))

        self.panel.SetSizerAndFit(widget_sizer)
