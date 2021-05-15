import wx

class MyToolbar(wx.ToolBar):
    def __init__(self, frame, *args, **kwargs):
        super().__init__(frame, *args, **kwargs)

        self.frame = frame

        self.search_field = wx.SearchCtrl(
            self,
            size=(300, -1),
            value='',
            style=wx.TE_PROCESS_ENTER
        )
        self.search_field.ShowCancelButton(True)
        self.search_field.ShowSearchButton(True)
        self.search_field.Bind(wx.EVT_TEXT, self.search)

        self.login_button = wx.Button(self, label='Login')
        self.login_button.Bind(wx.EVT_BUTTON, self.frame.login)

        self.AddControl(self.search_field)  # by pos: 0
        self.AddControl(self.login_button)  # by pos: 1
        self.SetToolBitmapSize((32, 32))

    def search(self, event):
        """"""

        filter = self.search_field.GetValue()
        self.frame.SetStatusText(f'Search..."{filter}"')
