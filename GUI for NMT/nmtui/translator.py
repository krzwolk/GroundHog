# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import os
import Tkinter as tk
from threading import Thread
from glob import glob
from blinker import signal
from .tktools import create_btn
from rsklab.globlog import glog
from ghtools.translate import start_trans
from .component import (
    FileSelect,
    ComboBox
)

class Translator(tk.Frame):

    """Docstring for Translator. """

    def __init__(self, master):
        """TODO: to be defined1.

        :master: TODO

        """
        tk.Frame.__init__(self, master)

        self.data = {}
        self.trainers = {}

        self.model_select = ComboBox(self, self.data, 'model', on_change=self.check,
                              title='Model', options=[])
        self.input_file = FileSelect(self, self.data, 'input_file', on_change=self.check,
                                     title='Select file for translation')
        self.input_file.pack({'side': 'top'}, fill=tk.X)

        self.output_file = FileSelect(self, self.data, 'output_file', on_change=self.check,
                                      save=True,
                                      title='Select file for saving translation')
        self.output_file.pack({'side': 'top'}, fill=tk.X)

        self.btn_trans = create_btn(self, 'Translate', self.translate)
        self.btn_back = create_btn(self, 'Back', self.back)
        self.btn_trans['state'] = tk.DISABLED

        signal('translator.show').connect(self.on_show)

    def reset_ui(self):
        """TODO: Docstring for reset_ui.
        :returns: TODO

        """
        self.btn_back['state'] = tk.NORMAL
        self.btn_trans['text'] = 'Translate'
        self.btn_trans['state'] = tk.NORMAL
        self.model_select.combo['values'] = sorted(self.trainers.keys())
        self.input_file.reset()
        self.output_file.reset()
        self.model_select.reset()

    def on_show(self, sender, trainers=None):
        """TODO: Docstring for on_show.

        :sender: TODO
        :returns: TODO

        """
        if trainers:
            self.trainers = trainers
        self.reset_ui()
        self.pack()

    def back(self):
        """TODO: Docstring for back.
        :returns: TODO

        """
        self.pack_forget()
        signal('translator.back').send()

    def check(self, val):
        """TODO: Docstring for check.
        :returns: TODO

        """
        if (self.data.get('input_file') and self.data.get('output_file') and
            self.data.get('model') and self.get_state_path() and
            self.get_model_path()):
            self.btn_trans['state'] = tk.NORMAL
        else:
            self.btn_trans['state'] = tk.DISABLED

    def get_model_path(self):
        """TODO: Docstring for get_model_path.
        :returns: TODO

        """
        try:
            trainer = self.trainers[self.data['model']]
            path = os.path.join(trainer['path'], trainer['id'])
            return glob(os.path.join(path, '*_model.npz'))[0]
        except:
            return None

    def get_state_path(self):
        """TODO: Docstring for get_state_path.
        :returns: TODO

        """
        try:
            trainer = self.trainers[self.data['model']]
            path = os.path.join(trainer['path'], trainer['id'])
            return glob(os.path.join(path, '*_state.pkl'))[0]
        except:
            return None

    def translate(self):
        """TODO: Docstring for translate.
        :returns: TODO

        """
        def wait():
            trans.wait()
            self.reset_ui()
        trainer = self.trainers[self.data['model']]
        model_path = self.get_model_path()
        state_path = self.get_state_path()
        in_path = self.data['input_file']
        out_path = self.data['output_file']
        glog.log('Model: %s' % model_path)
        glog.log('State: %s' % state_path)
        glog.log('File to translate: %s' % in_path)
        glog.log('File to save translation: %s' % out_path)
        trans = start_trans(trainer, state_path, model_path, in_path, out_path)
        trans_thread = Thread(target=wait)
        trans_thread.daemon = True
        self.btn_back['state'] = tk.DISABLED
        self.btn_trans['text'] = 'Translating...'
        self.btn_trans['state'] = tk.DISABLED
        trans_thread.start()
