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
        equifax = 800
        tranunion = 805
        experian = 799

        net_worth_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Net Worth:\t\t\t${net_worth}', name='net worth')
        total_assets_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Total Assets:\t\t\t${assets}', name='total assets')
        total_debts_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Total Debts:\t\t\t${debts}', name='total debts')
        da_ratio_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Debt to Asset Ratio:\t{da_ratio}%', name='da ratio')
        net_worth_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Net Worth')
        net_worth_sizer.Add(net_worth_label, 0)
        net_worth_sizer.Add(total_assets_label, 0)
        net_worth_sizer.Add(total_debts_label, 0)
        net_worth_sizer.Add(da_ratio_label, 0)

        equifax_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Equifax:\t\t{equifax}', name='equifax')
        transunion_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Transunion:\t{tranunion}', name='transunion')
        experian_label = wx.StaticText(self.panel, wx.ID_ANY, label=f'Experian:\t{experian}', name='experian')
        credit_score_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Credit Scores')
        credit_score_sizer.Add(equifax_label, 0)
        credit_score_sizer.Add(transunion_label, 0)
        credit_score_sizer.Add(experian_label, 0)

        dashboard_sizer = wx.BoxSizer(wx.VERTICAL)
        dashboard_sizer.Add(net_worth_sizer)
        dashboard_sizer.Add(credit_score_sizer)
        dashboard_sizer.Fit(self.panel)
        self.panel.SetSizer(dashboard_sizer)
