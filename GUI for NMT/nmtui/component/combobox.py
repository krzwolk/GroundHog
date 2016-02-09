# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import Tkinter as tk
import ttk
from .textcomponent import TextComponent
from nmtui.noopfn import noopfn

class ComboBox(TextComponent):

    """Docstring for ComboBox. """

    def __init__(self, master, data, name, on_change=noopfn, default='',
                 title='Select Option', options=()):
        """TODO: to be defined1.

        :master: TODO
        :bind: TODO
        :title: TODO

        """
        TextComponent.__init__(self, master, data, name, on_change, default)

        self.label = tk.Label(self)
        self.label['text'] = title
        self.label.pack({'side': 'left'})

        self.combo = ttk.Combobox(self, values=options, textvariable=self.binding.get_var())
        self.combo.state(['readonly'])
        self.combo.pack({'side': 'right'}, fill=tk.X, expand=True)

        self.pack()
