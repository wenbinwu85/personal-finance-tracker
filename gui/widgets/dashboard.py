from math import pi
import wx
import wx.dataview as dv
import wx.lib.gizmos as gizmos
from wx.lib.agw.piectrl import PieCtrl, PiePart
from wx.lib.agw.pycollapsiblepane import PyCollapsiblePane
from functions.funcs import load_data_from, dump_data
from gui.widgets.creditscoresupdatedialog import CreditScoresUpdateDialog
from settings import METRICS_DATA_PATH, PERSONAL_SUMMARY_DATA_PATH
from settings import PASSIVE_INCOME_DATA_PATH, CREDIT_SCORES_DATA_PATH, STOCKLIST_DATA_PATH


def make_led_num_ctrl(parent, label, value, color, size=(200, 50)):
    label = wx.StaticText(parent, label=label)
    led = gizmos.LEDNumberCtrl(
        parent,
        wx.ID_ANY,
        (25, 25),
        size=size,
        style=gizmos.LED_ALIGN_RIGHT
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

        ##### personal net worth #####
        net_worth_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Personal Summary')
        for (text, value, color) in load_data_from(PERSONAL_SUMMARY_DATA_PATH):
            label, led = make_led_num_ctrl(self, text, value, color)
            net_worth_sizer.Add(label)
            net_worth_sizer.Add(led, 0, wx.BOTTOM, 10)

        ##### passive income #####
        self.dividend_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Passive Income')
        for (text, value) in load_data_from(PASSIVE_INCOME_DATA_PATH):
            label, led = make_led_num_ctrl(self, text, value, 'forest green', size=(175, 50))
            self.dividend_sizer.Add(label)
            self.dividend_sizer.Add(led, 0, wx.BOTTOM, 10)
        self.update_passive_income()

        ##### credit scores #####
        self.credit_score_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Credit Scores')
        for (text, value) in load_data_from(CREDIT_SCORES_DATA_PATH):
            label, led = make_led_num_ctrl(self, text, value, 'sky blue', (100, 50))
            self.credit_score_sizer.Add(label)
            self.credit_score_sizer.Add(led, 0, wx.BOTTOM, 10)
        for child in self.credit_score_sizer.GetChildren():
            ctrl = child.GetWindow()
            ctrl.Bind(wx.EVT_CONTEXT_MENU, self.credit_scores_context_menu)

        self.pie = PieCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(260, 260))
        self.pie.SetHeight(25)
        self.pie.SetBackColour('dark grey')
        self.pie.SetShowEdges(False)
        pie_legend = self.pie.GetLegend()
        pie_legend.SetTransparent(True)
        pie_legend.SetLabelColour(wx.Colour(225, 225, 225))
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

        pie_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label='Wealth Distribution')
        pie_sizer.Add(hsizer)
        pie_sizer.Add(self.hslider, 1)

        summary_sizer = wx.BoxSizer(wx.HORIZONTAL)
        summary_sizer.Add(net_worth_sizer, 0, wx.BOTTOM)
        summary_sizer.Add(self.dividend_sizer, 0, wx.BOTTOM)
        summary_sizer.Add(self.credit_score_sizer, 0, wx.BOTTOM)
        summary_sizer.Add(pie_sizer, 0, wx.BOTTOM | wx.EXPAND)

        ##### Monthly Metrics #####
        self.cpane = PyCollapsiblePane(self, label='Monthly Metrics', style=wx.CP_DEFAULT_STYLE)
        self.cpane.SetAutoLayout(True)
        # self.cpane.Expand()
        self.cpane.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapse_pane_change)
        metrics_columns = [
            'Month', 'TSP', 'Schwab', 'Roth IRA', 'Webull',
            'Coinbase', 'Dividend', 'Invested', 'Cash', 'Debts', 'Net Worth'
        ]
        self.metrics_dvlc = dv.DataViewListCtrl(self.cpane.GetPane(), size=(860, 280), style=dv.DV_ROW_LINES)
        self.metrics_dvlc.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.metrics_context_menu)
        self.metrics_dvlc.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.update_pie_chart)
        for i in metrics_columns:
            self.metrics_dvlc.AppendTextColumn(i, width=wx.COL_WIDTH_AUTOSIZE, mode=dv.DATAVIEW_CELL_EDITABLE)
        for item in load_data_from(METRICS_DATA_PATH):
            self.metrics_dvlc.AppendItem(item)

        self.dashboard_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dashboard_sizer.Add(summary_sizer, 0, wx.EXPAND)
        self.dashboard_sizer.Add(self.cpane, 0, wx.EXPAND)

        self.SetSizerAndFit(self.dashboard_sizer)
        self.dashboard_sizer.Layout()
        self.SetMinSize((self.GetMinWidth(), self.GetMinHeight()+30))

        self.hslider_handler(wx.EVT_SLIDER)
        self.vslider_handler(wx.EVT_SLIDER)
        store = self.metrics_dvlc.GetStore()
        last_row = store.GetItemCount()-1
        last_row_data = [store.GetValueByRow(last_row, col) for col in range(store.GetColumnCount())]
        self.pie_part1.SetValue(float(last_row_data[1]))
        self.pie_part2.SetValue(float(last_row_data[2]))
        self.pie_part3.SetValue(float(last_row_data[3]))
        self.pie_part4.SetValue(float(last_row_data[4]))
        self.pie_part5.SetValue(float(last_row_data[5]))
        self.pie.Refresh()


    def vslider_handler(self, event):
        self.pie.SetAngle(float(self.vslider.GetValue()) / 180.0 * pi)

    def hslider_handler(self, event):
        self.pie.SetRotationAngle(float(self.hslider.GetValue()) / 180.0 * pi)

    def collapse_pane_change(self, event):
        if self.cpane.IsExpanded():
            self.SetSizerAndFit(self.dashboard_sizer)
            self.dashboard_sizer.Layout()
            frame = self.GetTopLevelParent()
            frame.SetClientSize(self.GetSize())
            frame.SendSizeEvent()
            frame.CenterOnScreen()
        else:
            self.SetSizerAndFit(self.dashboard_sizer)
            self.dashboard_sizer.Layout()
            self.SetMinSize((self.GetMinWidth(), self.GetMinHeight()+30))
            frame = self.GetTopLevelParent()
            frame.SetClientSize(self.GetMinSize())
            frame.SendSizeEvent()
            frame.CenterOnScreen()

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

    def update_passive_income(self):
        annual_dividend = 0
        total_dividend = 0
        market_value = 0
        for stock in load_data_from(STOCKLIST_DATA_PATH):
            market_value += float(stock[5])
            annual_dividend += float(stock[9])
            total_dividend += float(stock[10])
        children = self.dividend_sizer.GetChildren()
        children[1].GetWindow().SetValue(str(round(annual_dividend / market_value * 100, 4)))
        children[3].GetWindow().SetValue(str(round(annual_dividend, 2)))
        children[5].GetWindow().SetValue(str(round(annual_dividend / 12, 2)))
        children[7].GetWindow().SetValue(str(round(total_dividend, 2)))

    def metrics_context_menu(self, event):
        context_menu = wx.Menu()
        item9 = wx.MenuItem(context_menu, wx.NewIdRef(), 'Save Assets and Debts Data')
        context_menu.Append(item9)

        self.Bind(wx.EVT_MENU, self.save_metrics_data, id=item9.GetId())

        self.PopupMenu(context_menu)
        context_menu.Destroy()

    def save_metrics_data(self, event):
        data = []
        col_count = self.metrics_dvlc.GetColumnCount()
        row_count = self.metrics_dvlc.GetItemCount()
        for i in range(row_count):
            data.append([self.metrics_dvlc.GetTextValue(i, j) for j in range(col_count)])
        dump_data(data, METRICS_DATA_PATH)

    def update_pie_chart(self, event):
        row = self.metrics_dvlc.GetSelectedRow()
        store = self.metrics_dvlc.GetStore()
        row_data = [store.GetValueByRow(row, col) for col in range(store.GetColumnCount())]

        self.pie_part1.SetValue(float(row_data[1]))
        self.pie_part2.SetValue(float(row_data[2]))
        self.pie_part3.SetValue(float(row_data[3]))
        self.pie_part4.SetValue(float(row_data[4]))
        self.pie_part5.SetValue(float(row_data[5]))
        self.pie.Refresh()
