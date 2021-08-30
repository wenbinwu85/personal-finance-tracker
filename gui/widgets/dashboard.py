from math import pi
import wx
import wx.dataview as dv
import wx.lib.gizmos as gizmos
from wx.lib.agw.piectrl import PieCtrl, PiePart
from wx.lib.agw.pycollapsiblepane import PyCollapsiblePane
from functions.funcs import load_data_from, dump_data
from gui.widgets.creditscoresupdatedialog import CreditScoresUpdateDialog
from settings import METRICS_DATA_PATH, CREDIT_SCORES_DATA_PATH, ASSETS_DEBTS_DATA_PATH, STOCKLIST_DATA_PATH
from settings import net_worth_labels, passive_income_labels, metrics_columns


def make_led_num_ctrl(parent, label, value, color, size=(200, 50)):
    label = wx.StaticText(parent, label=label)
    led = gizmos.LEDNumberCtrl(
        parent, wx.ID_ANY, (25, 25), size=size, style=gizmos.LED_ALIGN_RIGHT
    )
    led.SetValue(value)
    led.SetForegroundColour(color)
    led.SetDrawFaded(True)
    return label, led


class Dashboard(wx.Panel):
    """"""

    def __init__(self, name, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.name = name

        ##### net worth LEDs #####
        net_worth_led_colors = ['firebrick', 'forest green', 'lime green', 'forest green']
        self.net_worth_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Personal Summary')
        for idx, text in enumerate(net_worth_labels):
            label, led = make_led_num_ctrl(self, text, '', net_worth_led_colors[idx])
            self.net_worth_sizer.Add(label)
            self.net_worth_sizer.Add(led, 0, wx.BOTTOM, 10)

        ##### passive income LEDs #####
        self.dividend_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Passive Income')
        for text in passive_income_labels:
            label, led = make_led_num_ctrl(self, text, '', 'forest green', size=(175, 50))
            self.dividend_sizer.Add(label)
            self.dividend_sizer.Add(led, 0, wx.BOTTOM, 10)

        ##### credit scores LEDs #####
        self.credit_score_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Credit Scores')
        for (text, value) in load_data_from(CREDIT_SCORES_DATA_PATH):
            label, led = make_led_num_ctrl(self, text, value, 'sky blue', (100, 50))
            led.Bind(wx.EVT_CONTEXT_MENU, self.credit_scores_context_menu)
            self.credit_score_sizer.Add(label)
            self.credit_score_sizer.Add(led, 0, wx.BOTTOM, 10)

        ##### pie chart #####
        self.pie = PieCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(320, 260))
        self.pie.SetHeight(25)
        self.pie.SetBackColour('dark grey')
        self.pie.SetShowEdges(False)
        legend = self.pie.GetLegend()
        legend.SetLabelColour('white')
        legend.SetTransparent(True)
        self.pie_part1 = PiePart(100, wx.Colour(200, 50, 50), 'TSP')
        self.pie_part2 = PiePart(250, wx.Colour(50, 200, 50), 'Schwab')
        self.pie_part3 = PiePart(450, wx.Colour(50, 50, 200), 'Roth IRA')
        self.pie_part4 = PiePart(150, wx.Colour(200, 200, 50), 'Webull')
        self.pie_part5 = PiePart(150, wx.Colour(200, 50, 200), 'Coinbase')
        self.pie._series.append(self.pie_part1)
        self.pie._series.append(self.pie_part2)
        self.pie._series.append(self.pie_part3)
        self.pie._series.append(self.pie_part4)
        self.pie._series.append(self.pie_part5)

        self.hslider = wx.Slider(
            self, wx.ID_ANY, 180, 0, 360, size=(260, -1), style=wx.SL_LABELS | wx.SL_TOP
        )
        self.hslider.Bind(wx.EVT_SLIDER, self.hslider_handler)
        self.vslider = wx.Slider(
            self, wx.ID_ANY, 40, 20, 60, size=wx.DefaultSize, style=wx.SL_VERTICAL | wx.SL_LABELS
        )
        self.vslider.Bind(wx.EVT_SLIDER, self.vslider_handler)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.pie, 0, wx.EXPAND)
        hsizer.Add(self.vslider, 1, wx.EXPAND | wx.GROW)
        pie_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Investment Distribution')
        pie_sizer.Add(hsizer)
        pie_sizer.Add(self.hslider, 1, wx.EXPAND | wx.GROW)

        led_pie_sizer = wx.BoxSizer(wx.HORIZONTAL)
        led_pie_sizer.Add(self.net_worth_sizer, 0, wx.BOTTOM)
        led_pie_sizer.Add(self.dividend_sizer, 0, wx.BOTTOM)
        led_pie_sizer.Add(self.credit_score_sizer, 0, wx.BOTTOM)
        led_pie_sizer.Add(pie_sizer, 0, wx.BOTTOM | wx.EXPAND)

        ##### Monthly Metrics dataview #####
        self.cpane = PyCollapsiblePane(self, label='Monthly Metrics', style=wx.CP_DEFAULT_STYLE)
        self.cpane.SetAutoLayout(True)
        self.cpane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapse_pane_change)

        self.metrics_dvlc = dv.DataViewListCtrl(
            self.cpane.GetPane(), size=(920, 280), style=dv.DV_ROW_LINES | dv.DV_VERT_RULES
        )
        self.metrics_dvlc.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.metrics_context_menu)
        self.metrics_dvlc.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.update_pie_chart)

        for i in metrics_columns[:8]:
            self.metrics_dvlc.AppendTextColumn(
                i, width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE
            )
        for i in metrics_columns[8:]:
            self.metrics_dvlc.AppendTextColumn(i, width=wx.COL_WIDTH_AUTOSIZE)
        for item in load_data_from(METRICS_DATA_PATH):
            self.metrics_dvlc.AppendItem(item)

        self.dashboard_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dashboard_sizer.Add(led_pie_sizer, 0, wx.EXPAND)
        self.dashboard_sizer.Add(self.cpane, 0, wx.EXPAND)

        self.SetSizerAndFit(self.dashboard_sizer)
        self.dashboard_sizer.Layout()
        self.SetMinSize((self.GetMinWidth(), self.GetMinHeight() + 30))

        self.hslider_handler(wx.EVT_SLIDER)
        self.vslider_handler(wx.EVT_SLIDER)

        self.update_metrics_net_worth()
        self.update_passive_income()
        self.update_pie_chart(dv.EVT_DATAVIEW_SELECTION_CHANGED)

    def vslider_handler(self, event):
        self.pie.SetAngle(float(self.vslider.GetValue()) / 180.0 * pi)

    def hslider_handler(self, event):
        self.pie.SetRotationAngle(float(self.hslider.GetValue()) / 180.0 * pi)

    def collapse_pane_change(self, event):
        self.SetSizerAndFit(self.dashboard_sizer)
        self.dashboard_sizer.Layout()

        if self.cpane.IsExpanded():
            size = self.GetSize()
        else:
            size = (self.GetMinWidth(), self.GetMinHeight() + 30)
            self.SetMinSize(size)

        frame = self.GetTopLevelParent()
        frame.SetClientSize(size)
        frame.SendSizeEvent()
        frame.CenterOnScreen()

    def update_metrics_net_worth(self):
        debts = 0
        cash = 0
        assets = 0
        for item in load_data_from(ASSETS_DEBTS_DATA_PATH):
            if item[2] == 'Debt':
                debts += float(item[1])
            elif item[2] == 'Cash':
                cash += float(item[1])
            elif item[2] == 'Assets':
                assets += float(item[1])

        last_col = self.metrics_dvlc.GetColumnCount() - 1
        last_row = self.metrics_dvlc.GetItemCount() - 1

        tsp = self.metrics_dvlc.GetTextValue(last_row, 1)
        stonks = self.metrics_dvlc.GetTextValue(last_row, 2)
        roth = self.metrics_dvlc.GetTextValue(last_row, 3)
        webull = self.metrics_dvlc.GetTextValue(last_row, 4)
        coinbase = self.metrics_dvlc.GetTextValue(last_row, 5)
        dividend = self.metrics_dvlc.GetTextValue(last_row, 6)

        investments = float(tsp) + float(stonks) + float(roth) + float(webull) + float(coinbase) + float(dividend)
        total_assets = assets + investments + cash
        net_worth = total_assets + debts  # debts is negative
        debt_asset_ratio = round(abs(debts / total_assets), 4)

        self.metrics_dvlc.SetTextValue(str(net_worth), last_row, last_col)
        self.metrics_dvlc.SetTextValue(str(assets), last_row, last_col - 1)
        self.metrics_dvlc.SetTextValue(str(debts), last_row, last_col - 2)
        self.metrics_dvlc.SetTextValue(str(cash), last_row, last_col - 3)

        children = self.net_worth_sizer.GetChildren()
        children[1].GetWindow().SetValue(str(debts))
        children[3].GetWindow().SetValue(str(total_assets))
        children[5].GetWindow().SetValue(str(net_worth))
        children[7].GetWindow().SetValue(str(debt_asset_ratio))

    def update_passive_income(self):
        annual_dividend = 0
        total_dividend = 0
        market_value = 0
        for stock in load_data_from(STOCKLIST_DATA_PATH):
            market_value += float(stock[5])
            annual_dividend += float(stock[9])
            total_dividend += float(stock[10])

        data = {
            1: str(round(annual_dividend / market_value * 100, 4)),
            3: str(round(annual_dividend, 2)),
            5: str(round(annual_dividend / 12, 2)),
            7: str(round(total_dividend, 2))
        }
        children = self.dividend_sizer.GetChildren()
        for key, val in data.items():
            ctrl = children[key].GetWindow()
            ctrl.SetValue(val)

    def update_pie_chart(self, event):
        row = self.metrics_dvlc.GetSelectedRow()
        if row is wx.NOT_FOUND:
            row = self.metrics_dvlc.GetItemCount() - 1

        data_store = self.metrics_dvlc.GetStore()
        col_count = self.metrics_dvlc.GetColumnCount()
        row_data = [data_store.GetValueByRow(row, col) for col in range(col_count)]

        self.pie_part1.SetValue(float(row_data[1]))
        self.pie_part2.SetValue(float(row_data[2]))
        self.pie_part3.SetValue(float(row_data[3]))
        self.pie_part4.SetValue(float(row_data[4]))
        self.pie_part5.SetValue(float(row_data[5]))
        self.pie.Refresh()

    def credit_scores_context_menu(self, event):
        self.context_menu_id1 = wx.NewIdRef()
        context_menu = wx.Menu()
        item1 = wx.MenuItem(context_menu, self.context_menu_id1, 'Update Credit Scores')
        context_menu.Append(item1)

        self.Bind(wx.EVT_MENU, self.credit_scores_update_dialog, id=self.context_menu_id1)

        self.PopupMenu(context_menu)
        context_menu.Destroy()

    def credit_scores_update_dialog(self, event):
        dialog = CreditScoresUpdateDialog(self, title='Update Credit Scores')
        children = self.credit_score_sizer.GetChildren()

        dialog.equifax_field.SetValue(children[1].GetWindow().GetValue())
        dialog.transunion_field.SetValue(children[3].GetWindow().GetValue())
        dialog.experian_field.SetValue(children[5].GetWindow().GetValue())
        dialog.avg_field.SetValue(children[7].GetWindow().GetValue())

        if dialog.ShowModal() == wx.ID_OK:
            data = {
                1: dialog.equifax_field.GetValue(),
                3: dialog.transunion_field.GetValue(),
                5: dialog.experian_field.GetValue(),
                7: dialog.avg_field.GetValue()
            }
            for key, val in data.items():
                ctrl = children[key].GetWindow()
                ctrl.SetValue(val)

            new_data = [
                ['Equifax', data[1]],
                ['Transunion', data[3]],
                ['Experian', data[5]],
                ['Average', data[7]]
            ]
            dump_data(new_data, CREDIT_SCORES_DATA_PATH)
        return None

    def metrics_context_menu(self, event):
        context_menu = wx.Menu()
        item1 = wx.MenuItem(context_menu, wx.NewIdRef(), 'Add new row')
        item2 = wx.MenuItem(context_menu, wx.NewIdRef(), 'Delete last row')
        item9 = wx.MenuItem(context_menu, wx.NewIdRef(), 'Save Metrics Data')
        context_menu.Append(item1)
        context_menu.Append(item2)
        context_menu.Append(item9)

        self.Bind(wx.EVT_MENU, self.metrics_add_row, id=item1.GetId())
        self.Bind(wx.EVT_MENU, self.metrics_delete_last_row, id=item2.GetId())
        self.Bind(wx.EVT_MENU, self.metrics_save_data, id=item9.GetId())

        self.PopupMenu(context_menu)
        context_menu.Destroy()

    def metrics_add_row(self, event):
        col_count = self.metrics_dvlc.GetColumnCount()
        self.metrics_dvlc.AppendItem(['123' for _ in range(col_count)])
        self.update_metrics_net_worth()

    def metrics_delete_last_row(self, event):
        self.metrics_dvlc.DeleteItem(self.metrics_dvlc.GetItemCount() - 1)

    def metrics_save_data(self, event):
        data = []
        col_count = self.metrics_dvlc.GetColumnCount()
        for row in range(self.metrics_dvlc.GetItemCount()):
            data.append([self.metrics_dvlc.GetTextValue(row, col) for col in range(col_count)])
        dump_data(data, METRICS_DATA_PATH)
        self.update_pie_chart(dv.EVT_DATAVIEW_SELECTION_CHANGED)
