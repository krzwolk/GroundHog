# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import math
from .entrybox import EntryBox
from nmtui.noopfn import noopfn

class NumberBox(EntryBox):

    """Docstring for NumberBox. """

    def __init__(self, master, data, name, on_change=noopfn, default=0, title='Number'):
        """TODO: to be defined1.

        :master: TODO
        :data: TODO
        :name: TODO
        :on_change: TODO
        :default: TODO
        :title: TODO

        """
        EntryBox.__init__(self, master, data, name, on_change, default, title)

    def _to_val(self, val):
        """TODO: Docstring for _to_val.

        :val: TODO
        :returns: TODO

        """
        try:
            if val == '':
                return float('nan')
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
            if math.isnan(val):
                return ''
            else:
                return str(val)
        except:
            return None
