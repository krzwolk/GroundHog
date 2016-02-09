# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import tkFileDialog
import Tkinter as tk
from .textcomponent import TextComponent
from nmtui.noopfn import noopfn

class FileSelect(TextComponent):

    """Docstring for FileSelect. """

    def __init__(self, master, data, name, on_change=noopfn, default='', title='Select File', save=False):
        """TODO: to be defined1.

        :master: TODO
        :title: TODO

        """
        TextComponent.__init__(self, master, data, name, on_change, default)

        self.title = title
        self.save = save
        self.path_entry = tk.Entry(self, textvariable=self.binding.get_var())
        self.path_entry['state'] = tk.DISABLED
        self.path_entry.pack({'side': 'left'}, fill=tk.X, expand=True)

        self.btn_sel = tk.Button(self)
        self.btn_sel['text'] = title
        self.btn_sel['command'] = self.on_select
        self.btn_sel.pack({'side': 'right'})

    def on_select(self, *args):
        """TODO: Docstring for on_select.

        :*args: TODO
        :returns: TODO

        """
        if self.save:
            path = tkFileDialog.SaveAs(title=self.title).show()
        else:
            path = tkFileDialog.Open(title=self.title).show()
        if path:
            self.set(path)
