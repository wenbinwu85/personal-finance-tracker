import time
import wx

from settings.app import APP_NAME, VERSION, STATUS_BAR_MESSAGE, ADMIN_ACCOUNT
from functions.funcs import logger
from gui.menubar import MyMenuBar
from gui.toolbar import MyToolbar
from gui.logindialog import LoginDialog
from gui.widgets. dashboard import Dashboard
from gui.widgets.stocklist import StockList


login_status = False
stocklist_changed = False


class MainWindow(wx.Frame):
    """Main window GUI"""

    def __init__(self):
        super().__init__(
            parent=None,
            title=APP_NAME + VERSION,
            size=(1400, 640),
            style=wx.DEFAULT_FRAME_STYLE  # & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        )

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

        self.tabs = wx.Notebook(self.panel, wx.ID_ANY)
        self.summary_tab = wx.Panel(self.tabs, wx.ID_ANY)
        self.dashboard = Dashboard(self.summary_tab, 'Dashboard')
        self.tabs.AddPage(self.summary_tab, self.dashboard.name)
        self.net_worth_tab = wx.Panel(self.tabs, wx.ID_ANY)
        self.tabs.AddPage(self.net_worth_tab, 'Net Worth')
        self.stocks_tab = wx.Panel(self.tabs, wx.ID_ANY)
        self.stocks_list = StockList(self.stocks_tab, 'Stock Positions')
        self.tabs.AddPage(self.stocks_tab, self.stocks_list.name)
        self.tabs.SetSize(self.tabs.GetBestSize())

        main_sizer = wx.BoxSizer(wx.VERTICAL) 
        main_sizer.Add(self.tabs, 1, wx.EXPAND)
        self.panel.SetSizer(main_sizer)

        timer = wx.PyTimer(self.add_time)
        timer.Start(1000)
        self.add_time()

        self.SetThemeEnabled(True)
        self.SetMinSize(self.tabs.GetSize())
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
