import wx
import wx.dataview as dv
import wx.lib.gizmos as gizmos
from functions.funcs import load_data_from
from settings import METRICS_DATA_PATH, PERSONAL_SUMMARY_DATA_PATH, PASSIVE_INCOME_DATA_PATH, CREDIT_SCORES_DATA_PATH


def led_num_ctrl(parent, label, value, color, size=(200, 50)):
    label = wx.StaticText(parent, label=label)
    led = gizmos.LEDNumberCtrl(
        parent,
        wx.ID_ANY,
        (25, 25),
        size=size,
        style=gizmos.LED_ALIGN_RIGHT
    )
    led.SetValue(value)
    led.SetForegroundColour(color)
    led.SetDrawFaded(True)
    return label, led


class Dashboard(wx.Panel):
    """"""

    def __init__(self, name, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.name = name

        ##### personal net worth #####
        net_worth_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Personal Summary')
        for (text, value, color) in load_data_from(PERSONAL_SUMMARY_DATA_PATH):
            label, led = led_num_ctrl(self, text, value, color)
            net_worth_sizer.AddMany((label, led))

        ##### passive income #####
        dividend_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Passive Income')
        for (text, value) in load_data_from(PASSIVE_INCOME_DATA_PATH):
            label, led = led_num_ctrl(self, text, value, 'forest green')
            dividend_sizer.AddMany((label, led))

        ##### credit scores #####
        credit_score_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Credit Scores')
        for (text, value) in load_data_from(CREDIT_SCORES_DATA_PATH):
            label, led = led_num_ctrl(self, text, value, 'sky blue', (100, 50))
            credit_score_sizer.AddMany((label, led))

        summary_sizer = wx.BoxSizer(wx.HORIZONTAL)
        summary_sizer.Add(net_worth_sizer, 0, wx.BOTTOM, 10)
        summary_sizer.Add(dividend_sizer, 0, wx.BOTTOM, 10)
        summary_sizer.Add(credit_score_sizer, 0, wx.BOTTOM, 10)

        ##### Monthly Metrics #####
        dvlc = dv.DataViewListCtrl(self, size=(945, 325))
        dvlc.AppendTextColumn('Month', width=75)
        dvlc.AppendTextColumn('Tsp', width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Stonk', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Roth IRA', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Webull', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Coinbase', width=70, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Dividend', width=60, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Invested', width=60, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Cash', width=50, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Debts', width=50, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Net Worth', width=80, mode=dv.DATAVIEW_CELL_EDITABLE)

        for item in load_data_from(METRICS_DATA_PATH):
            dvlc.AppendItem(item)

        dvlc_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Monthly Metrics')
        dvlc_sizer.Add(dvlc, 0, wx.EXPAND)

        ##### metrics graph #####
        dashboard_sizer = wx.BoxSizer(wx.VERTICAL)
        dashboard_sizer.Add(summary_sizer, 0, wx.EXPAND)
        dashboard_sizer.Add(dvlc_sizer, 0, wx.EXPAND)

        self.SetSizerAndFit(dashboard_sizer)
