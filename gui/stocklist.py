import wx
import wx.dataview as dv
from functions.startup import logger, stocks_data_path, stocks_data, stock_list_headers
from functions.funcs import dump_data
from model.stocklist import StockListModel


class StockList():
    def __init__(self, panel, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.panel = panel

        self.data = stocks_data
        self.stock_list_model, self.stock_list = self.generate_stock_list(self.data)
        self.stock_list.Bind(dv.EVT_DATAVIEW_ITEM_EDITING_DONE, self.enable_save_button, self.stock_list)
        self.stock_list.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.enable_save_button, self.stock_list)

        self.save_button = wx.Button(self.panel, label='Save')
        self.save_button.Disable()
        self.save_button.Bind(wx.EVT_BUTTON, self.dump_stocks, self.save_button)

        self.add_stock_row_button = wx.Button(self.panel, label='Add Row')
        self.add_stock_row_button.Disable()
        self.add_stock_row_button.Bind(wx.EVT_BUTTON, self.add_stock_row, self.add_stock_row_button)

        self.delete_stock_rows_button = wx.Button(self.panel, label='Delete Row(s)')
        self.delete_stock_rows_button.Disable()
        self.delete_stock_rows_button.Bind(wx.EVT_BUTTON, self.delete_stock_rows, self.delete_stock_rows_button)

        button_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self.panel, label='Manage Stocks')
        button_sizer.Add(self.save_button, 0, wx.LEFT|wx.RIGHT, 5)
        button_sizer.Add(self.add_stock_row_button, 0, wx.LEFT|wx.RIGHT, 5)
        button_sizer.Add(self.delete_stock_rows_button, 0, wx.LEFT|wx.RIGHT, 5)

        self.stocks_sizer = wx.BoxSizer(wx.VERTICAL)
        self.stocks_sizer.Add(self.stock_list, 1, wx.EXPAND)
        self.stocks_sizer.Add(button_sizer, 0, wx.TOP|wx.BOTTOM)
        self.stocks_sizer.Fit(self.panel)
        self.panel.SetSizer(self.stocks_sizer)

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
            self.parent.SetStatusText('Unable to load header row.')
            logger.exception(f'load header row failed: {e}')

        for idx, val in enumerate(header_row):
            stock_list.AppendTextColumn(val, idx, width=len(val)*8, mode=dv.DATAVIEW_CELL_EDITABLE)

        for col in stock_list.Columns:
            col.Sortable = True
            col.Reorderable = True

        return stock_list_model, stock_list     

    def enable_save_button(self, event):
        """"""

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

        if self.save_button:
            self.save_button.Disable()