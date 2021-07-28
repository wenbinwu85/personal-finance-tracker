import time
import wx
# import wx.lib.agw.aui as aui
# import wx.aui
from settings import APP_NAME, VERSION, STATUS_BAR_MESSAGE, ADMIN_ACCOUNT
from functions.funcs import logger
from gui.menubar import MyMenuBar
from gui.toolbar import MyToolbar
from gui.logindialog import LoginDialog
from gui.widgets.dashboard import Dashboard
from gui.widgets.assetsdebts import AssetsDebts
from gui.widgets.stocklist import StockList


login_status = False
stocklist_changed = False


# class MainPanel(wx.Panel):
#     def __init__(self, parent):
#         super().__init__(parent)

class MainWindow(wx.Frame):
    """Main window GUI"""

    def __init__(self):
        super().__init__(
            parent=None,
            title=APP_NAME+VERSION,
            size=(1700, 650),
            style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        )

        icon = wx.Icon('logo.png', wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)

        self.toolbar = MyToolbar(
            self,
            style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT
        )
        self.SetToolBar(self.toolbar)
        self.toolbar.Realize()

        self.SetMenuBar(MyMenuBar(self))

        self.CreateStatusBar()
        self.statusbar = self.GetStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-2, 150, 140])
        self.SetStatusText(STATUS_BAR_MESSAGE, 0)

        self.panel = wx.Panel(self)

        self.tabs = wx.Notebook(
            self.panel,
            wx.ID_ANY,
            # agwStyle=aui.AUI_NB_TAB_SPLIT | aui.AUI_NB_TAB_MOVE | aui.AUI_NB_TAB_EXTERNAL_MOVE
            #     | aui.AUI_NB_SCROLL_BUTTONS | aui.AUI_NB_CLOSE_ON_ACTIVE_TAB | aui.AUI_NB_SMART_TABS
            #     | aui.AUI_NB_ORDER_BY_ACCESS
        )

        self.dashboard_tab = wx.Panel(self.tabs, wx.ID_ANY)
        self.dashboard = Dashboard(self.dashboard_tab, 'Dashboard')
        self.tabs.AddPage(self.dashboard_tab, self.dashboard.name)

        self.assets_debts_tab = wx.Panel(self.tabs, wx.ID_ANY)
        self.assets_debts = AssetsDebts(self.assets_debts_tab, wx.ID_ANY)
        self.tabs.AddPage(self.assets_debts_tab, 'Assets & Debts')

        self.stocks_tab = wx.Panel(self.tabs, wx.ID_ANY)
        self.stocks_list = StockList(self.stocks_tab, 'Stock Positions')
        self.tabs.AddPage(self.stocks_tab, self.stocks_list.name)

        self.graphs_tab = wx.Panel(self.tabs, wx.ID_ANY)
        self.graphs_list = StockList(self.graphs_tab, 'Investment Graphs')
        self.tabs.AddPage(self.graphs_tab, self.graphs_list.name)

        self.history_tab = wx.Panel(self.tabs, wx.ID_ANY)
        self.history_list = StockList(self.history_tab, 'History')
        self.tabs.AddPage(self.history_tab, self.history_list.name)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.tabs, 1, wx.EXPAND)
        main_sizer.Fit(self.panel)
        self.panel.SetSizer(main_sizer)

        timer = wx.PyTimer(self.add_time)
        timer.Start(1000)
        self.add_time()

        self.SetThemeEnabled(True)
        self.SetMinSize(self.tabs.GetBestSize())
        self.Layout()
        self.CenterOnScreen()

    def add_time(self):
        """"""

        t = time.localtime(time.time())
        st = time.strftime("%Y-%b-%d   %I:%M:%S", t)
        self.SetStatusText(st, 2)

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

            self.stocks_list.management(enable=True)

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

        self.stocks_list.management(enable=False)
        self.stocks_list.dump_stocks(wx.EVT_BUTTON)

        logger.info('logout successful.')

        global login_status
        login_status = False
        return None
