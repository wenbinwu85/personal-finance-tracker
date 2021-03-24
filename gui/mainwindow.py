import time
import wx
import wx.dataview as dv

from settings.app import *
from functions.startup import logger, user_settings, stock_list_headers, stocks_data, stocks_data_path
from functions.funcs import load_data, dump_data
from model.stocklist import StockListModel
from gui.menubar import MyMenuBar
from gui.logindialog import LoginDialog


login_status = False

class MainWindow(wx.Frame):
    """Main window GUI"""

    def __init__(self):
        wx.Frame.__init__(
            self,
            parent=None,
            title=APP_NAME+VERSION,
            size=(1200, 600),
            style=wx.DEFAULT_FRAME_STYLE #  & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
            )
        self.panel = wx.Panel(self)

        if wx.Platform == '__WXMSW__':
            font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Courier')
        else:
            font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, False, 'Monaco')
        self.SetFont(font)

        self.SetMenuBar(MyMenuBar(self))

        self.toolbar = self.CreateToolBar(
            style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT
            )
        self.toolbar.SetToolBitmapSize((32, 32))

        self.search_field = wx.SearchCtrl(
            self.toolbar,
            size=(300, -1),
            value='',
            style=wx.TE_PROCESS_ENTER
        )
        self.search_field.ShowCancelButton(True)
        self.search_field.ShowSearchButton(True)
        self.search_field.Bind(wx.EVT_TEXT, self.search)

        self.login_button = wx.Button(self.toolbar, label='Login')
        self.login_button.Bind(wx.EVT_BUTTON, self.login)

        self.toolbar.AddControl(self.search_field)
        self.toolbar.AddControl(self.login_button)
        self.toolbar.Realize()

        self.CreateStatusBar()
        statusbar = self.GetStatusBar()
        statusbar.SetFieldsCount(3)
        statusbar.SetStatusWidths([-2, 150, 140])
        self.SetStatusText(STATUS_BAR_MESSAGE, 0)

        self.timer = wx.PyTimer(self.add_time)
        self.timer.Start(1000)
        self.add_time()

        self.data = stocks_data
        self.stock_list_model, self.stock_list = self.generate_stock_list(self.data)
        self.Bind(dv.EVT_DATAVIEW_ITEM_EDITING_DONE, self.enable_save_button, self.stock_list)
        self.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.enable_save_button, self.stock_list)

        self.save_button = wx.Button(self.panel, label='Save')
        self.save_button.Disable()
        self.Bind(wx.EVT_BUTTON, self.dump_stocks, self.save_button)
        self.add_stock_row_button = wx.Button(self.panel, label='Add Row')
        self.add_stock_row_button.Disable()
        self.Bind(wx.EVT_BUTTON, self.add_stock_row, self.add_stock_row_button)
        self.delete_stock_rows_button = wx.Button(self.panel, label='Delete Row(s)')
        self.delete_stock_rows_button.Disable()
        self.Bind(wx.EVT_BUTTON, self.delete_stock_rows, self.delete_stock_rows_button)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.save_button, 0, wx.LEFT|wx.RIGHT, 5)
        button_sizer.Add(self.add_stock_row_button, 0, wx.LEFT|wx.RIGHT, 5)
        button_sizer.Add(self.delete_stock_rows_button, 0, wx.LEFT|wx.RIGHT, 5)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.stock_list, 1, wx.EXPAND, 5)
        self.main_sizer.Add(button_sizer, 0, wx.TOP|wx.BOTTOM, 5)
        self.main_sizer.Fit(self.panel)
        self.panel.SetSizer(self.main_sizer)

        self.CenterOnScreen()
        self.SetThemeEnabled(True)
        self.SetMinSize(self.main_sizer.GetSize())

    def add_time(self):
        """"""

        t = time.localtime(time.time())
        st = time.strftime("%Y-%b-%d   %I:%M:%S", t)
        self.SetStatusText(st, 2)

    def enable_save_button(self, event):
        """"""

        self.save_button.Enable()

    def dump_stocks(self, event):
        """"""

        try:
            dump_data(self.data, stocks_data_path)
            print('dumped:', stocks_data_path)
        except Exception as e:
            self.SetStatusText('Failed to dump data to file.')
            logger.exception(f'data dump failed: {e}')
        else:
            if event != 'exit':
                self.SetStatusText(f'Data dumped to {stocks_data_path}.')
            logger.info('data dump successful.')

        if self.save_button:
            self.save_button.Disable()

    def reload_data(self, path):
        """"""

        self.stock_list.SelectAll()
        items = self.stock_list.GetSelections()
        rows = [self.stock_list_model.GetRow(item) for item in items]
        try:
            self.stock_list_model.delete_rows(rows)
        except Exception as e:
            self.SetStatusText('Failed to delete rows.')
            logger.exception(f'delete rows failure: {e}')

        self.data = load_data(path)
        for i in self.data:
            try:
                self.stock_list_model.add_row(i)
            except Exception as e:
                self.SetStatusText('Failed to add new row.')
                logger.exception(f'add new row failure: {e}')

        user_settings['stocks_data_path'] = path
        dump_data(data=user_settings, file=USER_SETTINGS_PATH)

        global stocks_data_path
        stocks_data_path = path
        print(path)
        print(stocks_data_path)

    def generate_stock_list(self, data):
        """"""

        stock_list_model = StockListModel(data)
        stock_list = dv.DataViewCtrl(
            self.panel,
            style = wx.BORDER_THEME | dv.DV_ROW_LINES | dv.DV_VERT_RULES | dv.DV_MULTIPLE
        )
        stock_list.AssociateModel(stock_list_model)
        stock_list.EnableSystemTheme()

        try:
            header_row = stock_list_headers[0]
        except Exception as e:
            self.SetStatusText('Unable to load header row.')
            logger.exception(f'load header row failed: {e}')

        for idx, val in enumerate(header_row):
            stock_list.AppendTextColumn(val, idx, width=len(val)*8, mode=dv.DATAVIEW_CELL_EDITABLE)

        for col in stock_list.Columns:
            col.Sortable = True
            col.Reorderable = True

        return stock_list_model, stock_list

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

            self.login_button.Hide()
            self.add_stock_row_button.Enable()
            self.delete_stock_rows_button.Enable()

            logout_button = wx.Button(self.toolbar, label='Logout')
            logout_button.Bind(wx.EVT_BUTTON, self.logout)
            self.toolbar.AddControl(logout_button)
            self.toolbar.Realize()

            menubar = self.GetMenuBar()
            item = menubar.FindItemById(102)
            item.SetItemLabel('Logout')
            menubar.Bind(wx.EVT_MENU, menubar.logout, id=102)

            self.SetStatusText('Successfully logged in.')
            logger.info(f'login successful: {username}.')
        return None

    def logout(self, event):
        """disable admin mode"""

        try:
            self.dump_stocks(None)
            print('dumped on logout:', stocks_data_path)
        except Exception as e:
            self.SetStatusText('Failed to dump data during logout.')
            logger.exception(f'dump data during admin logout: {e}')

        self.login_button.Show()
        self.save_button.Disable()
        self.add_stock_row_button.Disable()
        self.delete_stock_rows_button.Disable()

        count = self.toolbar.GetToolsCount()
        for _ in range(count-2):
            self.toolbar.DeleteToolByPos(2)

        menubar = self.GetMenuBar()
        item = menubar.FindItemById(102)
        item.SetItemLabel('Login')
        menubar.Bind(wx.EVT_MENU, menubar.login, id=102)

        self.SetStatusText('Successfully logged out.')
        logger.info('logout successful.')
        return None

    def delete_stock_rows(self, event):
        """"""

        items = self.stock_list.GetSelections()
        rows = [self.stock_list_model.GetRow(item) for item in items]
        try:
            self.stock_list_model.delete_rows(rows)
        except Exception as e:
            self.SetStatusText('Failed to delete rows.')
            logger.exception(f'delete rows failure: {e}')
        self.save_button.Enable()

    def add_stock_row(self, event):
        """"""

        col_count = self.stock_list.GetColumnCount()
        value = ['New'] + ['' for i in range(col_count-1)]
        try:
            self.stock_list_model.add_row(value)
        except Exception as e:
            self.SetStatusText('Failed to add new row.')
            logger.exception(f'add new row failure: {e}')
        self.save_button.Enable()

    def search(self, event):
        """"""

        filter = self.search_field.GetValue()
