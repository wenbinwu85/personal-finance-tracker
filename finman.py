import wx
from gui.mainwindow import MainWindow
from functions.logger import logger

# ----- fix pixelated fonts in windows -----
import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except:
    pass
#-------------------------------------------
    

class Finman(wx.App):
    """My app class"""

    def OnInit(self):
        logger.info('Program started.')
        self.frame = MainWindow()
        self.frame.Show()
        return True

    def OnExit(self):
        self.frame.dump_data(None)
        logger.info('Program exited by X button.')
        return super().OnExit()


if __name__ == '__main__':
    app = Finman()
    app.MainLoop()
