import wx
import wx.dataview as dv
from functions.funcs import load_data_from, dump_data
from settings import ASSETS_DEBTS_DATA_PATH, BUDGET_PLAN_DATA_PATH, ACCOUNTS_DATA_PATH
from settings import assets_debts_columns, budget_plan_columns, accounts_columns


def make_dvlc(parent, values, size):
    dvlc = dv.DataViewListCtrl(
        parent,
        size=size,
        style=dv.DV_MULTIPLE | dv.DV_ROW_LINES | dv.DV_ROW_LINES | dv.DV_VERT_RULES
    )
    for v in values:
        dvlc.AppendTextColumn(
            v,
            width=wx.COL_WIDTH_AUTOSIZE,
            mode=dv.DATAVIEW_CELL_EDITABLE,
            flags=dv.DATAVIEW_COL_SORTABLE | dv.DATAVIEW_COL_REORDERABLE | dv.DATAVIEW_COL_RESIZABLE
        )
    return dvlc


class Financials(wx.Panel):
    """"""

    def __init__(self, name, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.name = name

        ##### assets and debts #####
        self.dvlc = make_dvlc(self, assets_debts_columns, (500, 600))
        self.dvlc.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.dvlc_context_menu)
        self.dvlc.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.show_dvlc_status)

        for item in load_data_from(ASSETS_DEBTS_DATA_PATH):
            self.dvlc.AppendItem(item)

        self.dvlc_popup_id1 = wx.NewIdRef()  # add new row
        self.dvlc_popup_id2 = wx.NewIdRef()  # delete selected rows
        self.dvlc_popup_id9 = wx.NewIdRef()  # save data

        self.dvlc_status = wx.StaticText(self, -1, '     ')
        self.dvlc_status.SetForegroundColour('red')

        asset_debt_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Assets and Debts')
        asset_debt_sizer.Add(self.dvlc, 0)
        asset_debt_sizer.Add(self.dvlc_status, 0)

        ##### budget plan #####
        self.dvlc2 = make_dvlc(self, budget_plan_columns, (600, 600))
        self.dvlc2.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.dvlc2_context_menu)
        self.dvlc2.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.show_dvlc_status)

        for item in load_data_from(BUDGET_PLAN_DATA_PATH):
            self.dvlc2.AppendItem(item)

        self.dvlc2_popup_id1 = wx.NewIdRef()
        self.dvlc2_popup_id2 = wx.NewIdRef()
        self.dvlc2_popup_id9 = wx.NewIdRef()

        self.dvlc2_status = wx.StaticText(self, -1, '     ')
        self.dvlc2_status.SetForegroundColour('red')

        budget_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Budget Plan')
        budget_sizer.Add(self.dvlc2, 0)
        budget_sizer.Add(self.dvlc2_status, 0)

        ##### financial account #####

        self.dvlc3 = make_dvlc(self, accounts_columns, (340, 600))
        self.dvlc3.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.dvlc3_context_menu)
        self.dvlc3.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.show_dvlc_status)

        for item in load_data_from(ACCOUNTS_DATA_PATH):
            self.dvlc3.AppendItem(item)

        self.dvlc3_popup_id1 = wx.NewIdRef()
        self.dvlc3_popup_id2 = wx.NewIdRef()
        self.dvlc3_popup_id9 = wx.NewIdRef()

        self.dvlc3_status = wx.StaticText(self, -1, '    ')
        self.dvlc3_status.SetForegroundColour('red')

        accounts_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Financial Accounts')
        accounts_sizer.Add(self.dvlc3, 0)
        accounts_sizer.Add(self.dvlc3_status, 0)

        financials_sizer = wx.BoxSizer(wx.HORIZONTAL)
        financials_sizer.AddMany((asset_debt_sizer, budget_sizer, accounts_sizer))
        self.SetSizerAndFit(financials_sizer)
        self.SetMinSize((self.GetMinWidth(), self.GetMinHeight() + 30))

    def dvlc_context_menu(self, event):
        context_menu = wx.Menu()
        item1 = wx.MenuItem(context_menu, self.dvlc_popup_id1, 'Add New Row')
        item2 = wx.MenuItem(context_menu, self.dvlc_popup_id2, 'Delete Rows')
        item9 = wx.MenuItem(context_menu, self.dvlc_popup_id9, 'Save Assets and Debts Data')
        context_menu.Append(item1)
        context_menu.Append(item2)
        context_menu.Append(item9)

        self.Bind(wx.EVT_MENU, self.dvlc_add_row, id=self.dvlc_popup_id1)
        self.Bind(wx.EVT_MENU, self.dvlc_delete_rows, id=self.dvlc_popup_id2)
        self.Bind(wx.EVT_MENU, self.dvlc_save_data, id=self.dvlc_popup_id9)

        self.PopupMenu(context_menu)
        context_menu.Destroy()

    def dvlc2_context_menu(self, event):
        context_menu = wx.Menu()
        item1 = wx.MenuItem(context_menu, self.dvlc2_popup_id1, 'Add New Row')
        item2 = wx.MenuItem(context_menu, self.dvlc2_popup_id2, 'Delete Rows')
        item9 = wx.MenuItem(context_menu, self.dvlc2_popup_id9, 'Save Budget Plan Data')
        context_menu.Append(item1)
        context_menu.Append(item2)
        context_menu.Append(item9)

        self.Bind(wx.EVT_MENU, self.dvlc_add_row, id=self.dvlc2_popup_id1)
        self.Bind(wx.EVT_MENU, self.dvlc_delete_rows, id=self.dvlc2_popup_id2)
        self.Bind(wx.EVT_MENU, self.dvlc_save_data, id=self.dvlc2_popup_id9)

        self.PopupMenu(context_menu)
        context_menu.Destroy()

    def dvlc3_context_menu(self, event):
        context_menu = wx.Menu()
        item1 = wx.MenuItem(context_menu, self.dvlc3_popup_id1, 'Add New Row')
        item2 = wx.MenuItem(context_menu, self.dvlc3_popup_id2, 'Delete Rows')
        item9 = wx.MenuItem(context_menu, self.dvlc3_popup_id9, 'Save Accounts Data')
        context_menu.Append(item1)
        context_menu.Append(item2)
        context_menu.Append(item9)

        self.Bind(wx.EVT_MENU, self.dvlc_add_row, id=self.dvlc3_popup_id1)
        self.Bind(wx.EVT_MENU, self.dvlc_delete_rows, id=self.dvlc3_popup_id2)
        self.Bind(wx.EVT_MENU, self.dvlc_save_data, id=self.dvlc3_popup_id9)

        self.PopupMenu(context_menu)
        context_menu.Destroy()

    def dvlc_add_row(self, event):
        dvlc = self.dvlc
        status_text = self.dvlc_status
        if event.GetId() == self.dvlc2_popup_id1:
            dvlc = self.dvlc2
            status_text = self.dvlc2_status
        elif event.GetId() == self.dvlc3_popup_id1:
            dvlc = self.dvlc3
            status_text = self.dvlc3_status
        col_count = dvlc.GetColumnCount()
        dvlc.AppendItem(['0' for _ in range(col_count)])
        status_text.SetLabel('Data edited, please save.')

    def dvlc_delete_rows(self, event):
        dvlc = self.dvlc
        status_text = self.dvlc_status
        if event.GetId() == self.dvlc2_popup_id2:
            dvlc = self.dvlc2
            status_text = self.dvlc2_status
        elif event.GetId() == self.dvlc3_popup_id2:
            dvlc = self.dvlc3
            status_text = self.dvlc3_status
        for i in range(dvlc.GetItemCount() - 1, -1, -1):
            if dvlc.IsRowSelected(i):
                dvlc.DeleteItem(i)
        status_text.SetLabel('Data edited, please save.')

    def dvlc_save_data(self, event):
        path = ASSETS_DEBTS_DATA_PATH
        dvlc = self.dvlc
        status_text = self.dvlc_status
        if event.GetId() == self.dvlc2_popup_id9:
            path = BUDGET_PLAN_DATA_PATH
            dvlc = self.dvlc2
            status_text = self.dvlc2_status
        elif event.GetId() == self.dvlc3_popup_id9:
            path = ACCOUNTS_DATA_PATH
            dvlc = self.dvlc3
            status_text = self.dvlc3_status
        data = []
        col_count = dvlc.GetColumnCount()
        row_count = dvlc.GetItemCount()
        for i in range(row_count):
            data.append([dvlc.GetTextValue(i, j) for j in range(col_count)])
        dump_data(data, path)
        status_text.SetLabel('     ')

    def show_dvlc_status(self, event):
        status_text = self.dvlc_status
        if event.GetEventObject() == self.dvlc2:
            status_text = self.dvlc2_status
        elif event.GetEventObject() == self.dvlc3:
            status_text = self.dvlc3_status
        status_text.SetLabel('Data edited, please save.')
