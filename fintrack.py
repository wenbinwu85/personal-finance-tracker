#! /usr/bin/python3

import wx
from gui.mainwindow import MainWindow


class FinTrack(wx.App):
    """Main app class"""

    def OnInit(self):
        self.frame = MainWindow()

        self.frame.ShowWithEffect(True)
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        return super().OnExit()


if __name__ == '__main__':
    app = FinTrack(False)
    app.MainLoop()
