import wx


class AssetsDebts():
    """"""

    def __init__(self, panel, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        self.panel = panel

        self.splitter = wx.SplitterWindow(self.panel, wx.ID_ANY, style=wx.SP_LIVE_UPDATE)

        self.panelLeft = wx.Panel(self.splitter)
        wx.StaticText(self.panelLeft, -1, label='left side panel')
        self.panelRight = wx.Panel(self.splitter)
        wx.StaticText(self.panelRight, -1, label='right side panel')

        self.splitter.SplitVertically(self.panelLeft, self.panelRight)
