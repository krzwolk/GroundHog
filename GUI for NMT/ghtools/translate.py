# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import os
from subprocess import Popen
from ghtools import conf

def start_trans(theano_conf, state, model, in_path, out_path):
    """TODO: Docstring for start_trans.

    :theano_conf: TODO
    :state: TODO
    :model: TODO
    :in_path: TODO
    :out_path: TODO
    :returns: TODO

    """
    env = os.environ.copy()
    env['THEANO_FLAGS'] = conf.build_theano_env(theano_conf)
    if theano_conf['cores']:
        env['OMP_NUM_THREADS'] = str(theano_conf['cores'])
    proc = Popen(['python', 'translate.py', '--beam-size', '10',
                  '--beam-search', '--state', state, '--source', in_path,
                  '--trans', out_path, model], env=env)
    return proc
