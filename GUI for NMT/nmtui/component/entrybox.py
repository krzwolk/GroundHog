# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import Tkinter as tk
from .textcomponent import TextComponent
from nmtui.noopfn import noopfn

class EntryBox(TextComponent):

    """Docstring for EntryBox. """

    def __init__(self, master, data, name, on_change=noopfn, default='', title='Entry'):
        """TODO: to be defined1.

        :master: TODO
        :title: TODO

        """
        TextComponent.__init__(self, master, data, name, on_change, default)

        self.label = tk.Label(self)
        self.label['text'] = title
        self.label.pack({'side': 'left'})

        self.entry = tk.Entry(self, textvariable=self.binding.get_var())
        self.entry.pack({'side': 'right'}, fill=tk.X, expand=True)

        self.pack()
