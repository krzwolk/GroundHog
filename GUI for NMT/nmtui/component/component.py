# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import Tkinter as tk
from nmtui.noopfn import noopfn

class Component(tk.Frame):

    """Docstring for Component. """

    def __init__(self, master, data, name, on_change=noopfn, default=None):
        """TODO: to be defined1.

        :master: TODO
        :name: TODO
        :default: TODO

        """
        tk.Frame.__init__(self, master)

        self.master = master
        self.data = data
        self.name = name
        self.on_change = on_change
        self.default = default
        self.binding = None

    def reset(self):
        """TODO: Docstring for reset.
        :returns: TODO

        """
        self.set(self.default)
    
    def set(self, val):
        """TODO: Docstring for set.

        :val: TODO
        :returns: TODO

        """
        val = self._to_view(val)
        if val is not None:
            self.binding.get_var().set(val)

    def _to_val(self, val):
        """TODO: Docstring for _to_val.

        :val: TODO
        :returns: TODO

        """
        return val

    def _to_view(self, val):
        """TODO: Docstring for _to_view.

        :val: TODO
        :returns: TODO

        """
        return val
