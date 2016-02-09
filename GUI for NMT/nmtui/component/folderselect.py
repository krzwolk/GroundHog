# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import Tkinter as tk
import tkFileDialog
from .textcomponent import TextComponent
from nmtui.noopfn import noopfn

class FolderSelect(TextComponent):

    """Docstring for FolderSelect. """

    def __init__(self, master, data, name, on_change=noopfn, default='', title='Select Folder'):
        """TODO: to be defined1.

        :master: TODO
        :title: TODO

        """
        TextComponent.__init__(self, master, data, name, on_change, default)

        self.title = title
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
        path = tkFileDialog.askdirectory(title=self.title)
        if path:
            self.set(path)
