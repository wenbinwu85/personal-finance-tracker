import wx
import wx.dataview as dv
import wx.lib.gizmos as gizmos
from wx.lib import plot
from functions.funcs import load_data_from
from settings import METRICS_DATA_PATH


def led_num_ctrl(parent, value, color, size=(200, 50)):
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
    return led


class Dashboard(wx.Panel):
    """"""

    def __init__(self, name, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.name = name

        ##### personal net worth #####
        assets_label = wx.StaticText(self, label='Assets')
        assets_led = led_num_ctrl(self, str(12345.67), 'forest green')
        debts_label = wx.StaticText(self, label='Debts')
        debts_led = led_num_ctrl(self, str(-1234.56), 'firebrick')
        net_worth = str(float(assets_led.GetValue()) - float(debts_led.GetValue()))
        net_worth_label = wx.StaticText(self, label='Net Worth')
        net_worth_led = led_num_ctrl(self, net_worth, 'lime green')
        da_ratio = abs(round(float(debts_led.GetValue()) / float(assets_led.GetValue()), 4))
        tooltip = wx.ToolTip(f'Debt to Asset Ratio: {da_ratio}%')
        net_worth_label.SetToolTip(tooltip)
        net_worth_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Personal Summary')
        net_worth_sizer.AddMany((net_worth_label, net_worth_led))
        net_worth_sizer.AddMany((assets_label, assets_led))
        net_worth_sizer.AddMany((debts_label, debts_led))

        ##### passive income #####
        yield_label = wx.StaticText(self, label='Annual Dividend Yield %')
        yield_led = led_num_ctrl(self, '8.56', 'forest green')
        dividend_label = wx.StaticText(self, label='Annual Dividend Yield')
        dividend_led = led_num_ctrl(self, str(1357.89), 'forest green')
        monthly_div = round(float(dividend_led.GetValue()) / 12, 2)
        monthly_div_label = wx.StaticText(self, label='Monthly Dividend Yield')
        monthly_div_led = led_num_ctrl(self, str(monthly_div), 'forest green')
        total_div = 6543.21
        total_div_label = wx.StaticText(self, label='Total Dividend Received')
        total_div_led = led_num_ctrl(self, str(total_div), 'forest green')
        dividend_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Passive Income')
        dividend_sizer.AddMany((yield_label, yield_led))
        dividend_sizer.AddMany((dividend_label, dividend_led))
        dividend_sizer.AddMany((monthly_div_label, monthly_div_led))
        dividend_sizer.AddMany((total_div_label, total_div_led))

        ##### credit scores #####
        equifax_label = wx.StaticText(self, label='Equifax')
        equifax = led_num_ctrl(self, str(800), 'sky blue')
        transunion_label = wx.StaticText(self, label='Transunion')
        transunion = led_num_ctrl(self, str(805), 'sky blue')
        experian_label = wx.StaticText(self, label='Experian')
        experian = led_num_ctrl(self, str(799), 'sky blue')
        credit_score_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Credit Scores')
        credit_score_sizer.AddMany((equifax_label, equifax))
        credit_score_sizer.AddMany((transunion_label, transunion))
        credit_score_sizer.AddMany((experian_label, experian))

        summary_sizer = wx.BoxSizer(wx.VERTICAL)
        summary_sizer.Add(net_worth_sizer, 0, wx.BOTTOM, 10)
        summary_sizer.Add(dividend_sizer, 0, wx.BOTTOM, 10)
        summary_sizer.Add(credit_score_sizer, 0, wx.BOTTOM, 10)
        summary_sizer.SetMinSize((-1, 820))

        ##### Monthly Metrics #####
        dvlc = dv.DataViewListCtrl(self, size=(1000, 295))
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

        for item in load_data_from(METRICS_DATA_PATH):
            dvlc.AppendItem(item)

        dvlc_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Monthly Metrics')
        dvlc_sizer.Add(dvlc, 0, wx.EXPAND)

        ##### metrics graph #####
        x_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        y_data = [2, 4, 6, 4, 2, 5, 6, 7, 1, 7, 4, 5]
        xy_data = list(zip(x_data, y_data))
        line = plot.PolySpline(xy_data, colour=wx.Colour('black'), width=2)
        graphics = plot.PlotGraphics([line])
        canvas = plot.PlotCanvas(self, 0, size=(1000, 210))
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
        canvas_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Metrics Graph')
        canvas_sizer.Add(canvas, 0, wx.EXPAND)

        metrics_sizer = wx.BoxSizer(wx.VERTICAL)
        metrics_sizer.Add(dvlc_sizer, 0, wx.BOTTOM, 10)
        metrics_sizer.Add(canvas_sizer, 0, wx.BOTTOM, 10)

        dashboard_sizer = wx.BoxSizer(wx.HORIZONTAL)
        dashboard_sizer.Add(summary_sizer, 0, wx.EXPAND)
        dashboard_sizer.Add(metrics_sizer, 0, wx.EXPAND)

        self.SetSizerAndFit(dashboard_sizer)
