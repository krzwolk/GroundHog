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

class TextComponent(Component):

    """Docstring for TextComponent. """

    # pylint: disable=too-many-ancestors

    def __init__(self, master, data, name, on_change=noopfn, default=''):
        """TODO: to be defined1.

        :master: TODO
        :name: TODO
        :default: TODO

        """
        Component.__init__(self, master, data, name, on_change, default)

        self.binding = Binding(self.data, self.name, tk.StringVar(),
                               to_val=self._to_val, to_view=self._to_view,
                               run_on_change=on_change)
