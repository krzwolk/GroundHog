# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import os
import theano

groundhog = None
tokenizer = None
tok_langs = []
preprocessor = None
invertor = None
converter = None
shuffler = None
trainer_conf_path = None
trainer = None
translator = None
scripts3rd_path = None
lowercase_perl = None
norm_punct_perl = None

def set_conf(conf):
    """TODO: Docstring for set_conf.

    :conf: TODO
    :returns: TODO

    """
    global groundhog
    global tokenizer
    global tok_langs
    global preprocessor
    global invertor
    global converter
    global shuffler
    global trainer_conf_path
    global trainer
    global translator
    global scripts3rd_path
    global lowercase_perl
    global norm_punct_perl
    base = os.path.dirname(os.path.dirname(__file__))
    groundhog = conf['groundhog']
    tokenizer = os.path.join(groundhog, 'experiments', 'nmt', 'web-demo',
                             'tokenizer.perl')
    tok_file_path = os.path.join(groundhog, 'experiments', 'nmt', 'web-demo', 'nonbreaking_prefixes')
    tok_langs = []
    for path in os.listdir(tok_file_path):
        tok_langs.append(path[-2:])
    tok_langs.sort()
    preprocessor = os.path.join(groundhog, 'experiments', 'nmt', 'preprocess',
                                'preprocess.py')
    invertor = os.path.join(groundhog, 'experiments', 'nmt', 'preprocess',
                            'invert-dict.py')
    converter = os.path.join(groundhog, 'experiments', 'nmt', 'preprocess',
                             'convert-pkl2hdf5.py')
    shuffler = os.path.join(groundhog, 'experiments', 'nmt', 'preprocess',
                            'shuffle-hdf5.py')
    trainer_conf_path = conf['conf_path']
    trainer = os.path.join(base, 'train.py')
    translator = os.path.join(base, 'translate.py')
    scripts3rd_path = os.path.join(conf['nmtui_path'], '3rd')
    lowercase_perl = os.path.join(scripts3rd_path, 'lowercase.perl')
    norm_punct_perl = os.path.join(scripts3rd_path, 'normalize-punctuation.perl')

def set_theano_conf(conf):
    """TODO: Docstring for set_theano_conf.

    :conf: TODO
    :returns: TODO

    """
    # Theano configuration
    theano.config.floatX = 'float32'
    theano.config.nvcc.fastmath = True
    theano.config.device = conf['processor'].lower()
    if not conf['cores']:
        os.environ.pop('OMP_NUM_THREADS', None)
    else:
        os.environ['OMP_NUM_THREADS'] = str(conf['cores'])
    theano.config.on_unused_input = 'warn'

def build_theano_env(conf):
    """TODO: Docstring for build_theano_env.

    :conf: TODO
    :returns: TODO

    """
    tmpl = 'floatX=float32,device={},nvcc.fastmath=True,on_unused_input=warn'
    return tmpl.format(conf['processor'].lower())
