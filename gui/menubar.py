import os
import sys
import wx
import wx.adv
from settings.app import *
from functions.startup import logger


class MyMenuBar(wx.MenuBar):
    """menu bar """

    def __init__(self, frame):
        super().__init__()
        self.frame = frame

        menu1 = wx.Menu()
        menu1.Append(wx.ID_OPEN, '&Open', 'Open a file')
        menu1.Append(102, '&Login', 'User login')
        menu1.AppendSeparator()

        # qmi = wx.MenuItem(menu1, wx.ID_EXIT, '&Quit\tCtrl+Q')
        # qmi.SetBitmap(wx.ArtProvider.GetBitmap('exit.png'))
        # menu1.Append(qmi)

        menu1.Append(wx.ID_EXIT, '&Quit', 'Quit '+APP_NAME)

        view_menu = wx.Menu()
        self.sb_toggle = view_menu.Append(wx.ID_ANY, 'Show Statusbar', 'Show Statusbar', kind=wx.ITEM_CHECK)
        self.tb_toggle = view_menu.Append(wx.ID_ANY, 'Show Toolbar', 'Show Toolbar', kind=wx.ITEM_CHECK)
        
        # check both items on application start
        view_menu.Check(self.sb_toggle.GetId(), True)
        view_menu.Check(self.tb_toggle.GetId(), True)

        window_menu = wx.Menu()
        help_menu = wx.Menu()
        about = help_menu.Append(wx.ID_ABOUT)

        self.Bind(wx.EVT_MENU, self.open_dialog, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.login, id=102)
        self.Bind(wx.EVT_MENU, self.quit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.about_dialog, about)
        self.Bind(wx.EVT_MENU, self.statusbar_toggle, self.sb_toggle)
        self.Bind(wx.EVT_MENU, self.toolbar_toggle, self.tb_toggle)

        self.Append(menu1, 'File')
        self.Append(view_menu, 'View')
        self.Append(window_menu, 'Window')
        self.Append(help_menu, 'Help')
    
    def about_dialog(self, event):
        """About dialog box """

        info = wx.adv.AboutDialogInfo()
        info.SetName(APP_NAME)
        info.SetVersion(VERSION)
        info.SetDescription(EMAIL)
        info.AddDeveloper(DEVELOPER)
        info.SetCopyright(COPYRIGHT)  
        info.SetLicense(LICENSE)
        info.SetWebSite(*WEBSITE)
        wx.adv.AboutBox(info)
        return None
    
    def login(self, event):
        """enbable admin mode"""

        self.frame.login(event)


    def logout(self, event):
        """"""

        self.frame.logout(event)


    def open_dialog(self, event):
        """"""

        wildcards = 'CSV file (*.csv)|*.csv|'

        with wx.FileDialog(
            self,
            message='Choose data file',
            defaultDir=os.getcwd(),
            defaultFile='',
            wildcard=wildcards,
            style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
            ) as dialog:

            if dialog.ShowModal() == wx.ID_OK:
                self.frame.reload_data(dialog.GetPath())
                self.frame.SetStatusText(f'New data loaded form {dialog.GetPath()}.')
                logger.info('New data load successful.')

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

    def quit(self, event):
        try:
            self.frame.dump_stocks('quit')
        except Exception as e:
            logger.exception(f'Failed to dump data during program exit: {e}')

        logger.info('Program exited by file->quit.')
        sys.exit()
