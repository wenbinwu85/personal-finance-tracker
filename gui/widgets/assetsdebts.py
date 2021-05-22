import wx


class AssetsDebts():
    """"""

    def __init__(self, panel, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        self.panel = panel

        self.splitter = wx.SplitterWindow(self.panel, wx.ID_ANY, style=wx.SP_LIVE_UPDATE)
        self.left_pane = wx.Panel(self.splitter)
        self.right_pane = wx.Panel(self.splitter)

        self.assets_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.left_pane, 'Assets')
        self.debts_sizer = wx.StaticBoxSizer(wx.VERTICAL, self.right_pane, 'Debts')

        left_label = wx.StaticText(self.left_pane, -1, label='left side panel')
        right_label = wx.StaticText(self.right_pane, -1, label='right side panel')

        self.assets_sizer.Add(left_label)
        self.debts_sizer.Add(right_label)
        self.left_pane.SetSizer(self.assets_sizer)
        self.right_pane.SetSizer(self.debts_sizer)
        self.splitter.SplitVertically(self.left_pane, self.right_pane)
        self.splitter.SetMinimumPaneSize(700)

        widget_sizer = wx.BoxSizer(wx.VERTICAL)
        widget_sizer.Add(self.splitter, 1, wx.EXPAND, 0)
        self.panel.SetSizer(widget_sizer)
