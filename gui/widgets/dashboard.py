import os
import wx
import wx.dataview as dv
import wx.lib.gizmos as gizmos
from wx.lib import plot
from functions.funcs import load_data
from settings import DATA_PATH


def led_num_ctrl(parent, value, color, size=(200, 50)):
    led = gizmos.LEDNumberCtrl(parent, wx.ID_ANY, (25, 25), size=size, style=gizmos.LED_ALIGN_RIGHT)
    led.SetValue(value)
    led.SetForegroundColour(color)
    return led


class Dashboard():
    """"""

    def __init__(self, panel, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        self.panel = panel

        ##### personal net worth #####
        assets_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Total Assets', name='total assets')
        assets = led_num_ctrl(self.panel, str(12345.67), 'forest green')
        debts_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Total Debts', name='total debts')
        debts = led_num_ctrl(self.panel, str(-1234.56), 'firebrick')
        net_worth_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Total Net Worth', name='net worth')
        net_worth = led_num_ctrl(self.panel, str(float(assets.GetValue()) - float(debts.GetValue())), 'lime green')
        da_ratio = abs(round(float(debts.GetValue()) / float(assets.GetValue()), 4))
        tooltip = wx.ToolTip(f'Debt to Asset Ratio: {da_ratio}%')
        net_worth_label.SetToolTip(tooltip)
        net_worth_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Personal Summary')
        net_worth_sizer.AddMany((net_worth_label, net_worth))
        net_worth_sizer.AddMany((assets_label, assets))
        net_worth_sizer.AddMany((debts_label, debts))

        ##### passive income #####
        dividend_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Annual Dividend Yield', name='dividend')
        dividend = led_num_ctrl(self.panel, str(1357.89), 'forest green')
        dividend_monthly = round(float(dividend.GetValue()) / 12, 4)
        tooltip = wx.ToolTip(f'Average dividend per month: ${dividend_monthly}.\nTotal Dividend Received: ${1123.45}')
        dividend_label.SetToolTip(tooltip)
        passive_income_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Passive Income')
        passive_income_sizer.AddMany((dividend_label, dividend))

        ##### credit scores #####
        equifax_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Equifax', name='equifax')
        equifax = led_num_ctrl(self.panel, str(800), 'sky blue')
        transunion_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Transunion', name='transunion')
        transunion = led_num_ctrl(self.panel, str(805), 'sky blue')
        experian_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Experian', name='experian')
        experian = led_num_ctrl(self.panel, str(799), 'sky blue')
        credit_score_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Credit Scores')
        credit_score_sizer.AddMany((equifax_label, equifax))
        credit_score_sizer.AddMany((transunion_label, transunion))
        credit_score_sizer.AddMany((experian_label, experian))

        summary_sizer = wx.BoxSizer(wx.VERTICAL)
        summary_sizer.Add(net_worth_sizer, 0, wx.BOTTOM, 8)
        summary_sizer.Add(passive_income_sizer, 0, wx.BOTTOM, 8)
        summary_sizer.Add(credit_score_sizer, 0)

        ##### Monthly Metrics #####
        dvlc = dv.DataViewListCtrl(self.panel, size=(1000, 295))
        dvlc.AppendTextColumn('Month', width=75)
        dvlc.AppendTextColumn('Tsp', width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Stonk', width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Roth IRA', width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Webull', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Coinbase', width=75, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Dividend', width=60, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Invested', width=60, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Cash', width=60, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Debts', width=60, mode=dv.DATAVIEW_CELL_EDITABLE)
        dvlc.AppendTextColumn('Net Worth', width=100, mode=dv.DATAVIEW_CELL_EDITABLE)

        data = load_data(os.path.join(DATA_PATH, 'metrics.csv'))
        for item in data:
            dvlc.AppendItem(item)

        dvlc_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Monthly Metrics')
        dvlc_sizer.Add(dvlc, 0, wx.EXPAND)

        x_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        y_data = [2, 4, 6, 4, 2, 5, 6, 7, 1, 7, 4, 5]
        xy_data = list(zip(x_data, y_data))
        line = plot.PolySpline(xy_data, colour=wx.Colour('black'), width=2)
        graphics = plot.PlotGraphics([line])
        canvas = plot.PlotCanvas(self.panel, 0, size=(1000, 215))
        canvas.axesPen = wx.Pen(wx.BLUE, 1, wx.PENSTYLE_LONG_DASH)
        canvas.enableAntiAliasing = True
        canvas.enableAxesLabels = True
        canvas.enableHiRes = True
        canvas.enableAxes = True
        canvas.enableAxesValues = True
        canvas.enableGrid = True
        canvas.enableTicks = True
        canvas.enableTitle = True
        canvas.SetBackgroundColour('dark grey')
        canvas.Draw(graphics)
        canvas_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Metrics Graph')
        canvas_sizer.Add(canvas, 0, wx.EXPAND)

        metrics_sizer = wx.BoxSizer(wx.VERTICAL)
        metrics_sizer.AddMany((dvlc_sizer, canvas_sizer))

        dashboard_sizer = wx.BoxSizer(wx.HORIZONTAL)
        dashboard_sizer.Add(summary_sizer, 0, wx.EXPAND)
        dashboard_sizer.Add(metrics_sizer, 0, wx.EXPAND)
        dashboard_sizer.Fit(self.panel)
        self.panel.SetSizer(dashboard_sizer)
