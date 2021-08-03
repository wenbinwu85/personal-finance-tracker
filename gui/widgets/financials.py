import wx
import wx.dataview as dv
from settings import ASSETS_DEBTS_DATA_PATH, BUDGET_PLAN_DATA_PATH, ACCOUNTS_DATA_PATH
from functions.funcs import load_data_from


class Financials(wx.Panel):
    """"""

    def __init__(self, name, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.name = name

        ##### assets and debts #####
        dvlc = dv.DataViewListCtrl(self, size=(500, 600))
        dvlc.AppendTextColumn('Item', width=wx.COL_WIDTH_AUTOSIZE)
        dvlc.AppendTextColumn('Value', width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Type', width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Note', width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE)

        for item in load_data_from(ASSETS_DEBTS_DATA_PATH):
            dvlc.AppendItem(item)

        asset_debt_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Assets and Debts')
        asset_debt_sizer.Add(dvlc, 0, wx.EXPAND)

        ##### budget plan #####
        dvlc2 = dv.DataViewListCtrl(self, size=(600, 600))
        dvlc2.AppendTextColumn('Item', width=wx.COL_WIDTH_AUTOSIZE)
        dvlc2.AppendTextColumn('Amount', width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc2.AppendTextColumn('Time', width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc2.AppendTextColumn('Date', width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc2.AppendTextColumn('Type', width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc2.AppendTextColumn('Payment Plan', width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE)

        for item in load_data_from(BUDGET_PLAN_DATA_PATH):
            dvlc2.AppendItem(item)

        budget_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Budget Plan')
        budget_sizer.Add(dvlc2, 0, wx.EXPAND)

        ##### financial account #####
        dvlc3 = dv.DataViewListCtrl(self, size=(340, 600))
        dvlc3.AppendTextColumn('Account', width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc3.AppendTextColumn('Type', width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc3.AppendTextColumn('Status', width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE)

        for item in load_data_from(ACCOUNTS_DATA_PATH):
            dvlc3.AppendItem(item)

        accounts_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Financial Accounts')
        accounts_sizer.Add(dvlc3, 0, wx.EXPAND)

        financials_sizer = wx.BoxSizer(wx.HORIZONTAL)
        financials_sizer.AddMany((asset_debt_sizer, budget_sizer, accounts_sizer))

        self.SetSizerAndFit(financials_sizer)
