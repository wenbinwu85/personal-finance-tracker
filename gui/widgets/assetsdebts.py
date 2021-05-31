import wx


class AssetsDebts():
    """"""

    def __init__(self, panel, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        self.panel = panel

        self.splitter = wx.SplitterWindow(
            self.panel, wx.ID_ANY, style=wx.SP_LIVE_UPDATE | wx.SP_THIN_SASH | wx.SP_ARROW_KEYS
        )
        left_pane = wx.Panel(self.splitter)
        right_pane = wx.Panel(self.splitter)
        self.assets_sizer = wx.StaticBoxSizer(wx.VERTICAL, left_pane, 'Assets')
        self.debts_sizer = wx.StaticBoxSizer(wx.VERTICAL, right_pane, 'Debts')

        left_label = wx.StaticText(left_pane, -1, label='left side panel')
        right_label = wx.StaticText(right_pane, -1, label='right side panel')

        self.assets_sizer.Add(left_label)
        self.debts_sizer.Add(right_label)
        left_pane.SetSizer(self.assets_sizer)
        right_pane.SetSizer(self.debts_sizer)
        self.splitter.SplitVertically(left_pane, right_pane)
        self.splitter.SetMinimumPaneSize(700)

        widget_sizer = wx.BoxSizer(wx.VERTICAL)
        widget_sizer.Add(self.splitter, 1, wx.EXPAND, 0)
        self.panel.SetSizer(widget_sizer)
