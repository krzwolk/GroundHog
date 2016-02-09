# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import uuid
import logging
import Tkinter as tk
from blinker import signal
from cerberus import Validator
from .component import (
    Checkbox,
    ComboBox,
    CoresSelector,
    EntryBox,
    FileSelect,
    FolderSelect,
    NumberBox,
)
from .tktools import create_btn
from ghtools import conf as gh_conf

schema_str = {
    'type': 'string',
    'minlength': 1,
    'required': True
}
schema_int_pos = {
    'type': 'integer',
    'min': 1,
    'required': True
}
schema_bool = {
    'type': 'boolean',
    'required': True
}
schema = {
    'name': schema_str,
    'path': schema_str,
    'text1_path': schema_str,
    'lang1': schema_str,
    'text2_path': schema_str,
    'lang2': schema_str,
    'processor': schema_str,
    'cores': {
    'type': 'integer',
    'required': True
    },
    'method': schema_str,
    'bs': schema_int_pos,
    'loopIters': schema_int_pos,
    'timeStop': schema_int_pos,
    'dim': schema_int_pos,
    'null_sym_source': schema_int_pos,
    'null_sym_target': schema_int_pos,
    'compound_splitter': schema_bool,
    'true_casing': schema_bool,
    'lower_casing': schema_bool,
    'norm_punctuation': schema_bool,
    'clean_corpus': schema_bool,
    'clean_corpus_n': schema_int_pos,
}

