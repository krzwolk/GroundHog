# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import Tkinter as tk


def create_btn(master, title, command, pack=None, fill=tk.X):
    """TODO: Docstring for create_btn.

    :master: TODO
    :title: TODO
    :command: TODO
    :pack: TODO
    :fill: TODO
    :returns: TODO

    """
    if pack is None:
        pack = {'side': 'top'}
    btn = tk.Button(master)
    btn['text'] = title
    btn['command'] = command
    btn.pack(pack, fill=fill)
    return btn
