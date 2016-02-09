# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import Tkinter as tk
import os
from uuid import uuid4
from shutil import copyfile
from signal import SIGINT
from threading import Thread
from blinker import signal
from .tktools import create_btn
from rsklab.globlog import glog
from ghtools import preprocess
from ghtools.train import start_trainer
from rsklab.path import rel_path_fact

class ChangeInPlace(object):

    """Docstring for ChangeInPlace. """

    def __init__(self, path):
        """TODO: to be defined1.

        :path: TODO

        """
        self.path = path
        self.path_out = '{}.{}'.format(path, uuid4().hex)

    def __enter__(self):
        """TODO: Docstring for __enter__.
        :returns: TODO

        """
        return (self.path, self.path_out)

    def __exit__(self, exc_type, exc_value, traceback):
        """TODO: Docstring for __exit__.

        :exc_type: TODO
        :exc_value: TODO
        :traceback: TODO
        :returns: TODO

        """
        if exc_type:
            try:
                os.remove(self.path_out)
            except:
                pass
        else:
            try:
                os.remove(self.path)
            except:
                pass
            os.rename(self.path_out, self.path)

class Trainer(tk.Frame):

    """Docstring for Trainer. """

    def __init__(self, master):
        """TODO: to be defined1.

        :master: TODO

        """
        tk.Frame.__init__(self, master)

        self.conf = None
        self.trainer = None

        signal('trainer.show').connect(self.on_show)
        signal('trainer.jobfinished').connect(self.on_job_finished)

        self.btn_stop = create_btn(self, 'Stop', self.stop)
        self.stop_pressed = False

    def on_show(self, sender, conf=None):
        """TODO: Docstring for on_show.

        :sender: TODO
        :conf: TODO
        :returns: TODO

        """
        self.btn_stop['text'] = 'Stop'
        self.conf = conf
        self.path = os.path.join(conf['path'], conf['id'])
        self.prel = rel_path_fact(self.path)
        self.pack()
        self.start_state()

    def start_state(self):
        """TODO: Docstring for start_state.
        :returns: TODO

        """
        if self.get_state() == 0:
            self.btn_stop.config(state=tk.DISABLED)
            try:
                os.makedirs(self.path)
            except:
                pass
            job = Thread(target=self.preprocess)
            job.daemon = True
            job.start()
        elif self.get_state() == 1:
            job = Thread(target=self.train)
            job.daemon = True
            job.start()
            self.btn_stop.config(state=tk.NORMAL)
        elif self.get_state() == 2:
            self.btn_stop['text'] = 'Close (train finished)'

    def stop(self):
        """TODO: Docstring for stop.
        :returns: TODO

        """
        self.stop_pressed = True
        try:
            self.trainer.send_signal(SIGINT)
        except:
            pass
        if self.trainer:
            self.trainer.wait()
            self.trainer = None
        self.pack_forget()
        signal('trainer.stop').send()

    def preprocess(self):
        """TODO: Docstring for preprocess.
        :returns: TODO

        """
        glog.log('Preparing text data')
        glog.log('Copying source text files to project directory')
        copyfile(self.conf['text1_path'], self.prel('lang1.txt'))
        copyfile(self.conf['text2_path'], self.prel('lang2.txt'))

        glog.log('Before tokenization preprocessing')
        if self.conf['norm_punctuation']:
            glog.log('Normalize punctuation')
            with ChangeInPlace(self.prel('lang1.txt')) as (pin, pout):
                preprocess.norm_punct(pin, pout)
            with ChangeInPlace(self.prel('lang2.txt')) as (pin, pout):
                preprocess.norm_punct(pin, pout)

        if self.conf['clean_corpus']:
            glog.log('Clean corpus')
            with ChangeInPlace(self.prel('lang1.txt')) as (p1in, p1out),\
                    ChangeInPlace(self.prel('lang2.txt')) as (p2in, p2out):
                preprocess.filter_by_words_len(p1in, p2in, p1out, p2out, self.conf['clean_corpus_n'])

        glog.log('Tokenization')
        preprocess.tokenize(
            self.conf['lang1'],
            self.prel('lang1.txt'),
            self.prel('lang1.tok.txt'))
        preprocess.tokenize(
            self.conf['lang2'],
            self.prel('lang2.txt'),
            self.prel('lang2.tok.txt'))
        glog.log('After tokenization preprocessing')

        if self.conf['lower_casing']:
            glog.log('Lower casing')
            with ChangeInPlace(self.prel('lang1.tok.txt')) as (pin, pout):
                preprocess.lowercase(pin, pout)
            with ChangeInPlace(self.prel('lang2.tok.txt')) as (pin, pout):
                preprocess.lowercase(pin, pout)

        glog.log('Preprocess')
        preprocess.preprocess(
            self.prel('vocab.lang1.pkl'),
            self.prel('binarized_text.lang1.pkl'),
            self.prel('lang1.tok.txt'))
        preprocess.preprocess(
            self.prel('vocab.lang2.pkl'),
            self.prel('binarized_text.lang2.pkl'),
            self.prel('lang2.tok.txt'))

        glog.log('Invert dict')
        preprocess.invert_dict(
            self.prel('vocab.lang1.pkl'),
            self.prel('ivocab.lang1.pkl'))
        preprocess.invert_dict(
            self.prel('vocab.lang2.pkl'),
            self.prel('ivocab.lang2.pkl'))

        glog.log('Convert pkl-hdf5')
        preprocess.convert_dict(
            self.prel('binarized_text.lang1.pkl'),
            self.prel('binarized_text.lang1.h5'))
        preprocess.convert_dict(
            self.prel('binarized_text.lang2.pkl'),
            self.prel('binarized_text.lang2.h5'))

        glog.log('Shuffle hdf5')
        preprocess.shuffle_hdf5(
            self.prel('binarized_text.lang1.h5'),
            self.prel('binarized_text.lang2.h5'),
            self.prel('binarized_text.lang1.shuffle.h5'),
            self.prel('binarized_text.lang2.shuffle.h5'))
        self.set_state(1)
        signal('trainer.jobfinished').send()

    def train(self):
        """TODO: Docstring for train.
        :returns: TODO

        """
        self.trainer = start_trainer(self.conf)
        self.trainer.wait()
        if not self.stop_pressed:
            self.set_state(2)
            signal('trainer.jobfinished').send()
        self.stop_pressed = False

    def set_state(self, state):
        """TODO: Docstring for set_state.

        :state: TODO
        :returns: TODO

        """
        assert state > self.conf.setdefault('state', 0)
        self.conf['state'] = state
        signal('trainer.confupdate').send(data=self.conf)

    def get_state(self):
        """TODO: Docstring for get_state.
        :returns: TODO

        """
        return self.conf.setdefault('state', 0)

    def on_job_finished(self, sender):
        """TODO: Docstring for on_job_finished.

        :sender: TODO
        :returns: TODO

        """
        self.start_state()
