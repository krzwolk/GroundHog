# -*- coding: utf-8 -*-
"""
Description: UI for NMT
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import Tkinter
import tkFont
import os
import shelve
import json
import logging
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from .welcome import Welcome
from ghtools.conf import set_conf
from rsklab.globlog import get_fifo_path

def get_args():
    """TODO: Docstring for get_args.
    :returns: TODO

    """
    home_path = os.path.expanduser('~')
    conf_path = os.path.join(home_path, '.nmtui', 'nmtui.db')
    parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('-c', '--conf', default=conf_path, help='Path to configuration file')
    parser.add_argument('--groundhog', help='Path to groundhog sources')
    parser.add_argument('--fs', help='Font size')
    args = parser.parse_args()
    try:
        os.makedirs(os.path.dirname(args.conf))
    except os.error:
        pass
    args.conf_path = args.conf
    args.conf = shelve.open(args.conf, writeback=True)
    return args

def set_font(root, size):
    """TODO: Docstring for set_font.

    :root: TODO
    :size: TODO
    :returns: TODO

    """
    default_font = tkFont.nametofont('TkDefaultFont')
    default_font.configure(size=size)
    root.option_add('*Font', default_font)

def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    logging.basicConfig(level=logging.DEBUG)

    args = get_args()
    root = Tkinter.Tk()
    if args.fs:
        set_font(root, args.fs)
        args.conf['fs'] = args.fs
        args.conf.sync()
    else:
        if 'fs' in args.conf:
            set_font(root, args.conf['fs'])
    if args.groundhog:
        args.conf['groundhog'] = args.groundhog
        args.conf.sync()
    if 'groundhog' not in args.conf:
        print('Please first run program with "--groundhog" key, with path to groundhog sources')
        exit(1)
    if not os.path.exists(os.path.join(args.conf['groundhog'], 'experiments')):
        print('Incorrect path to groundhog sources, please run first with "--groundhog" key')
        exit(1)

    #if os.fork() > 0:
    #    sys.exit(0)

    # sys.stdout.flush()
    # sys.stderr.flush()
    # si = file('/dev/null', 'r')
    # so = file(get_fifo_path(), 'a+')
    # se = file(get_fifo_path(), 'a+', 0)
    # os.dup2(si.fileno(), sys.stdin.fileno())
    # os.dup2(so.fileno(), sys.stdout.fileno())
    # os.dup2(se.fileno(), sys.stderr.fileno())

    print('Configuration:')
    print(json.dumps(dict(args.conf), sort_keys=True, indent=2))
    set_conf({
        'conf_path': args.conf_path,
        'groundhog': args.conf['groundhog'],
        'nmtui_path': os.path.dirname(os.path.dirname(__file__))
    })
    app = Welcome(root, args.conf)
    app.mainloop()
