import wx
import wx.adv
import wx.lib.inspection
from settings import APP_NAME, VERSION, EMAIL, DEVELOPER
from settings import COPYRIGHT, LICENSE, WEBSITE


class MyMenuBar(wx.MenuBar):
    """Menubar"""

    def __init__(self, frame):
        super().__init__()
        self.frame = frame

        file_menu = wx.Menu()
        # file_menu.Append(102, '&Login', 'User login')
        # file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, '&Quit', f'Quit {APP_NAME}')

        view_menu = wx.Menu()
        self.sb_toggle = view_menu.Append(
            wx.ID_ANY, 'Show Statusbar', 'Show Statusbar', kind=wx.ITEM_CHECK
        )
        self.tb_toggle = view_menu.Append(
            wx.ID_ANY, 'Show Toolbar', 'Show Toolbar', kind=wx.ITEM_CHECK
        )
        # check both items on application start
        view_menu.Check(self.sb_toggle.GetId(), True)
        view_menu.Check(self.tb_toggle.GetId(), True)

        window_menu = wx.Menu()
        help_menu = wx.Menu()
        inspector = help_menu.Append(901, 'Widget Inspector', 'Widget Inspector')
        about = help_menu.Append(wx.ID_ABOUT)

        # self.Bind(wx.EVT_MENU, self.login, id=102)
        self.Bind(wx.EVT_MENU, self.quit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.about_dialog, about)
        self.Bind(wx.EVT_MENU, self.statusbar_toggle, self.sb_toggle)
        self.Bind(wx.EVT_MENU, self.toolbar_toggle, self.tb_toggle)
        self.Bind(wx.EVT_MENU, self.widget_inspector, inspector)

        self.Append(file_menu, 'File')
        self.Append(view_menu, 'View')
        self.Append(window_menu, 'Window')
        self.Append(help_menu, 'Help')

    def about_dialog(self, event):
        """About info box"""

        info = wx.adv.AboutDialogInfo()
        info.SetName(APP_NAME)
        info.SetVersion(VERSION)
        info.SetDescription(EMAIL)
        info.AddDeveloper(DEVELOPER)
        info.SetCopyright(COPYRIGHT)
        info.SetLicense(LICENSE)
        info.SetWebSite(*WEBSITE)
        wx.adv.GenericAboutBox(info)

    # def login(self, event):
    #     """enbable admin mode"""

    #     dialog = LoginDialog(self, title='Admin Login')
    #     if dialog.ShowModal() == wx.ID_OK:
    #         username = dialog.username_field.GetValue()
    #         password = dialog.password_field.GetValue()

    #         if (username, password) != ADMIN_ACCOUNT:
    #             self.frame.SetStatusText('Unable to login. Invalid credentials.')
    #             return None

    #         item = self.FindItemById(102)
    #         item.SetItemLabel('Logout')
    #         self.Bind(wx.EVT_MENU, self.logout, id=102)

    #     return None

    # def logout(self, event):
    #     """disable admin mode"""

    #     item = self.FindItemById(102)
    #     item.SetItemLabel('Login')
    #     self.Bind(wx.EVT_MENU, self.login, id=102)

    #     return None

    def statusbar_toggle(self, event):
        if self.sb_toggle.IsChecked():
            self.frame.statusbar.Show()
        else:
            self.frame.statusbar.Hide()

    def toolbar_toggle(self, event):
        if self.tb_toggle.IsChecked():
            self.frame.toolbar.Show()
        else:
            self.frame.toolbar.Hide()

    def widget_inspector(self, event):
        wx.lib.inspection.InspectionTool().Show()

    def quit(self, event):
        self.frame.Close()
