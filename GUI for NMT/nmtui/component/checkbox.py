# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import Tkinter as tk
from .component import Component
from nmtui.binding import Binding
from nmtui.noopfn import noopfn

class Checkbox(Component):

    """Docstring for Checkbox. """

    def __init__(self, master, data, name, on_change=noopfn, default=False, title='Enable'):
        """TODO: to be defined1.

        :master: TODO
        :data: TODO
        :name: TODO
        :on_change: TODO
        :default: TODO

        """
        Component.__init__(self, master, data, name, on_change, default)

        self.binding = Binding(self.data, self.name, tk.IntVar(),
                               to_val=self._to_val, to_view=self._to_view,
                               run_on_change=on_change)

        self.combo = tk.Checkbutton(self, text=title, variable=self.binding.get_var())
        self.combo.pack({'side': 'left'})

        self.pack()

    def _to_val(self, val):
        """TODO: Docstring for _to_val.

        :val: TODO
        :returns: TODO

        """
        return bool(val)

    def _to_view(self, val):
        """TODO: Docstring for _to_view.

        :val: TODO
        :returns: TODO

        """
        if val:
            return 1
        else:
            return 0
