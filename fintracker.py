import wx
from gui.mainwindow import MainWindow
from functions.startup import logger
from gui.logindialog import LoginDialog


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
        logger.info('Program started.')
        self.frame = MainWindow()
        self.frame.Show()
        return True

    def OnExit(self):
        try:
            self.frame.dump_stocks('exit')
        except Exception as e:
            logger.exception(f'Failed to dump data during program exit: {e}')

        logger.info('Program exited by X button.')
        return super().OnExit()


if __name__ == '__main__':
    app = FinTrack()
    app.MainLoop()
