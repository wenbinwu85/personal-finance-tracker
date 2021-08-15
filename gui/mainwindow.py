import time
import wx
import wx.aui as aui  # import wx.lib.agw.aui as aui
from settings import APP_NAME, STATUS_BAR_MESSAGE
from gui.menubar import MyMenuBar
from gui.toolbar import MyToolbar
from gui.widgets.dashboard import Dashboard
from gui.widgets.financials import Financials
from gui.widgets.stocklist import StockList


class MainWindow(wx.Frame):
    """Main window GUI"""

    def __init__(self):
        super().__init__(
            parent=None,
            title=APP_NAME,
            style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        )
        self.panel = wx.Panel(self)

        # icon = wx.Icon('logo.png', wx.BITMAP_TYPE_ANY)
        # self.SetIcon(icon)

        self.toolbar = MyToolbar(
            self, style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT
        )
        self.SetToolBar(self.toolbar)
        self.toolbar.Realize()

        self.SetMenuBar(MyMenuBar(self))

        self.CreateStatusBar()
        self.statusbar = self.GetStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-2, 150, 140])
        self.SetStatusText(STATUS_BAR_MESSAGE, 0)

        self.tabs = aui.AuiNotebook(
            self.panel, wx.ID_ANY, style=aui.AUI_NB_WINDOWLIST_BUTTON | aui.AUI_NB_TAB_MOVE
        )
        self.dashboard = Dashboard('Dashboard', self.tabs)
        self.financials = Financials('Financials', self.tabs)
        self.stocklist = StockList('Stocks', self.tabs)
        self.tabs.AddPage(self.dashboard, self.dashboard.name)
        self.tabs.AddPage(self.financials, self.financials.name)
        self.tabs.AddPage(self.stocklist, self.stocklist.name)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.tab_change, self.tabs)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.tabs)

        timer = wx.PyTimer(self.add_time)
        timer.Start(1000)

        self.panel.SetSizerAndFit(main_sizer)
        self.add_time()
        self.SetClientSize(self.dashboard.GetBestSize())
        self.CenterOnScreen()

    def add_time(self):
        """"""

        t = time.localtime(time.time())
        st = time.strftime("%Y-%b-%d   %I:%M:%S", t)
        self.SetStatusText(st, 2)


    def tab_change(self, event):
        """Resizes the main window frame to fit notbook page content"""

        tab = self.tabs.GetCurrentPage()
        frame = tab.GetTopLevelParent()  # TODO: frame == self
        frame.SetClientSize(tab.GetMinSize())
        frame.SendSizeEvent()
        frame.CenterOnScreen()
