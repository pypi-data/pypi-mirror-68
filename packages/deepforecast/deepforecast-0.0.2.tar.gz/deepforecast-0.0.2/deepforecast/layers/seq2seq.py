# coding: utf-8
"""
@author: Nelson Zhao
@date:   2020-05-02 12:32
@email:  dutzhaoyeyu@163.com
"""

import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras.layers import Layer, Input, LSTM, GRU, LSTMCell, GRUCell, Flatten, Dense
from tensorflow.keras.models import Model


class Encoder(Layer):
    def __init__(self, encoder_timesteps, encoder_input_dim, num_encoder_layers=1,
                 num_encoder_hidden_dim=16, rnn_type="lstm", **kwargs):
        """
        Encoder Class of Seq2Seq Model
        :param encoder_timesteps:
        :param encoder_input_dim:
        :param num_encoder_layers:
        :param num_encoder_hidden_dim:
        :param rnn_type:
        """
        super(Encoder, self).__init__(**kwargs)
        self.encoder_timesteps = encoder_timesteps
        self.encoder_input_dim = encoder_input_dim
        self.num_encoder_layers = num_encoder_layers
        self.num_encoder_hidden_dim = num_encoder_hidden_dim
        self.rnn_type = rnn_type

        if self.rnn_type == "gru":
            self.RNN = GRU
        else:
            self.RNN = LSTM

        assert num_encoder_layers >= 1
        if self.num_encoder_layers == 1:
            self.encoder_rnn = self.RNN(self.num_encoder_hidden_dim, return_state=True)
        else:
            self.encoder_rnn = self.RNN(self.num_encoder_hidden_dim, return_sequences=True, return_state=True)

    def call(self, inputs, **kwargs):
        if self.num_encoder_layers == 1:
            encoder_outputs, encoder_state_h, encoder_state_c = self.encoder_rnn(inputs)
        else:
            encoder_outputs = inputs
            for _ in range(self.num_encoder_layers):
                encoder_outputs, encoder_state_h, encoder_state_c = self.encoder_rnn(encoder_outputs)
        return encoder_outputs, encoder_state_h, encoder_state_c

    def get_config(self):
        config = {"encoder_timesteps": self.encoder_timesteps,
                "encoder_input_dim": self.encoder_input_dim,
                "num_encoder_layers": self.num_encoder_layers,
                "num_encoder_hidden_dim": self.num_encoder_hidden_dim,
                "rnn_type": self.rnn_type}
        base_config = super(Encoder, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class Decoder(Layer):
    def __init__(self, decoder_timesteps, decoder_input_dim, num_decoder_layers=1,
                 num_decoder_hidden_dim=16, rnn_type="lstm", **kwargs):
        """
        Decoder class of Seq2Seq Model
        :param decoder_timesteps:
        :param decoder_input_dim:
        :param num_decoder_layers:
        :param num_decoder_hidden_dim:
        :param rnn_type:
        """
        super(Decoder, self).__init__(**kwargs)
        self.decoder_timesteps = decoder_timesteps
        self.decoder_input_dim = decoder_input_dim
        self.num_decoder_layers = num_decoder_layers
        self.num_decoder_hidden_dim = num_decoder_hidden_dim
        self.rnn_type = rnn_type

        if self.rnn_type == "gru":
            self.RNN = GRU
        else:
            self.RNN = LSTM

        assert num_decoder_layers >= 1
        self.decoder_rnn = self.RNN(self.num_decoder_hidden_dim, return_sequences=True, return_state=True)

    def call(self, inputs, **kwargs):
        assert isinstance(inputs, tuple) or isinstance(inputs, list)
        decoder_inputs = inputs[0]
        context_vector = inputs[1]
        if self.num_decoder_layers == 1:
            decoder_outputs, _, _ = self.decoder_rnn(decoder_inputs, initial_state=context_vector)
        else:
            decoder_outputs = decoder_inputs
            for _ in range(self.num_decoder_layers):
                decoder_outputs, _, _ = self.decoder_rnn(decoder_outputs, initial_state=context_vector)

        return decoder_outputs

    def get_config(self):
        config = {"decoder_timesteps": self.decoder_timesteps,
                "decoder_input_dim": self.decoder_input_dim,
                "num_decoder_layers": self.num_decoder_layers,
                "num_decoder_hidden_dim": self.num_decoder_hidden_dim,
                "rnn_type": self.rnn_type}
        base_config = super(Decoder, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class AttentionSeq2Seq(Layer):
    pass
