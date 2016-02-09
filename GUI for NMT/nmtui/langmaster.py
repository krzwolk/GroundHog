# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import Tkinter as tk
from blinker import signal
from .component.fileselect import FileSelect
from .binding import Binding
from cerberus import Validator

schema_fn = {
    'type': 'string',
    'minlength': 1,
    'required': True
}
schema = {
    'name': {
        'type': 'string',
        'minlength': 1,
        'required': True
    },
    'target': schema_fn,
    'source': schema_fn,
    'indx_word': schema_fn,
    'indx_word_target': schema_fn,
    'word_indx': schema_fn,
    'word_indx_trgt': schema_fn,
}

class LangMaster(tk.Frame):

    """Docstring for LangMaster. """

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-public-methods

    def __init__(self, master):
        """TODO: to be defined1.

        :master: TODO

        """
        def entry_binding(name):
            entry_var = tk.StringVar()
            self.vars.append(entry_var)
            return Binding(self.data, name, entry_var, run_on_change=self.check)

        def create_file_select(bind, title):
            fs = FileSelect(self, bind, title=title)
            fs.pack({'side': 'top'}, fill=tk.X)
            return fs

        tk.Frame.__init__(self, master)

        self.vars = []
        self.data = {}

        self.name_b = entry_binding('name')
        self.target_b = entry_binding('target')
        self.source_b = entry_binding('source')
        self.indx_word_b = entry_binding('indx_word')
        self.indx_word_target_b = entry_binding('indx_word_target')
        self.word_indx_b = entry_binding('word_indx')
        self.word_indx_trgt_b = entry_binding('word_indx_trgt')

        entry_frame = tk.Frame(self)
        entry_frame.pack({'side': 'top'}, fill=tk.X)
        entry_label = tk.Label(entry_frame, text='Language ID')
        entry_label.pack({'side': 'left'})
        self.entry_name = tk.Entry(entry_frame, textvariable=self.name_b.get_var())
        self.entry_name.pack({'side': 'right'})

        self.target_file = create_file_select(self.target_b, 'Select "target" File')
        self.source_file = create_file_select(self.source_b, 'Select "source" File')
        self.indx_word_file = create_file_select(self.indx_word_b, 'Select "indx_word" File')
        self.indx_word_target_file = create_file_select(self.indx_word_target_b, 'Select "indx_word_target" File')
        self.word_indx_file = create_file_select(self.word_indx_b, 'Select "word_indx" File')
        self.word_indx_trgt_file = create_file_select(self.word_indx_trgt_b, 'Select "word_indx_trgt" File')

        action_frame = tk.Frame(self)
        action_frame.pack({'side': 'top'})
        self.btn_ok = tk.Button(action_frame, state=tk.DISABLED)
        self.btn_ok['text'] = 'Add Language'
        self.btn_ok['command'] = self.add_language
        self.btn_ok.pack({'side': 'left'})
        self.btn_cancel = tk.Button(action_frame)
        self.btn_cancel['text'] = 'Cancel'
        self.btn_cancel['command'] = self.cancel
        self.btn_cancel.pack({'side': 'right'})

        signal('langmaster.show').connect(self.on_show)

    def on_show(self, sender):
        [v.set('') for v in self.vars]
        self.pack()

    def check(self, val):
        """TODO: Docstring for check.
        :returns: TODO

        """
        v = Validator(schema)
        if v.validate(self.data):
            self.btn_ok.config(state=tk.NORMAL)
        else:
            self.btn_ok.config(state=tk.DISABLED)

    def add_language(self):
        """TODO: Docstring for add_language.
        :returns: TODO

        """
        self.pack_forget()
        signal('langmaster.new_lang').send(data=self.data)

    def cancel(self):
        """TODO: Docstring for cancel.
        :returns: TODO

        """
        self.pack_forget()
        signal('langmaster.cancel').send()
