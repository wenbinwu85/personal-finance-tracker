import wx


class LoginDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super().__init__(
            style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX),
            *args,
            **kw
        )

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

        self.SetSizerAndFit(main_sizer)
        self.CenterOnParent()
        self.ShowWithEffect(True)
