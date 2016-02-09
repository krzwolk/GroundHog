# -*- coding: utf-8 -*-
"""
Description: ghtools
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import logging
import pprint
import numpy

from groundhog.trainer.SGD_adadelta import SGD as SGD_adadelta
from groundhog.trainer.SGD import SGD as SGD
from groundhog.trainer.SGD_momentum import SGD as SGD_momentum
from groundhog.mainLoop import MainLoop
from experiments.nmt import RNNEncoderDecoder, get_batch_iterator

log = logging.getLogger(__name__)

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

def create_loop(state, skip_init=False):
    """TODO: Docstring for create_loop.

    :state: TODO
    :skip_init: TODO
    :returns: TODO

    """
    log.debug("State:\n{}".format(pprint.pformat(state)))

    rng = numpy.random.RandomState(state['seed'])
    enc_dec = RNNEncoderDecoder(state, rng, skip_init)
    enc_dec.build()
    lm_model = enc_dec.create_lm_model()

    log.debug("Load data")
    train_data = get_batch_iterator(state)
    log.debug("Compile trainer")
    algo = eval(state['algo'])(lm_model, state, train_data)
    log.debug("Run training")
    return MainLoop(train_data, None, None, lm_model, algo, state, None,
            reset=state['reset'],
            hooks=[RandomSamplePrinter(state, lm_model, train_data)]
                if state['hookFreq'] >= 0
                else None)
