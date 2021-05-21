import wx


class Dashboard():
    """"""

    def __init__(self, panel, name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = name
        self.panel = panel
