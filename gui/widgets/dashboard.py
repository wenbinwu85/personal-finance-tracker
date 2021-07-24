import wx
import wx.lib.gizmos as gizmos


class Dashboard():
    """"""

    def __init__(self, panel, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        self.panel = panel

        assets_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Total Assets:', name='total assets')
        assets = gizmos.LEDNumberCtrl(self.panel, -1, (25, 25), (200, 50), style=gizmos.LED_ALIGN_RIGHT)
        assets.SetValue(str(12345.67))
        assets.SetForegroundColour('forest green')

        debts_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Total Debts:', name='total debts')
        debts = gizmos.LEDNumberCtrl(self.panel, wx.ID_ANY, (25, 25), (200, 50), style=gizmos.LED_ALIGN_RIGHT)
        debts.SetValue(str(-123.45))
        debts.SetForegroundColour('firebrick')

        net_worth_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Total Net Worth:', name='net worth')
        net_worth = gizmos.LEDNumberCtrl(self.panel, wx.ID_ANY, (25, 25), (200, 50), style=gizmos.LED_ALIGN_RIGHT)
        net_worth.SetValue(str(float(assets.GetValue()) - float(debts.GetValue())))
        net_worth.SetForegroundColour('lime green')

        da_ratio = abs(round(float(debts.GetValue()) / float(assets.GetValue()), 6))
        da_ratio_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Debt to Asset Ratio: {da_ratio}%', name='da ratio')
        da_ratio_label.SetForegroundColour('coral')

        dividend_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Annual Dividend Yield:', name='dividend')
        dividend = gizmos.LEDNumberCtrl(self.panel, wx.ID_ANY, (25, 25), (200, 50), style=gizmos.LED_ALIGN_RIGHT)
        dividend.SetValue(str(1234))
        dividend.SetForegroundColour('forest green')
        dividend_monthly = round(float(dividend.GetValue()) / 12, 4)
        dividend_label.SetToolTip(f'Total dividend received annually, average ${dividend_monthly} per month.')
        dividend_monthly_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'monthly average: ${dividend_monthly}')
        dividend_monthly_label.SetForegroundColour('coral')

        equifax_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Equifax:', name='equifax')
        equifax = gizmos.LEDNumberCtrl(self.panel, -1, (25, 25), (200, 50), style=gizmos.LED_ALIGN_RIGHT)
        equifax.SetValue(str(800))
        equifax.SetForegroundColour('sky blue')

        transunion_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Transunion:', name='transunion')
        transunion = gizmos.LEDNumberCtrl(self.panel, wx.ID_ANY, (25, 25), (200, 50), style=gizmos.LED_ALIGN_RIGHT)
        transunion.SetValue(str(805))
        transunion.SetForegroundColour('sky blue')

        experian_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Experian:', name='experian')
        experian = gizmos.LEDNumberCtrl(self.panel, wx.ID_ANY, (25, 25), (200, 50), style=gizmos.LED_ALIGN_RIGHT)
        experian.SetValue(str(799))
        experian.SetForegroundColour('sky blue')

        net_worth_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Personal Net Worth')
        net_worth_sizer.Add(net_worth_label, 0)
        net_worth_sizer.Add(net_worth)
        net_worth_sizer.Add(assets_label, 0)
        net_worth_sizer.Add(assets)
        net_worth_sizer.Add(debts_label, 0)
        net_worth_sizer.Add(debts)
        net_worth_sizer.Add(da_ratio_label, 0)

        passive_income_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Passive Income')
        passive_income_sizer.Add(dividend_label, 0)
        passive_income_sizer.Add(dividend)
        passive_income_sizer.Add(dividend_monthly_label, 0)

        credit_score_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Credit Scores')
        credit_score_sizer.Add(equifax_label, 0)
        credit_score_sizer.Add(equifax)
        credit_score_sizer.Add(transunion_label, 0)
        credit_score_sizer.Add(transunion)
        credit_score_sizer.Add(experian_label, 0)
        credit_score_sizer.Add(experian)

        dashboard_sizer = wx.BoxSizer(wx.VERTICAL)
        dashboard_sizer.Add(net_worth_sizer, 0, wx.BOTTOM, 10)
        dashboard_sizer.Add(passive_income_sizer, 0, wx.BOTTOM, 10)
        dashboard_sizer.Add(credit_score_sizer, 0, wx.BOTTOM, 10)
        dashboard_sizer.Fit(self.panel)
        self.panel.SetSizer(dashboard_sizer)
