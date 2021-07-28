#! /usr/bin/python3

# fix DPI problems in fucking windows
# if wx.Platform == '__WXMSW__':
#     import ctypes
#     try:
#         ctypes.windll.shcore.SetProcessDpiAwareness(True)
#     except AttributeError:
#         pass

import wx
from gui.mainwindow import MainWindow
from functions.funcs import logger


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
    app = FinTrack(False)
    app.MainLoop()
