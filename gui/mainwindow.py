import time
import wx

from settings.app import APP_NAME, VERSION, STATUS_BAR_MESSAGE
from settings.user import user_settings, stock_data_path
from functions.funcs import logger, load_data, dump_data
from gui.menubar import MyMenuBar
from gui.toolbar import MyToolbar
from gui.logindialog import LoginDialog
from gui.widgets.stocklist import StockList


login_status = False
stocklist_changed = False


class MainWindow(wx.Frame):
    """Main window GUI"""

    def __init__(self):
        super().__init__(
            parent=None,
            title=APP_NAME+VERSION,
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
        self.tabs.AddPage(self.summary_tab, 'Summary')

        self.net_worth_tab = wx.Panel(self.tabs, wx.ID_ANY)
        self.tabs.AddPage(self.net_worth_tab, 'Net Worth')

        self.stocks_tab = wx.Panel(self.tabs, wx.ID_ANY)
        self.stocks_list = StockList(self.stocks_tab)
        self.tabs.AddPage(self.stocks_tab, 'Stock Positions')

        self.history_tab = wx.Panel(self.tabs, wx.ID_ANY)
        self.tabs.AddPage(self.history_tab, 'History')

        self.tabs.SetSize(self.tabs.GetBestSize())

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.tabs, 1, wx.EXPAND, 0)
        self.panel.SetSizer(self.main_sizer)

        self.timer = wx.PyTimer(self.add_time)
        self.timer.Start(1000)
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

    def dump_stocks(self, event):
        """"""

        try:
            dump_data(self.data, stocks_data_path)
            print('dumped:', stocks_data_path)
        except Exception as e:
            self.SetStatusText('Failed to dump data to file.')
            logger.exception(f'data dump failed: {e}')
        else:
            if event != 'quit':
                self.SetStatusText(f'Data dumped to {stocks_data_path}.')
            logger.info('data dump successful.')

        if self.stocks_list.save_button:
            self.stocks_list.save_button.Disable()

    def reload_data(self, data_path):
        """"""

        global stocks_data_path 
        stocks_data_path = data_path

        self.stock_list.SelectAll()
        items = self.stock_list.GetSelections()
        rows = [self.stock_list_model.GetRow(item) for item in items]
        try:
            self.stock_list_model.delete_rows(rows)
        except Exception as e:
            self.SetStatusText('Failed to delete rows.')
            logger.exception(f'delete rows failure: {e}')

        self.data = load_data(stocks_data_path)
        for i in self.data:
            try:
                self.stock_list_model.add_row(i)
            except Exception as e:
                self.SetStatusText('Failed to add new row.')
                logger.exception(f'add new row failure: {e}')

        user_settings['stocks_data_path'] = stocks_data_path
        dump_data(data=user_settings, file=USER_SETTINGS_PATH)
        self.SetStatusText(f'New data loaded form {stocks_data_path}.')
        self.Refresh()

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

            self.add_stock_row_button.Enable()
            self.delete_stock_rows_button.Enable()

            self.SetStatusText('Successfully logged in.')
            logger.info(f'login successful: {username}.')

            global login_status
            login_status = True
        return None

    def logout(self, event):
        """disable admin mode"""

        try:
            self.dump_stocks(None)
            print('dumped on logout:', stocks_data_path)
        except Exception as e:
            self.SetStatusText('Failed to dump data during logout.')
            logger.exception(f'dump data during admin logout: {e}')

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

        self.save_button.Disable()
        self.add_stock_row_button.Disable()
        self.delete_stock_rows_button.Disable()

        self.SetStatusText('Successfully logged out.')
        logger.info('logout successful.')

        global login_status
        login_status = False
        return None
