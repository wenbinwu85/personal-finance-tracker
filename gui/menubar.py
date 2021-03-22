import sys
import wx
import wx.adv
from settings.app import *
from functions.logger import logger


class MyMenuBar(wx.MenuBar):
    """menu bar """

    def __init__(self, frame):
        super().__init__()
        self.frame = frame

        menu1 = wx.Menu()
        menu1.Append(101, 'Open', 'Open a file')
        menu1.Append(102, 'Login', 'User login')
        menu1.AppendSeparator()
        menu1.Append(109, 'Exit', 'Exit')
        window_menu = wx.Menu()
        help_menu = wx.Menu()
        about = help_menu.Append(wx.ID_ABOUT)

        self.Bind(wx.EVT_MENU, self.open_dialog, id=101)
        self.Bind(wx.EVT_BUTTON, self.login, id=102)
        self.Bind(wx.EVT_MENU, self.quit, id=109)
        self.Bind(wx.EVT_MENU, self.about_dialog, about)

        self.Append(menu1, 'File')
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

    def open_dialog(self, event):
        """"""
    
    def login(self, event):
        """"""


    def quit(self, event):
        try:
            self.frame.dump_stocks(event)
        except Exception as e:
            logger.exception(f'Failed to dump data during program exit: {e}')

        logger.info('Program exited by file->exit.')
        sys.exit()
