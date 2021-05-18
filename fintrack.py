#! /usr/bin/python3

import wx
from gui.mainwindow import MainWindow
from functions.startup import logger


# fix pixelated fonts in fucking windows
# if wx.Platform == '__WXMSW__':
#     import ctypes
#     try:
#         ctypes.windll.shcore.SetProcessDpiAwareness(True)
#     except AttributeError:
#         pass


class FinTrack(wx.App):
    """Main app class"""

    def OnInit(self):
        self.frame = MainWindow()
        self.SetTopWindow(self.frame)
        self.frame.Show()
        logger.info('Program started.')
        return True

    def OnExit(self):
        try:
            self.frame.dump_stocks('quit')
        except Exception as e:
            logger.exception(f'Failed to dump data during program exit: {e}')

        logger.info('Program exited by X button.')
        return super().OnExit()


if __name__ == '__main__':
    app = FinTrack()
    app.MainLoop()
