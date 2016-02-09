# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import Tkinter as tk
import ttk
from multiprocessing import cpu_count
from .textcomponent import TextComponent
from .combobox import ComboBox
from nmtui.noopfn import noopfn

def get_cores_options():
    """TODO: Docstring for get_cores_options.
    :returns: TODO

    """
    cores = []
    for n in range(cpu_count()):
        cores.append(str(n+1))
    return cores

class CoresSelector(ComboBox):

    """Docstring for CoresSelector. """

    def __init__(self, master, data, name, on_change=noopfn, default=0,
                 title='Number Of Cores'):
        """TODO: to be defined1.

        :master: TODO
        :bind: TODO
        :title: TODO

        """
        options = ['all'] + get_cores_options()
        ComboBox.__init__(self, master, data, name, on_change, default, title, options)
        self.pack()

    def _to_val(self, val):
        """TODO: Docstring for _to_val.

        :val: TODO
        :returns: TODO

        """
        try:
            if val == 'all':
                return 0
            else:
                return int(val)
        except:
            return None

    def _to_view(self, val):
        """TODO: Docstring for _to_view.

        :val: TODO
        :returns: TODO

        """
        try:
            if val == 0:
                return 'all'
            else:
                return str(val)
        except:
            return None
