import wx


def make_credit_score_widget(parent, label):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    cc_label = wx.StaticText(parent, -1, label=label)
    text_field = wx.TextCtrl(parent)
    sizer.Add(cc_label, 0, wx.ALL, 5)
    sizer.Add(text_field, 1, wx.ALL, 5)
    return sizer, text_field


class CreditScoresUpdateDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(
            style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX),
            *args,
            **kwargs
        )

        equifax_sizer, self.equifax_field = make_credit_score_widget(self, 'Equifax:')
        transunion_sizer, self.transunion_field = make_credit_score_widget(self, 'Transunion:')
        experian_sizer, self.experian_field = make_credit_score_widget(self, 'Experian:')
        avg_sizer, self.avg_field = make_credit_score_widget(self, 'Average:')

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
        self.ShowWithEffect(True)
