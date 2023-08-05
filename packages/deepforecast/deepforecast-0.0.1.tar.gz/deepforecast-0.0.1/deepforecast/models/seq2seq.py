# coding: utf-8
"""
@author: Nelson Zhao
@date:   2020-05-05 16:35
@email:  dutzhaoyeyu@163.com
"""
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Model
from deepforecast.layers import Encoder, Decoder


def seq2seq(encoder_inputs, decoder_inputs, encoder_timesteps, encoder_input_dim, decoder_timesteps, decoder_input_dim,
            num_encoder_layers=1, num_encoder_hidden_dim=16, num_decoder_layers=1, num_decoder_hidden_dim=16,
            num_dense_layers=1, num_dense_hidden_dim=16, dense_activation="relu", rnn_type="lstm"):
    """
    The vanilla Seq2Seq model
    https://papers.nips.cc/paper/5346-sequence-to-sequence-learning-with-neural-networks.pdf

    :param encoder_inputs: The encoder input sequences, (None, timesteps, input_dim)
    :param decoder_inputs: The encoder input sequences, (None, timesteps, output_dim)
    :param encoder_timesteps:
    :param encoder_input_dim:
    :param decoder_timesteps:
    :param decoder_input_dim:
    :param num_encoder_layers:
    :param num_encoder_hidden_dim:
    :param num_decoder_layers:
    :param num_decoder_hidden_dim:
    :param num_dense_layers:
    :param num_dense_hidden_dim:
    :param dense_activation:
    :param rnn_type:
    :return:
    """
    # build encoder
    encoder = Encoder(encoder_timesteps=encoder_timesteps,
                      encoder_input_dim=encoder_input_dim,
                      num_encoder_layers=num_encoder_layers,
                      num_encoder_hidden_dim=num_encoder_hidden_dim,
                      rnn_type=rnn_type)
    # build decoder
    decoder = Decoder(decoder_timesteps=decoder_timesteps,
                      decoder_input_dim=decoder_input_dim,
                      num_decoder_layers=num_decoder_layers,
                      num_decoder_hidden_dim=num_decoder_hidden_dim,
                      rnn_type=rnn_type)

    # build dense
    decoder_dense_layer = Dense(units=num_dense_hidden_dim, activation=dense_activation)

    # build encoder
    encoder_outputs, encoder_state_h, encoder_state_c = encoder(encoder_inputs)
    encoder_states = (encoder_state_h, encoder_state_c)

    # build decoder
    decoder_outputs = decoder([decoder_inputs, encoder_states])

    # mlp layer
    decoder_dense = decoder_outputs
    for _ in range(num_dense_layers):
        decoder_dense = decoder_dense_layer(decoder_dense)

    # output layer
    outputs = Dense(1)(decoder_dense)

    model = Model([encoder_inputs, decoder_inputs], outputs)

    return model
