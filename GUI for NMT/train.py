# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import sys
import shelve
import copy
import logging
import pprint
import numpy
import os

import experiments.nmt
from groundhog.trainer.SGD_adadelta import SGD as SGD_adadelta
from groundhog.trainer.SGD import SGD as SGD
from groundhog.trainer.SGD_momentum import SGD as SGD_momentum
from groundhog.mainLoop import MainLoop
from experiments.nmt import RNNEncoderDecoder, get_batch_iterator

from rsklab.path import rel_path_fact

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

state_map = {
    'RNNsearch-50': 'prototype_search_state',
    'RNNenc-30': 'prototype_encdec_state',
    'RNNenc-50': 'prototype_encdec_state'
}

class RandomSamplePrinter(object):

    def __init__(self, state, model, train_iter):
        args = dict(locals())
        args.pop('self')
        self.__dict__.update(**args)

    def __call__(self):
        def cut_eol(words):
            for i, word in enumerate(words):
                if words[i] == '<eol>':
                    return words[:i + 1]
            raise Exception("No end-of-line found")

        sample_idx = 0
        while sample_idx < self.state['n_examples']:
            batch = self.train_iter.next(peek=True)
            xs, ys = batch['x'], batch['y']
            for seq_idx in range(xs.shape[1]):
                if sample_idx == self.state['n_examples']:
                    break

                x, y = xs[:, seq_idx], ys[:, seq_idx]
                x_words = cut_eol(map(lambda w_idx : self.model.word_indxs_src[w_idx], x))
                y_words = cut_eol(map(lambda w_idx : self.model.word_indxs[w_idx], y))
                if len(x_words) == 0:
                    continue

                log.debug("Input: {}".format(" ".join(x_words)))
                log.debug("Target: {}".format(" ".join(y_words)))
                self.model.get_samples(self.state['seqlen'] + 1, self.state['n_samples'], x[:len(x_words)])
                sample_idx += 1

def update_custom_keys(d1, d2, keys):
    """TODO: Docstring for update_custom_keys.

    :d1: TODO
    :d2: TODO
    :keys: TODO
    :returns: TODO

    """
    for key in keys:
        if key in d2:
            d1[key] = d2[key]

def get_conf():
    """TODO: Docstring for get_conf.
    :returns: TODO

    """
    cfg_path = sys.argv[1]
    cfg_name = sys.argv[2]
    conf_db = shelve.open(cfg_path)
    conf = conf_db['trainers'][cfg_name]
    conf_db.close()
    return conf

if __name__ == '__main__':
    conf = get_conf()
    prel = rel_path_fact(os.path.join(conf['path'], conf['id']))
    os.chdir(os.path.join(conf['path'], conf['id']))

    state = getattr(experiments.nmt, state_map[conf['method']])()

    state['source'] = [prel('binarized_text.lang1.shuffle.h5')]
    state['target'] = [prel('binarized_text.lang2.shuffle.h5')]
    state['indx_word'] = prel('ivocab.lang1.pkl')
    state['indx_word_target'] = prel('ivocab.lang2.pkl')
    state['word_indx'] = prel('vocab.lang1.pkl')
    state['word_indx_trgt'] = prel('vocab.lang2.pkl')

    update_custom_keys(state, conf, ['bs', 'loopIters', 'timeStop', 'dim',
                                     'null_sym_source', 'null_sym_target'])
    if conf['method'] == 'RNNenc-50':
        state['prefix'] = 'encdec-50_'
        state['seqlen'] = 50
        state['sort_k_batches'] = 20

    log.debug("State:\n{}".format(pprint.pformat(state)))

    rng = numpy.random.RandomState(state['seed'])
    enc_dec = RNNEncoderDecoder(state, rng, False)
    enc_dec.build()
    lm_model = enc_dec.create_lm_model()

    log.debug("Load data")
    train_data = get_batch_iterator(state)
    log.debug("Compile trainer")
    algo = eval(state['algo'])(lm_model, state, train_data)
    log.debug("Run training")
    main = MainLoop(train_data, None, None, lm_model, algo, state, None,
                    reset=state['reset'],
                    hooks=[RandomSamplePrinter(state, lm_model, train_data)]
                    if state['hookFreq'] >= 0
                    else None)
    if state['reload']:
        main.load()
    if state['loopIters'] > 0:
        main.main()
