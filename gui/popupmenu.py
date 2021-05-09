import wx

class MyPopupMenu(wx.Menu):
    def __init__(self, parent, *args, **kw):
        super().__init__(*args, **kw)

        self.parent = parent

        mini = wx.MenuItem(self, wx.ID_ANY, 'Minimize')
        self.Append(mini)
        self.Bind(wx.EVT_MENU, self.minimize, mini)

        close = wx.MenuItem(self, wx.ID_ANY, 'Close')
        self.Append(close)
        self.Bind(wx.EVT_MENU, self.close, close)

    def minimize(self, event):
        self.parent.Iconize()

    def close(self, event):
        self.parent.Close()
