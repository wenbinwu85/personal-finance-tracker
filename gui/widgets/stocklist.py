import wx
import wx.dataview as dv
from settings.user import stock_header_path, stock_data_path
from functions.funcs import logger, load_data, dump_data
from functions.exceptions import StockListWidgetException
from model.stocklist import StockListModel


class StockList():
    def __init__(self, panel, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.panel = panel

        self.stock_list_model, self.stock_list = self.generate_stock_list()
        self.stock_list.Bind(dv.EVT_DATAVIEW_ITEM_EDITING_DONE, self.enable_save_button)
        self.stock_list.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.enable_save_button)

        self.open_button = wx.Button(self.panel, label='Open')
        self.open_button.Bind(wx.EVT_BUTTON, self.load_stocks)
        self.open_button.Disable()

        self.save_button = wx.Button(self.panel, label='Save')
        self.save_button.Bind(wx.EVT_BUTTON, self.dump_stocks)
        self.save_button.Disable()

        self.add_row_button = wx.Button(self.panel, label='Add Row')
        self.add_row_button.Bind(wx.EVT_BUTTON, self.add_stock_row)
        self.add_row_button.Disable()

        self.delete_row_button = wx.Button(self.panel, label='Delete Row(s)')
        self.delete_row_button.Bind(wx.EVT_BUTTON, self.delete_stock_rows)
        self.delete_row_button.Disable()

        button_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self.panel, label='Manage Stocks')
        button_sizer.Add(self.open_button, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 5)
        button_sizer.AddSpacer(10)
        button_sizer.Add(self.save_button, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 5)
        button_sizer.Add(self.add_row_button, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 5)
        button_sizer.Add(self.delete_row_button, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, 5)

        stocks_sizer = wx.BoxSizer(wx.VERTICAL)
        stocks_sizer.Add(self.stock_list, 1, wx.EXPAND)
        stocks_sizer.Add(button_sizer, 0)
        stocks_sizer.Fit(self.panel)
        self.panel.SetSizer(stocks_sizer)

    def generate_stock_list(self):
        """"""
        try:
            self.header_row = load_data(stock_header_path)[0]
        except Exception as e:
            error_msg = f'Failed to load stock list header from {stock_header_path}:\n{e}'
            logger.exception(error_msg)
            raise StockListWidgetException(error_msg)
        else:
            logger.info(f'Stock list headers loaded from {stock_header_path}.')

        try:
            self.stock_data = load_data(stock_data_path)
        except Exception as e:
            error_msg = f'Failed to load stock data from {stock_data_path}:\n{e}'
            logger.exception(error_msg)
            raise StockListWidgetException(error_msg)
        else:
            logger.info(f'Stock data loaded from {stock_data_path}.')

        stock_list_model = StockListModel(self.stock_data)
        stock_list = dv.DataViewCtrl(
            self.panel,
            style=wx.BORDER_THEME | dv.DV_ROW_LINES | dv.DV_VERT_RULES | dv.DV_MULTIPLE
        )
        stock_list.AssociateModel(stock_list_model)
        stock_list.EnableSystemTheme()

        for idx, val in enumerate(self.header_row):
            stock_list.AppendTextColumn(val, idx, width=len(val) * 8, mode=dv.DATAVIEW_CELL_EDITABLE)

        for col in stock_list.Columns:
            col.Sortable = True
            col.Reorderable = True

        return stock_list_model, stock_list

    def load_stocks(self, event):
        """"""


    def enable_save_button(self, event):
        """"""
        self.save_button.Enable()

    def add_stock_row(self, event):
        """"""
        col_count = self.stock_list.GetColumnCount()
        value = ['New Stock'] + ['' for i in range(col_count - 1)]
        try:
            self.stock_list_model.add_row(value)
        except Exception as e:
            error_msg = f'Failed to add new row: {e}'
            logger.exception(error_msg)
            raise StockListWidgetException(error_msg)
        else:
            logger.info('Added new row successfully.')
            self.save_button.Enable()

    def delete_stock_rows(self, event):
        """"""
        items = self.stock_list.GetSelections()
        rows = [self.stock_list_model.GetRow(item) for item in items]
        try:
            self.stock_list_model.delete_rows(rows)
        except Exception as e:
            error_msg = f'Failed to delete rows: {e}'
            logger.exception(error_msg)
            raise StockListWidgetException(error_msg)
        else:
            logger.info('Deleted rows successully.')
            self.save_button.Enable()

    def dump_stocks(self, event):
        """"""
        try:
            dump_data(self.stock_data, stock_data_path)
        except Exception as e:
            error_msg = f'data dump failed: {e}'
            logger.exception(error_msg)
            raise StockListWidgetException(error_msg)
        else:
            logger.info('Data dumped successfully.')
            self.save_button.Disable()
