import wx
import wx.dataview as dv
from settings import STOCKLIST_DATA_PATH
from functions.funcs import logger, load_data_from, dump_data
from functions.exceptions import StockListWidgetException
from model.stocklist import DVIListModel


class StockList(wx.Panel):
    """"""

    def __init__(self, name, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.main_window = parent.GetTopLevelParent()
        self.name = name

        self.stock_list_model, self.stock_list = self.generate_stock_list()
        # self.stock_list.Bind(dv.EVT_DATAVIEW_ITEM_EDITING_DONE, self.enable_save_button)
        # self.stock_list.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.enable_save_button)
        self.stock_list.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.stock_list_context_menu)

        stocklist_sizer = wx.BoxSizer(wx.VERTICAL)
        stocklist_sizer.Add(self.stock_list, 1, wx.EXPAND)

        self.SetSizerAndFit(stocklist_sizer)

    def generate_stock_list(self):
        """"""

        stock_list = dv.DataViewCtrl(
            self,
            size=(1300, 640),
            style=wx.BORDER_THEME | dv.DV_ROW_LINES | dv.DV_VERT_RULES | dv.DV_MULTIPLE
        )
        self.stock_data = load_data_from(STOCKLIST_DATA_PATH)
        stock_list_model = DVIListModel(self.stock_data)
        stock_list.AssociateModel(stock_list_model)

        headers = [
            'Symbol', 'Shares', 'Cost Avg', 'Price', 'Cost Basis',
            'Market Value', 'Gain / Lost', 'Gain / Lost %', 'Yield %', 'Annual Dividend',
            'Dividend Received', 'Y2C %', 'Sector', 'Account %', 'Account'
        ]
        for idx, val in enumerate(headers):
            stock_list.AppendTextColumn(
                val,
                idx,
                width=wx.COL_WIDTH_AUTOSIZE,
                mode=dv.DATAVIEW_CELL_EDITABLE
            )

        for col in stock_list.Columns:
            col.Sortable = True
            col.Reorderable = True

        return stock_list_model, stock_list

    def stock_list_context_menu(self, event):
        context_menu = wx.Menu()
        item1 = wx.MenuItem(context_menu, wx.NewIdRef(), 'Add Row')
        item2 = wx.MenuItem(context_menu, wx.NewIdRef(), 'Delete Rows')
        item9 = wx.MenuItem(context_menu, wx.NewIdRef(), 'Save Stocks Data')
        context_menu.Append(item1)
        context_menu.Append(item2)
        context_menu.Append(item9)

        self.Bind(wx.EVT_MENU, self.add_row, id=item1.GetId())
        self.Bind(wx.EVT_MENU, self.delete_rows, id=item2.GetId())
        self.Bind(wx.EVT_MENU, self.save_stocks_data, id=item9.GetId())

        self.PopupMenu(context_menu)
        context_menu.Destroy()

    def add_row(self, event):
        col_count = self.stock_list.GetColumnCount()
        values = ['x' for i in range(col_count)]
        try:
            self.stock_list_model.add_row(values)
        except Exception as e:
            error_msg = f'Failed to add new row: {e}'
            logger.exception(error_msg)
            raise StockListWidgetException(error_msg)
        else:
            logger.info('Added new row successfully.')

    def delete_rows(self, event):
        selected = self.stock_list.GetSelections()
        rows = [self.stock_list_model.GetRow(item) for item in selected]
        try:
            self.stock_list_model.delete_rows(rows)
        except Exception as e:
            error_msg = f'Failed to delete rows: {e}'
            logger.exception(error_msg)
            raise StockListWidgetException(error_msg)
        else:
            logger.info('Deleted rows successully.')

    def save_stocks_data(self, event):
        try:
            dump_data(self.stock_data, STOCKLIST_DATA_PATH)
        except Exception as e:
            error_msg = f'data dump failed: {e}'
            logger.exception(error_msg)
            raise StockListWidgetException(error_msg)
        else:
            logger.info('Data dumped successfully.')
        self.main_window.dashboard.update_passive_income()
