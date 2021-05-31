import wx


class Dashboard():
    """"""

    def __init__(self, panel, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        self.panel = panel

        assets = 12345.67
        debts = 345.67
        net_worth = assets - debts
        da_ratio = round(debts / assets, 2)
        dividend = 1802
        equifax = 800
        tranunion = 805
        experian = 799

        net_worth_label = wx.StaticText(
            self.panel, wx.ID_ANY, label=f'Net Worth:\t\t\t${net_worth}', name='net worth'
        )
        net_worth_label.SetForegroundColour(wx.Colour(0, 255, 0))
        net_worth_label.SetToolTip('This is your net worth, derived from adding all assets minus all debts.')
        # net_worth_label.SetFont(wx.Font(wx.FontInfo(18)))
        assets_label = wx.StaticText(
            self.panel, wx.ID_ANY, label=f'Total Assets:\t\t\t${assets}', name='total assets'
        )
        debts_label = wx.StaticText(
            self.panel, wx.ID_ANY, label=f'Total Debts:\t\t\t${debts}', name='total debts'
        )
        da_ratio_label = wx.StaticText(
            self.panel, wx.ID_ANY, label=f'Debt to Asset Ratio:\t{da_ratio}%', name='da ratio'
        )
        da_ratio_label.SetForegroundColour(wx.Colour(255, 0, 0))
        net_worth_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Net Worth')
        net_worth_sizer.Add(net_worth_label, 0)
        net_worth_sizer.Add(assets_label, 0)
        net_worth_sizer.Add(debts_label, 0)
        net_worth_sizer.Add(da_ratio_label, 0)

        dividend_label = wx.StaticText(
            self.panel, wx.ID_ANY, label=f'Dividend Yield:\t\t\t${dividend}', name='dividend'
        )
        dividend_label.SetToolTip(f'Total dividend received annually, average ${round(dividend/12, 2)} per month.')
        passive_income_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Passive Income')
        passive_income_sizer.Add(dividend_label, 0)

        equifax_label = wx.StaticText(
            self.panel, wx.ID_ANY, label=f'Equifax:\t\t{equifax}', name='equifax'
        )
        transunion_label = wx.StaticText(
            self.panel, wx.ID_ANY, label=f'Transunion:\t{tranunion}', name='transunion'
        )
        experian_label = wx.StaticText(
            self.panel, wx.ID_ANY, label=f'Experian:\t{experian}', name='experian'
        )
        credit_score_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Credit Scores')
        credit_score_sizer.Add(equifax_label, 0)
        credit_score_sizer.Add(transunion_label, 0)
        credit_score_sizer.Add(experian_label, 0)

        dashboard_sizer = wx.BoxSizer(wx.VERTICAL)
        dashboard_sizer.Add(net_worth_sizer, 0, wx.BOTTOM, 10)
        # dashboard_sizer.Add(wx.StaticLine(self.panel, size=(300, 5)))
        dashboard_sizer.Add(passive_income_sizer, 0, wx.BOTTOM, 10)
        dashboard_sizer.Add(credit_score_sizer, 0, wx.BOTTOM, 10)
        dashboard_sizer.Fit(self.panel)
        self.panel.SetSizer(dashboard_sizer)
