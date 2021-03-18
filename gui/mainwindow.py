import os
import time
import wx
import wx.dataview as dv

from settings.app import *
from helper.cjs import CJS
from model.stocklist import StockListModel
from gui.menubar import MyMenuBar
from gui.logindialog import LoginDialog


class MainWindow(wx.Frame):
    """Main window GUI"""

    def __init__(self):
        wx.Frame.__init__(
            self,
            parent=None,
            title=APP_NAME + VERSION,
            size=(1200, 800),
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
        self.login_button.Bind(wx.EVT_BUTTON, self.admin_login)

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

        self.data = self.load_data()
        self.stock_list_model, self.stock_list = self._generate_stock_list(self.data)
        self.Bind(dv.EVT_DATAVIEW_ITEM_EDITING_DONE, self.dump_data, self.stock_list)
        # self.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnValueChanged, self.stock_list)

        self.add_stock_row_button = wx.Button(self.panel, label='Add Row')
        self.add_stock_row_button.Disable()
        self.Bind(wx.EVT_BUTTON, self.add_stock_row, self.add_stock_row_button)
        self.delete_stock_rows_button = wx.Button(self.panel, label='Delete Row(s)')
        self.delete_stock_rows_button.Disable()
        self.Bind(wx.EVT_BUTTON, self.delete_stock_rows, self.delete_stock_rows_button)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.add_stock_row_button, 0, wx.LEFT|wx.RIGHT, 5)
        button_sizer.Add(self.delete_stock_rows_button, 0, wx.LEFT|wx.RIGHT, 5)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.stock_list, 1, wx.EXPAND, 5)
        self.main_sizer.Add(button_sizer, 0, wx.TOP|wx.BOTTOM, 5)
        self.main_sizer.Fit(self.panel)
        self.panel.SetSizer(self.main_sizer)

        self.CenterOnScreen()
        self.SetThemeEnabled(True)
        self.SetMinSize(self.GetBestSize())

    def add_time(self):
        """"""

        t = time.localtime(time.time())
        st = time.strftime("%Y-%b-%d   %I:%M:%S", t)
        self.SetStatusText(st, 2)

    def _get_path(self, folder, file):
        """"""

        filepath = os.path.join(
            os.path.dirname(__file__),
            '..',
            folder,
            file
        )
        return filepath

    def load_data(self):
        """"""

        loader = CJS()
        file_path = self._get_path(folder='data', file='stocks.csv')
        return loader.load(file_path)

    def dump_data(self, event):
        """"""

        dumper = CJS()
        file_path = self._get_path(folder='data', file='stocks.csv')
        dumper.dump(self.data, file_path)

    def _generate_stock_list(self, data):
        """"""

        stock_list_model = StockListModel(data)
        stock_list = dv.DataViewCtrl(
            self.panel,
            style = wx.BORDER_THEME | dv.DV_ROW_LINES | dv.DV_VERT_RULES | dv.DV_MULTIPLE
        )
        stock_list.AssociateModel(stock_list_model)

        loader = CJS()
        header_file_path = self._get_path(folder='data', file='stock_list_headers.csv')
        header_row = loader.load(header_file_path)[0]

        for idx, val in enumerate(header_row):
            stock_list.AppendTextColumn(val, idx+1, width=len(val)*8, mode=dv.DATAVIEW_CELL_EDITABLE)
        col0 = stock_list.PrependTextColumn('ID', 0, width=40)

        col0.Alignment = wx.ALIGN_RIGHT
        col0.Renderer.Alignment = wx.ALIGN_RIGHT
        col0.MinWidth = 30

        for col in stock_list.Columns:
            col.Sortable = True
            col.Reorderable = True
        
        col0.Reorderable = False

        return stock_list_model, stock_list

    def admin_login(self, event):
        """enbable admin mode"""

        dialog = LoginDialog(self, title='Admin Login')
        if dialog.ShowModal() == wx.ID_OK:
            username = dialog.username_field.GetValue()
            password = dialog.password_field.GetValue()
            if (username, password) != ADMIN_ACCOUNT:
                self.SetStatusText('Unable to login. Invalid credentials.')
                return None

            self.login_button.Hide()
            self.add_stock_row_button.Enable()
            self.delete_stock_rows_button.Enable()

            logout_button = wx.Button(self.toolbar, label='Logout')
            logout_button.Bind(wx.EVT_BUTTON, self.admin_logout)
            self.toolbar.AddControl(logout_button)
            self.toolbar.Realize()
            self.SetStatusText('Successfully logged in. Administrator functions enabled.')
            
        return None

    def admin_logout(self, event):
        """disable admin mode"""

        self.login_button.Show()
        self.add_stock_row_button.Disable()
        self.delete_stock_rows_button.Disable()

        count = self.toolbar.GetToolsCount()
        for _ in range(count-2):
            self.toolbar.DeleteToolByPos(2)
        self.SetTitle(APP_NAME + VERSION)
        self.SetStatusText('Successfully logged out.')
        return None

    def delete_stock_rows(self, event):
        items = self.stock_list.GetSelections()
        rows = [self.stock_list_model.GetRow(item) for item in items]
        self.stock_list_model.delete_rows(rows)

    def add_stock_row(self, event):
        new_row_id = len(self.stock_list_model.data) + 1
        col_count = self.stock_list.GetColumnCount()
        value = [str(new_row_id)] + ['' for i in range(col_count-1)]
        self.stock_list_model.add_row(value)

    def search(self, event):
        """"""

        filter = self.search_field.GetValue()
