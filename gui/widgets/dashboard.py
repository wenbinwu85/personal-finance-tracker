import wx
import wx.lib.gizmos as gizmos


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
        da_ratio_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Debt to Asset Ratio: {da_ratio}%', name='da ratio')
        da_ratio_label.SetForegroundColour('coral')
        net_worth_label.SetToolTip(f'Debt to Asset Ratio: {da_ratio}%')

        net_worth_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Personal Net Worth')
        net_worth_sizer.AddMany((net_worth_label, net_worth))
        net_worth_sizer.AddMany((assets_label, assets))
        net_worth_sizer.AddMany((debts_label, debts))
        net_worth_sizer.Add(da_ratio_label, 0)

        ##### passive income #####
        dividend_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Annual Dividend Yield', name='dividend')
        dividend = led_num_ctrl(self.panel, str(1357.9), 'forest green')
        dividend_monthly = round(float(dividend.GetValue()) / 12, 4)
        dividend_label.SetToolTip(f'Total dividend received annually, average ${dividend_monthly} per month.')
        dividend_monthly_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Monthly Average: ${dividend_monthly}')
        dividend_monthly_label.SetForegroundColour('coral')
        dividend_total_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Total Received: ${1123.45}')
        dividend_total_label.SetForegroundColour('coral')

        passive_income_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Passive Income')
        passive_income_sizer.AddMany((dividend_label, dividend, dividend_monthly_label, dividend_total_label))

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

        dashboard_sizer = wx.BoxSizer(wx.VERTICAL)
        dashboard_sizer.Add(net_worth_sizer, 0, wx.BOTTOM, 10)
        dashboard_sizer.Add(passive_income_sizer, 0, wx.BOTTOM, 10)
        dashboard_sizer.Add(credit_score_sizer, 0, wx.BOTTOM, 10)
        dashboard_sizer.Fit(self.panel)
        self.panel.SetSizer(dashboard_sizer)
