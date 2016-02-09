# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import os

def rel_path_fact(base):
    """TODO: Docstring for rel_path_fact.

    :base: TODO
    :returns: TODO

    """
    def rel_path(filename):
        return os.path.join(base, filename)
    return rel_path
