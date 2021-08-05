import time
import wx
import wx.aui as aui  # import wx.lib.agw.aui as aui
from settings import APP_NAME, STATUS_BAR_MESSAGE, ADMIN_ACCOUNT
from functions.funcs import logger
from gui.menubar import MyMenuBar
from gui.toolbar import MyToolbar
from gui.logindialog import LoginDialog
from gui.widgets.dashboard import Dashboard
from gui.widgets.financials import Financials
from gui.widgets.stocklist import StockList


login_status = False
stocklist_changed = False


class MainWindow(wx.Frame):
    """Main window GUI"""

    def __init__(self):
        super().__init__(
            parent=None,
            title=APP_NAME,
            style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        )
        self.panel = wx.Panel(self)

        icon = wx.Icon('logo.png', wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)

        self.toolbar = MyToolbar(
            self,
            style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT | wx.TB_DOCKABLE
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
            self.panel,
            wx.ID_ANY,
            style=aui.AUI_NB_WINDOWLIST_BUTTON | aui.AUI_NB_TAB_MOVE | aui.AUI_NB_TAB_SPLIT
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
        self.SetThemeEnabled(True)
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
        frame = tab.GetTopLevelParent()
        frame.SetClientSize(tab.GetMinSize())
        frame.SendSizeEvent()
        frame.CenterOnScreen()

    def login(self, event):
        """enbable admin mode"""

        dialog = LoginDialog(self, title='Admin Login')
        if dialog.ShowModal() == wx.ID_OK:
            username = dialog.username_field.GetValue()
            password = dialog.password_field.GetValue()

            if (username, password) != ADMIN_ACCOUNT:
                self.SetStatusText('Unable to login. Invalid credentials.')
                logger.warning(f'login failure: {username}:{password}')
                return None

            tool = self.toolbar.GetToolByPos(1)
            button = tool.GetControl()
            button.SetLabel('Logout')
            button.Unbind(wx.EVT_BUTTON, id=button.GetId(), handler=self.login)
            button.Bind(wx.EVT_BUTTON, self.logout)
            self.toolbar.Realize()

            menubar = self.GetMenuBar()
            item = menubar.FindItemById(102)
            item.SetItemLabel('Logout')
            menubar.Bind(wx.EVT_MENU, self.logout, id=102)

            self.stocklist.management(enable=True)

            logger.info(f'login successful: {username}.')

            global login_status
            login_status = True
        return None

    def logout(self, event):
        """disable admin mode"""

        tool = self.toolbar.GetToolByPos(1)
        button = tool.GetControl()
        button.SetLabel('Login')
        button.Unbind(wx.EVT_BUTTON, id=button.GetId(), handler=self.logout)
        button.Bind(wx.EVT_BUTTON, self.login)
        self.toolbar.Realize()

        menubar = self.GetMenuBar()
        item = menubar.FindItemById(102)
        item.SetItemLabel('Login')
        menubar.Bind(wx.EVT_MENU, self.login, id=102)

        self.stocklist.management(enable=False)
        self.stocklist.dump_stocks(wx.EVT_BUTTON)

        logger.info('logout successful.')

        global login_status
        login_status = False
        return None
