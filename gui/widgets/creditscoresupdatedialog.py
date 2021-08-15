import wx


class CreditScoresUpdateDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(
            style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX),
            *args,
            **kwargs
        )

        # ----- Experian -----
        equifax_sizer = wx.BoxSizer(wx.HORIZONTAL)
        equifax_label = wx.StaticText(self, -1, label='Equifax:')
        self.equifax_field = wx.TextCtrl(self)
        equifax_sizer.Add(equifax_label, 0, wx.ALL, 5)
        equifax_sizer.Add(self.equifax_field, 1, wx.ALL, 5)

        # ----- Transunion -----
        transunion_sizer = wx.BoxSizer(wx.HORIZONTAL)
        transunion_label = wx.StaticText(self, -1, label='Transunion:')
        self.transunion_field = wx.TextCtrl(self)
        transunion_sizer.Add(transunion_label, 0, wx.ALL, 5)
        transunion_sizer.Add(self.transunion_field, 1, wx.ALL, 5)

        # ----- Experian -----
        experian_sizer = wx.BoxSizer(wx.HORIZONTAL)
        experian_label = wx.StaticText(self, -1, label='Experian:')
        self.experian_field = wx.TextCtrl(self)
        experian_sizer.Add(experian_label, 0, wx.ALL, 5)
        experian_sizer.Add(self.experian_field, 1, wx.ALL, 5)

        # ----- National Average -----
        avg_sizer = wx.BoxSizer(wx.HORIZONTAL)
        avg_label = wx.StaticText(self, -1, label='Average:')
        self.avg_field = wx.TextCtrl(self)
        avg_sizer.Add(avg_label, 0, wx.ALL, 5)
        avg_sizer.Add(self.avg_field, 1, wx.ALL | wx.GROW, 5)

        # ----- buttons -----
        button_sizer = wx.StdDialogButtonSizer()
        login_button = wx.Button(self, wx.ID_OK, label='Update')
        login_button.SetDefault()
        cancel_button = wx.Button(self, wx.ID_CANCEL)
        button_sizer.AddButton(login_button)
        button_sizer.AddButton(cancel_button)
        button_sizer.Realize()

        # ----- main container -----
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(equifax_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        main_sizer.Add(transunion_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        main_sizer.Add(experian_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        main_sizer.Add(avg_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        main_sizer.Add(button_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.SetSizerAndFit(main_sizer)
        self.CenterOnParent()
