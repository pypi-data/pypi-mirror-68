# coding: utf-8
"""
@author: Nelson Zhao
@date:   2020-05-02 14:56
@email:  dutzhaoyeyu@163.com
"""
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding


class Column(object):
    def __init__(self, name, **kwargs):
        self.name = name


class SparseColumn(Column):

    def __init__(self, name, vocab_size, embed_dim=8, l2=0.5, **kwargs):
        super(SparseColumn, self).__init__(name, **kwargs)
        self.name = name
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.l2 = l2
        self.input_tensor = Input(shape=(1,), name=self.name)


class DenseColumn(Column):

    def __init__(self, name, **kwargs):
        super(DenseColumn, self).__init__(name, **kwargs)
        self.name = name
        self.input_tensor = Input(shape=(1,), name=self.name)


class SequenceColumn(Column):

    def __init__(self, name, num_seq, seq_steps, dim, **kwargs):
        super(SequenceColumn, self).__init__(name, **kwargs)
        self.name = name
        self.num_seq = num_seq
        self.seq_steps = seq_steps
        self.dim = dim
        self.input_tensor = Input(shape=(self.num_seq, self.seq_steps, self.dim), name=self.name)
