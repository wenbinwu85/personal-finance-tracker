import wx
from gui.mainwindow import MainWindow


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
        self.frame = MainWindow()
        self.frame.Show()
        return True


if __name__ == '__main__':
    app = Finman()
    app.MainLoop()
