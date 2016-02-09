# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from itertools import izip
from subprocess import call
from ghtools import conf

def tokenize(lang, in_path, out_path):
    """TODO: Docstring for tokenize.

    :lang: TODO
    :in_path: TODO
    :out_path: TODO
    :returns: TODO

    """
    with open(in_path) as in_file, open(out_path, 'w') as out_file:
        call(['perl', conf.tokenizer, '-l', lang], stdin=in_file.fileno(),
             stdout=out_file.fileno())

def preprocess(vocab, bin_text, text):
    """TODO: Docstring for preprocess.

    :vocab: TODO
    :bin_text: TODO
    :text: TODO
    :returns: TODO

    """
    call(['python', conf.preprocessor, '-d', vocab, '-v', '30000', '-b',
          bin_text, '-p', text])

def invert_dict(vocab, ivocab):
    """TODO: Docstring for invert_dict.

    :vocab: TODO
    :ivocab: TODO
    :returns: TODO

    """
    call(['python', conf.invertor, vocab, ivocab])

def convert_dict(bin_text, bin_text_h5):
    """TODO: Docstring for convert_dict.

    :bin_text: TODO
    :bin_text_h5: TODO
    :returns: TODO

    """
    call(['python', conf.converter, bin_text, bin_text_h5])

def shuffle_hdf5(bin_text1, bin_text2, bin_text_s1, bin_text_s2):
    """TODO: Docstring for shuffle_hdf5.

    :bin_text1: TODO
    :bin_text2: TODO
    :bin_text_s1: TODO
    :bin_text_s2: TODO
    :returns: TODO

    """
    call(['python', conf.shuffler, bin_text1, bin_text2, bin_text_s1, bin_text_s2])

def lowercase(path_in, path_out):
    """TODO: Docstring for lowercase.

    :path_in: TODO
    :path_out: TODO
    :returns: TODO

    """
    call(['perl', conf.lowercase_perl], stdin=open(path_in), stdout=open(path_out, 'w'))

def norm_punct(path_in, path_out):
    """TODO: Docstring for norm_punct.

    :path_in: TODO
    :path_out: TODO
    :returns: TODO

    """
    call(['perl', conf.norm_punct_perl], stdin=open(path_in), stdout=open(path_out, 'w'))

def filter_by_words_len(path1_in, path2_in, path1_out, path2_out, max_words):
    """TODO: Docstring for filter_by_words_len.

    :path1_in: TODO
    :path2_in: TODO
    :path1_out: TODO
    :path2_out: TODO
    :max_words: TODO
    :returns: TODO

    """
    with open(path1_in) as f1_in,\
            open(path2_in) as f2_in,\
            open(path1_out, 'w') as f1_out,\
            open(path2_out, 'w') as f2_out:
        for (text1, text2) in izip(f1_in, f2_in):
            if len(text1.split()) > max_words:
                continue
            if len(text2.split()) > max_words:
                continue
            f1_out.write(text1)
            f2_out.write(text2)
