# fix pixelated fonts in fucking windows
# if wx.Platform == '__WXMSW__':
#     import ctypes
#     try:
#         ctypes.windll.shcore.SetProcessDpiAwareness(True)
#     except AttributeError:
#         pass

import wx
import os
from gui.mainwindow import MainWindow
from functions.funcs import logger


appdir = os.path.abspath(os.path.dirname(__file__))


class FinTrack(wx.App):
    """Main app class"""

    def OnInit(self):
        self.frame = MainWindow()
        self.SetTopWindow(self.frame)
        self.frame.Show()
        logger.info('Program started.')
        return True

    def OnExit(self):
        return super().OnExit()


if __name__ == '__main__':
    app = FinTrack()
    app.MainLoop()
