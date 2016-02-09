# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import logging
import Tkinter as tk
from blinker import signal
from .tktools import create_btn
from .trainer import Trainer

class TrainManager(tk.Frame):

    """Docstring for TrainManager. """

    log = logging.getLogger(__name__)

    def __init__(self, master):
        """TODO: to be defined1.

        :master: TODO

        """
        tk.Frame.__init__(self, master)

        self.trainers = {}
        self.trainers_mapping = []
        self.trainer = Trainer(master)

        signal('trainmanager.show').connect(self.on_show)

        self.trainers_list = tk.Listbox(self)
        self.trainers_list.pack({'side': 'top'})

        self.btn_start = create_btn(self, 'Start/Continue', self.start)
        self.btn_back = create_btn(self, 'Back', self.back)

    def on_show(self, sender, trainers=None):
        """TODO: Docstring for on_show.

        :sender: TODO
        :returns: TODO

        """
        self.trainers = trainers
        self.trainers_list.delete(0, tk.END)
        self.trainers_mapping = []
        for name in sorted(self.trainers):
            self.trainers_mapping.append(self.trainers[name])
            self.trainers_list.insert(tk.END, name)
        self.pack()

    def start(self):
        """TODO: Docstring for start.
        :returns: TODO

        """
        if self.trainers_list.curselection():
            index = self.trainers_list.curselection()[0]
            self.log.debug('Starting trainer %s', self.trainers_mapping[index])
            signal('trainer.show').send(conf=self.trainers_mapping[index])
            self.pack_forget()

    def back(self):
        """TODO: Docstring for back.
        :returns: TODO

        """
        self.pack_forget()
        signal('trainmanager.back').send()
