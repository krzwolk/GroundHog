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

def start_trainer(trainer_conf):
    """TODO: Docstring for start_trainer.

    :trainer_conf: TODO
    :returns: TODO

    """
    env = os.environ.copy()
    env['THEANO_FLAGS'] = conf.build_theano_env(trainer_conf)
    if trainer_conf['cores']:
        env['OMP_NUM_THREADS'] = str(trainer_conf['cores'])
    proc = Popen(['python', conf.trainer, conf.trainer_conf_path, trainer_conf['name']], env=env)
    return proc
