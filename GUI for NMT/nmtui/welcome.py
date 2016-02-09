# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import Tkinter as tk
from time import sleep
from threading import Thread
from blinker import signal
from .trainmaster import TrainMaster
from .trainmanager import TrainManager
from .translator import Translator
from .tktools import create_btn
from rsklab.globlog import glog


class Welcome(tk.Frame):

    """Docstring for Welcome. """

    def __init__(self, master, conf):
        """TODO: to be defined1.

        :master: TODO

        """
        tk.Frame.__init__(self, master)

        self.conf = conf

        self.welcome_frame = tk.Frame(master)
        self.welcome_frame.pack({'side': 'top'})
        self.btn_frame = tk.Frame(self.welcome_frame)
        self.btn_frame.pack({'side': 'top'})
        self.details_frame = tk.Frame(master)
        self.details_frame.pack({'side': 'top'}, fill=tk.X)

        # Creates new trainer
        self.train_master = TrainMaster(self.welcome_frame)
        # Manage existing trainers
        self.train_manager = TrainManager(self.welcome_frame)
        # Translate text
        self.trans = Translator(self.welcome_frame)

        self.btn_create_trainer = create_btn(
            self.btn_frame, 'Create Trainer', self.open_train_master)

        self.btn_manage_trainer = create_btn(
            self.btn_frame, 'Manage Trainers', self.open_train_manager)

        self.btn_trans = create_btn(
            self.btn_frame, 'Translate', self.open_trans)

        self.btn_lm = tk.Button(self.btn_frame, state=tk.DISABLED)
        self.btn_lm['text'] = 'Language Modeling'
        self.btn_lm.pack({'side': 'top'}, fill=tk.X)

        self.btn_tuning = tk.Button(self.btn_frame, state=tk.DISABLED)
        self.btn_tuning['text'] = 'Tuning'
        self.btn_tuning.pack({'side': 'top'}, fill=tk.X)

        self.btn_test = tk.Button(self.btn_frame, state=tk.DISABLED)
        self.btn_test['text'] = 'Test'
        self.btn_test.pack({'side': 'top'}, fill=tk.X)

        self.btn_details = create_btn(self.details_frame, 'Details', self.show_details)
        self.details = tk.Text(self.details_frame, height=10)
        self.details.forget()
        self.is_show_details = False

        signal('langmaster.cancel').connect(self.show_welcome)
        signal('trainmaster.back').connect(self.show_welcome)
        signal('trainmaster.new_trainer').connect(self.new_trainer)
        signal('trainmanager.back').connect(self.show_welcome)
        signal('translator.back').connect(self.show_welcome)
        signal('trainer.stop').connect(self.show_welcome)
        signal('trainer.confupdate').connect(self.trainer_conf_update)
        self.pack()

        self.log_updater = Thread(target=self.update_log)
        self.log_updater.daemon = True
        self.log_updater.start()

    def show_welcome(self, sender):
        """TODO: Docstring for show_welcome.

        :sender: TODO
        :returns: TODO

        """
        self.btn_frame.pack()

    def open_train_master(self):
        """TODO: Docstring for open_train_master.
        :returns: TODO

        """
        self.btn_frame.pack_forget()
        signal('trainmaster.show').send()

    def open_train_manager(self):
        """TODO: Docstring for open_train_manager.
        :returns: TODO

        """
        self.btn_frame.pack_forget()
        signal('trainmanager.show').send(trainers=self.conf.get('trainers', {}))

    def new_trainer(self, sender, data=None):
        """TODO: Docstring for new_trainer.

        :data: TODO
        :returns: TODO

        """
        self.conf.setdefault('trainers', {})[data['name']] = data
        self.conf.sync()
        self.btn_frame.pack()

    def open_trans(self):
        """TODO: Docstring for open_trans.
        :returns: TODO

        """
        self.btn_frame.pack_forget()
        signal('translator.show').send(trainers=self.conf.get('trainers', {}))

    def show_details(self):
        """TODO: Docstring for show_details.
        :returns: TODO

        """
        if self.is_show_details:
            self.details.forget()
        else:
            self.details.pack({'side': 'top'}, fill=tk.X)
        self.is_show_details = not self.is_show_details

    def trainer_conf_update(self, sender, data=None):
        """TODO: Docstring for trainer_conf_update.

        :sender: TODO
        :data: TODO
        :returns: TODO

        """
        self.conf.setdefault('trainers', {})[data['name']] = data
        self.conf.sync()

    def update_log(self):
        """TODO: Docstring for update_log.
        :returns: TODO

        """
        from rsklab.globlog import get_fifo
        while True:
            self.details.delete(1.0, tk.END)
            self.details.insert(tk.END, glog.get_log())
            sleep(2)
