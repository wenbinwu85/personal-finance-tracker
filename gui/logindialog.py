import wx


class LoginDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        if wx.Platform == '__WXMSW__':
            font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Courier')
        else:
            font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Monaco')
        self.SetFont(font)

        # ----- username -----
        username_sizer = wx.BoxSizer(wx.HORIZONTAL)
        username_label = wx.StaticText(self, -1, label='Username:')
        self.username_field = wx.TextCtrl(self)
        username_sizer.Add(username_label, 0, wx.ALL | wx.CENTER, 5)
        username_sizer.Add(self.username_field, 0, wx.ALL, 5)

        # ----- password -----
        password_sizer = wx.BoxSizer(wx.HORIZONTAL)
        password_label = wx.StaticText(self, -1, label='Password:')
        self.password_field = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        password_sizer.Add(password_label, 0, wx.ALL | wx.CENTER, 5)
        password_sizer.Add(self.password_field, 0, wx.ALL, 5)

        # ----- buttons -----
        button_sizer = wx.StdDialogButtonSizer()
        login_button = wx.Button(self, wx.ID_OK, label='Login')
        login_button.SetDefault()
        cancel_button = wx.Button(self, wx.ID_CANCEL)
        button_sizer.AddButton(login_button)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()

        # ----- main container -----
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(username_sizer, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(password_sizer, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(button_sizer, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Fit(self)
        self.SetSizer(main_sizer)
        self.CenterOnParent()
