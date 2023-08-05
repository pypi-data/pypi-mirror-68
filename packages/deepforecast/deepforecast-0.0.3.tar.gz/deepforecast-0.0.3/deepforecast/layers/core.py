# coding: utf-8
"""
@author: Nelson Zhao
@date:   2020-05-02 15:02
@email:  dutzhaoyeyu@163.com
"""

import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Layer, Dense, RepeatVector, Flatten, Concatenate, Activation


class CrossNet(Layer):
    """
    Cross Net
    """
    def __init__(self, num_layers, **kwargs):
        self.num_layers = num_layers
        super(CrossNet, self).__init__(**kwargs)

    def build(self, input_shape):
        assert len(input_shape) == 2, ValueError("Unexpected inputs dimensions")
        dim = int(input_shape[-1])
        self.kernels = [self.add_weight(name="kernels",
                                        shape=(dim,),
                                        initializer='uniform',
                                        trainable=True) for _ in range(self.num_layers)]
        self.bias = [self.add_weight(name="bias",
                                     shape=(dim,),
                                     initializer='zeros',
                                     trainable=True
                                     ) for _ in range(self.num_layers)]
        super(CrossNet, self).build(input_shape)

    def call(self, inputs, **kwargs):
        xl = inputs
        for i in range(self.num_layers):
            xl = self._build_single_cross_layer(i, inputs, xl)

        return xl

    def compute_output_shape(self, input_shape):
        return input_shape

    def _build_single_cross_layer(self, layer_idx, x0, xl):
        embed_dim = xl.get_shape()[-1]
        x_lw = tf.tensordot(tf.reshape(xl, [-1, 1, embed_dim]), self.weights[layer_idx], axes=1)
        cross = x0 * x_lw + self.bias[layer_idx] + xl
        return cross

    def get_config(self):
        config = {"num_layers": self.num_layers}
        base_config = super(CrossNet, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class MultiLayerSelfAttention(Layer):
    def __init__(self, n_layers, **kwargs):
        self.n_layers = n_layers
        super(MultiLayerSelfAttention, self).__init__(**kwargs)

    def build(self, input_shape):
        dim = int(input_shape[-1])
        self.weights = self.add_weight(name="weights",
                                       shape=(dim,),
                                       initializer='uniform',
                                       trainable=True)
        self.bias = self.add_weight(name="bias",
                                    shape=(dim,),
                                    initializer='zeros',
                                    trainable=True
                                    )
        super(MultiLayerSelfAttention, self).build(input_shape)  # Be sure to call this at the end

    def call(self, x):
        xl = x
        for i in range(self.n_layers):
            xl = self._build_cross_layer(i, x, xl)

        return xl

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.output_dim)

    def _build_cross_layer(self, layer, x0, xl):
        embed_dim = xl.shape[-1]
        x_lw = tf.tensordot(tf.reshape(xl, [-1, 1, embed_dim]), self.weights[layer], axes=1)
        cross = x0 * x_lw + self.bias[layer] + xl
        return cross


class GraphAttention(Layer):
    """
    Attention Layer for Graph Attention Network (GAT)
    """
    def __init__(self, proj_dim, **kwargs):
        super(GraphAttention, self).__init__(**kwargs)
        self.proj_dim = proj_dim

    def build(self, input_shape):
        """

        :param input_shape: 3D tensor for
        :return:
        """
        assert len(input_shape) == 3, IndexError
        self.num_feats = input_shape[1]
        self.input_dim = input_shape[-1]

        self.kernel = self.add_weight(name="kernel",
                                      shape=(self.input_dim, self.proj_dim),
                                      initializer="glorot_normal",
                                      trainable=True)


        self.repeator = RepeatVector(self.num_feats)
        self.flatten = Flatten()
        self.concat = Concatenate(axis=-1)
        self.dense = Dense(units=1, activation="relu")  # 改成leaky relu
        self.softmax = Activation(activation="softmax")
        super(GraphAttention, self).build(input_shape)

    def call(self, inputs, **kwargs):
        proj_inputs = K.dot(inputs, self.kernel)
        proj_inputs_list = tf.split(value=proj_inputs, num_or_size_splits=self.num_feats, axis=1)

        attention_outputs_list = []
        for proj_input in proj_inputs_list:
            repeat_input = self.repeator(self.flatten(proj_input))
            energy = self.dense(self.concat([repeat_input, proj_inputs]))
            alpha = self.softmax(energy)

            attention_output = tf.matmul(a=proj_inputs, b=alpha, transpose_a=True, transpose_b=False)
            attention_outputs_list.append(attention_output)

        outputs = tf.transpose(self.concat(attention_outputs_list), perm=[0, 2, 1])
        return outputs

    def compute_output_shape(self, input_shape):
        return input_shape[:-1] + self.proj_dim

    def get_config(self):
        config = {"proj_dim": self.proj_dim}
        base_config = super(GraphAttention, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class AutoEncoder(Layer):
    pass


class MLP(Layer):
    def __init__(self, num_layers, units, dropout, **kwargs):
        super(MLP, self).__init__(**kwargs)

        if isinstance(num_layers, int) and isinstance(units, int):
            self.layers = [units] * num_layers
        elif isinstance(units, list) or isinstance(units, tuple):
            self.layers = list(units)

    def build(self, input_shape):
        self.dense = Dense(units=1)

    def call(self, inputs, **kwargs):
        pass

