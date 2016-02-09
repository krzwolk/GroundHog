# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import Tkinter as tk
from nmtui.noopfn import noopfn

class Binding(object):

    """Docstring for Binding. """

    def __init__(self, data, key, tk_var, to_val=None, to_view=None, run_on_change=noopfn):
        """TODO: to be defined1.

        :data: dictionary for binding
        :key: key in dictionary for tk_var binding
        :tk_var: Tk traceable variable
        :to_val: convert variable value to app value

        """
        self.data = data
        self.key = key
        self.tk_var = tk_var
        self.to_val = to_val
        self.to_view = to_view
        self.run_on_change = run_on_change

        if isinstance(tk_var, (tk.StringVar, tk.IntVar)):
            tk_var.trace('w', self._on_change)
        else:
            raise ValueError('Untraceable variable')

    def set_on_change(self, fn):
        """TODO: Docstring for set_on_change.

        :fn: TODO
        :returns: TODO

        """
        self.run_on_change = fn

    def _on_change(self, *args):
        """TODO: Docstring for _on_change.

        :*args: TODO
        :returns: TODO

        """
        if self.to_val:
            val = self.to_val(self.tk_var.get())
        else:
            val = self.tk_var.get()
        if val is not None:
            self.data[self.key] = val
            self.run_on_change(val)
        else:
            if self.to_view:
                self.tk_var.set(self.to_view(self.data[self.key]))
            else:
                self.tk_var.set(self.data[self.key])

    def get_var(self):
        """TODO: Docstring for get_var.
        :returns: TODO

        """
        return self.tk_var
