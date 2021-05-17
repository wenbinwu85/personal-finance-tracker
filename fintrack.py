import wx
from gui.mainwindow import MainWindow
from functions.startup import logger


# ----- fix pixelated fonts in windows -----
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass
#-------------------------------------------


class FinTrack(wx.App):
    """Main app class"""

    def OnInit(self):
        self.frame = MainWindow()

        if wx.Platform == '__WXMSW__':
            font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Courier')
        else:
            font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Monaco')
        self.frame.SetFont(font)

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
