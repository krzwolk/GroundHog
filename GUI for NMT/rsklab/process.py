# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from threading import Thread
from subprocess import Popen, PIPE, STDOUT

def run_with_output(cmd):
    """TODO: Docstring for run_with_output.

    :cmd: TODO
    :returns: TODO

    """
    proc = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    while True:
        line = proc.stdout.readline()
        if line:
            yield line
        else:
            break

def iter_reader(fn, items):
    """TODO: Docstring for iter_reader.

    :fn: TODO
    :items: TODO
    :returns: TODO

    """
    def _reader():
        for item in items:
            fn(item)
    th = Thread(target=_reader)
    th.daemon = True
    th.start()
