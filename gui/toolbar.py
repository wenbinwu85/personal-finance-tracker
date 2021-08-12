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

        self.AddControl(self.search_field)  # by pos: 0
        # self.SetToolBitmapSize((32, 32))

    def search(self, event):
        """"""

        filter = self.search_field.GetValue()
        self.frame.SetStatusText(f'Search..."{filter}"')
