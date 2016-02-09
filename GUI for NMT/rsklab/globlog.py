# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import os
import logging
from tempfile import mkdtemp
from threading import Thread

temp_dir_path = mkdtemp()
fifo = os.path.join(temp_dir_path, 'nmtui.socket')
os.mkfifo(fifo)

class Log(object):

    """Docstring for Log. """

    def __init__(self, max_count):
        """TODO: to be defined1.

        :max_count: TODO

        """
        self.max_count = max_count
        self.msgs = []

    def log(self, msg):
        """TODO: Docstring for log.

        :msg: TODO
        :returns: TODO

        """
        self.msgs.append(msg)
        if len(self.msgs) > (self.max_count*2):
            self.msgs = self.msgs[-self.max_count:]

    def get_messages(self):
        """TODO: Docstring for get_messages.
        :returns: TODO

        """
        return self.msgs

    def get_log(self):
        """TODO: Docstring for get_log.
        :returns: TODO

        """
        return '\n'.join(self.msgs)

glog = Log(1000)

def fifo_reader():
    """TODO: Docstring for fifo_reader.
    :returns: TODO

    """
    f = open(fifo, 'r', 0)
    while True:
        data = f.read()
        if not data:
            break
        for msg in data.split('\n'):
            glog.log(msg)

def get_fifo(mode='w'):
    """TODO: Docstring for get_fifo_w.
    :returns: TODO

    """
    return open(fifo, mode, 0)

def get_fifo_path():
    """TODO: Docstring for get_fifo_path.

    :arg1: TODO
    :returns: TODO

    """
    return fifo

reader = Thread(target=fifo_reader)
reader.daemon = True
reader.start()
stream_hander = logging.StreamHandler(get_fifo('w'))
logging.getLogger().addHandler(stream_hander)
