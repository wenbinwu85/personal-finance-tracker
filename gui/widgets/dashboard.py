from math import pi
import wx
import wx.dataview as dv
import wx.lib.gizmos as gizmos
from wx.lib.agw.piectrl import PieCtrl, PiePart
from wx.lib.agw.pycollapsiblepane import PyCollapsiblePane
from functions.funcs import load_data_from
from settings import METRICS_DATA_PATH, PERSONAL_SUMMARY_DATA_PATH
from settings import PASSIVE_INCOME_DATA_PATH, CREDIT_SCORES_DATA_PATH


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
        avg_label, avg_led = led_num_ctrl(self, 'Average(2020)', '711', 'sky blue', (100, 50))
        credit_score_sizer.AddMany((avg_label, avg_led))

        self.pie = PieCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(230, 225))
        self.pie.SetHeight(30)
        self.pie.SetBackColour('dark grey')
        self.pie.SetShowEdges(False)
        pie_legend = self.pie.GetLegend()
        pie_legend.SetTransparent(True)
        pie_legend.SetLabelColour(wx.Colour(225, 225, 225))
        pie_part1 = PiePart(100, wx.Colour(200, 50, 50), 'Cash')
        pie_part2 = PiePart(250, wx.Colour(50, 200, 50), 'Savings')
        pie_part3 = PiePart(450, wx.Colour(50, 50, 200), 'Investments')
        pie_part4 = PiePart(150, wx.Colour(200, 200, 50), 'Real Estate')

        self.pie._series.append(pie_part1)
        self.pie._series.append(pie_part2)
        self.pie._series.append(pie_part3)
        self.pie._series.append(pie_part4)

        self.hslider = wx.Slider(
            self, wx.ID_ANY, 180, 0, 360, size=(225, -1), style=wx.SL_LABELS | wx.SL_TOP
        )
        self.hslider.Bind(wx.EVT_SLIDER, self.hslider_handler)
        self.vslider = wx.Slider(
            self, wx.ID_ANY, 40, 20, 60, size=wx.DefaultSize, style=wx.SL_VERTICAL | wx.SL_LABELS
        )
        self.vslider.Bind(wx.EVT_SLIDER, self.vslider_handler)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.pie, 0, wx.EXPAND)
        hsizer.Add(self.vslider, 1, wx.EXPAND | wx.GROW)

        pie_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Wealth Distribution')
        pie_sizer.Add(hsizer)
        pie_sizer.Add(self.hslider, 1)

        summary_sizer = wx.BoxSizer(wx.HORIZONTAL)
        summary_sizer.Add(net_worth_sizer, 0, wx.BOTTOM, 10)
        summary_sizer.Add(dividend_sizer, 0, wx.BOTTOM, 10)
        summary_sizer.Add(credit_score_sizer, 0, wx.BOTTOM, 10)
        summary_sizer.Add(pie_sizer, 0, wx.BOTTOM | wx.EXPAND, 10)

        ##### Monthly Metrics #####
        self.cpane = PyCollapsiblePane(self, label='Monthly Metrics', style=wx.CP_DEFAULT_STYLE)
        self.cpane.SetAutoLayout(True)
        # self.cpane.Expand()
        self.cpane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapse_pane_change)
        metrics_columns = [
            'Month', 'TSP', 'Schwab', 'Roth IRA', 'Webull',
            'Coinbase', 'Dividend', 'Invested', 'Cash', 'Debts', 'Net Worth'
        ]
        dvlc = dv.DataViewListCtrl(self.cpane.GetPane(), size=(860, 325))
        for i in metrics_columns:
            dvlc.AppendTextColumn(i, width=wx.COL_WIDTH_AUTOSIZE)
        for item in load_data_from(METRICS_DATA_PATH):
            dvlc.AppendItem(item)

        self.dashboard_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dashboard_sizer.Add(summary_sizer, 0, wx.EXPAND)
        self.dashboard_sizer.Add(self.cpane, 0, wx.EXPAND)

        self.SetSizerAndFit(self.dashboard_sizer)
        self.dashboard_sizer.Layout()
        self.SetMinSize((self.GetMinWidth(), self.GetMinHeight()+30))

        self.hslider_handler(wx.EVT_SLIDER)
        self.vslider_handler(wx.EVT_SLIDER)

    def vslider_handler(self, event):
        self.pie.SetAngle(float(self.vslider.GetValue()) / 180.0 * pi)

    def hslider_handler(self, event):
        self.pie.SetRotationAngle(float(self.hslider.GetValue()) / 180.0 * pi)

    def collapse_pane_change(self, event):
        if self.cpane.IsExpanded():
            self.SetSizerAndFit(self.dashboard_sizer)
            self.dashboard_sizer.Layout()
            frame = self.GetTopLevelParent()
            frame.SetClientSize(self.GetSize())
            frame.SendSizeEvent()
            frame.CenterOnScreen()
        else:
            self.SetSizerAndFit(self.dashboard_sizer)
            self.dashboard_sizer.Layout()
            self.SetMinSize((self.GetMinWidth(), self.GetMinHeight()+30))
            frame = self.GetTopLevelParent()
            frame.SetClientSize(self.GetMinSize())
            frame.SendSizeEvent()
            frame.CenterOnScreen()