class TrainMaster(tk.Frame):

    """Docstring for TrainMaster. """

    # pylint: disable=too-many-public-methods
    methods = [
        'RNNsearch-50',
        'RNNenc-30',
        'RNNenc-50',
    ]
    default_method = 'RNNsearch-50'
    log = logging.getLogger(__name__)

    def __init__(self, master):
        """TODO: to be defined1.

        :master: TODO

        """
        tk.Frame.__init__(self, master)

        self.data = {}

        self.name_entry = EntryBox(self, self.data, 'name', on_change=self.check, title='Name')
        self.name_entry.pack({'side': 'top'}, fill=tk.X)

        self.path_select = FolderSelect(self, self.data, 'path', on_change=self.check,
                                        title='Select Folder For Project')
        self.path_select.pack({'side': 'top'}, fill=tk.X)

        frame1 = tk.Frame(self)
        self.text1_file = FileSelect(frame1, self.data, 'text1_path',
                                     on_change=self.check,
                                     title='Select Text1 File')
        self.text1_file.pack({'side': 'left'})
        self.lang1_select = ComboBox(frame1, self.data, 'lang1', on_change=self.check,
                                     title='Language', options=gh_conf.tok_langs)
        self.lang1_select.pack({'side': 'right'})
        frame1.pack({'side': 'top'}, fill=tk.X)

        frame2 = tk.Frame(self)
        self.text2_file = FileSelect(frame2, self.data, 'text2_path',
                                     on_change=self.check,
                                     title='Select Text2 File')
        self.text2_file.pack({'side': 'left'})
        self.lang2_select = ComboBox(frame2, self.data, 'lang2', on_change=self.check,
                                     title='Language', options=gh_conf.tok_langs)
        self.lang2_select.pack({'side': 'right'})
        frame2.pack({'side': 'top'}, fill=tk.X)

        self.processor_select = ComboBox(self, self.data, 'processor',
                                         on_change=self.check,
                                         default='CPU', title='Run With',
                                         options=['CPU', 'GPU', 'GPU0', 'GPU1', 'GPU2', 'GPU3'])
        self.processor_select.pack({'side': 'top'}, fill=tk.X)

        self.cores_select = CoresSelector(self, self.data, 'cores', on_change=self.check)
        self.cores_select.pack({'side': 'top'}, fill=tk.X)

        self.method_select = ComboBox(self, self.data, 'method', on_change=self.check,
                                      default=self.default_method,
                                      title='Training Method', options=self.methods)
        self.method_select.pack({'side': 'top'}, fill=tk.X)
        self.bs_entry = NumberBox(self, self.data, 'bs', on_change=self.check,
                                        default=64, title='bs')
        self.bs_entry.pack({'side': 'top'}, fill=tk.X)
        self.loop_iters_entry = NumberBox(self, self.data, 'loopIters', on_change=self.check,
                                          default=3000000, title='loopIters')
        self.loop_iters_entry.pack({'side': 'top'}, fill=tk.X)
        self.time_stop_entry = NumberBox(self, self.data, 'timeStop', on_change=self.check,
                                         default=24*60*31, title='timeStop')
        self.time_stop_entry.pack({'side': 'top'}, fill=tk.X)
        self.dim_entry = NumberBox(self, self.data, 'dim', on_change=self.check,
                                   default=1000, title='dim')
        self.dim_entry.pack({'side': 'top'}, fill=tk.X)
        self.null_sym_source_entry = NumberBox(self, self.data, 'null_sym_source', on_change=self.check,
                                               default=30000, title='null_sym_source')
        self.null_sym_source_entry.pack({'side': 'top'}, fill=tk.X)
        self.null_sym_target_entry = NumberBox(self, self.data, 'null_sym_target', on_change=self.check,
                                               default=30000, title='null_sym_target')
        self.null_sym_target_entry.pack({'side': 'top'}, fill=tk.X)
        self.cs_flag = Checkbox(self, self.data, 'compound_splitter', on_change=self.check,
                                default=False, title='Compound Splitting')
        self.cs_flag.combo['state'] = tk.DISABLED
        self.cs_flag.pack({'side': 'top'}, fill=tk.X)
        self.tc_flag = Checkbox(self, self.data, 'true_casing', on_change=self.check,
                                default=False, title='True Casting')
        self.tc_flag.combo['state'] = tk.DISABLED
        self.tc_flag.pack({'side': 'top'}, fill=tk.X)
        self.lc_flag = Checkbox(self, self.data, 'lower_casing', on_change=self.check,
                                default=False, title='Lower Casing')
        self.lc_flag.pack({'side': 'top'}, fill=tk.X)
        self.np_flag = Checkbox(self, self.data, 'norm_punctuation', on_change=self.check,
                                default=False, title='Normalize Punctuation')
        self.np_flag.pack({'side': 'top'}, fill=tk.X)

        frame2 = tk.Frame(self)
        frame2.pack({'side': 'top'}, fill=tk.X)
        self.cc_flag = Checkbox(frame2, self.data, 'clean_corpus', on_change=self.check,
                                default=False, title='Clean Corpus')
        self.cc_flag.pack({'side': 'left'}, fill=tk.X)
        self.cc_n_entry = NumberBox(frame2, self.data, 'clean_corpus_n', on_change=self.check,
                                    default=7, title='')
        self.cc_n_entry.pack({'side': 'left'})

        self.btn_ok = create_btn(self, 'Create', self.add_trainer)
        self.btn_back = create_btn(self, 'Back', self.back)
        signal('trainmaster.show').connect(self.on_show)

    def on_show(self, sender):
        self.name_entry.reset()
        self.path_select.reset()
        self.text1_file.reset()
        self.lang1_select.reset()
        self.text2_file.reset()
        self.lang2_select.reset()
        self.processor_select.reset()
        self.cores_select.reset()
        self.method_select.reset()
        self.bs_entry.reset()
        self.loop_iters_entry.reset()
        self.time_stop_entry.reset()
        self.dim_entry.reset()
        self.null_sym_source_entry.reset()
        self.null_sym_target_entry.reset()
        self.cs_flag.reset()
        self.tc_flag.reset()
        self.lc_flag.reset()
        self.np_flag.reset()
        self.cc_flag.reset()
        self.cc_n_entry.reset()
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

    def back(self):
        """TODO: Docstring for back.
        :returns: TODO

        """
        self.pack_forget()
        signal('trainmaster.back').send()

    def add_trainer(self):
        """TODO: Docstring for add_trainer.
        :returns: TODO

        """
        data = {}
        data.update(self.data)
        data['id'] = uuid.uuid4().hex
        self.log.debug(data)
        self.pack_forget()
        signal('trainmaster.new_trainer').send(data=data)
