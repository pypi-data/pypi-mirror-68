# coding: utf-8
"""
@author: Nelson Zhao
@date:   2020-05-02 12:27
@email:  dutzhaoyeyu@163.com
"""

import tensorflow as tf
from tensorflow.keras.layers import Dense, Embedding, Flatten, Concatenate, Conv2D, LSTM, RepeatVector
from deepforecast.layers.core import CrossNet, GraphAttention
from tensorflow.keras.models import Model


def STTF(attr_columns, sequence_columns, attr_attention_embed_dim=8,
         num_cross_layers=2, attr_output_dim=32, cnn_filters=1, cnn_kernel_size=(3, 1), lstm_output_dim=32,
         recons_steps=None, forecast_steps=7, recons_task_name="recons", forecast_task_name="forecast"):
    """
    STTF for Deep Spatial-Temporal Tensor Factorization Framework
    https://dl.acm.org/doi/pdf/10.1145/3292500.3330728?download=true

    :param attr_columns: the list of SparseColumn, which refer to attribution columns
    :param sequence_columns: the list of SequenceColumn, which refer to sequence columns
    :param attr_attention_embed_dim: the projection dim used in graph attention
    :param num_cross_layers: the number of cross layers used in spatial model
    :param attr_output_dim: the output dim of the vector from spatial model
    :param cnn_filters: the number of cnn filters used in temporal model
    :param cnn_kernel_size: the kernel size of cnn filters used in temporal model
    :param lstm_output_dim: the lstm hidden size or output dim used in temporal model
    :param recons_steps: the time steps when you reconstruct information in auto-encoder, such as reconstructing
                        last 28 days, recons_steps=28 ; if param is None, it will be set to the time steps used in
                        history sequence tensor
    :param forecast_steps: the time steps when you forecast information, such as forecasting 7 days in future,
                        forecast_steps=7 ; if param is None, raise error.
    :param recons_task_name: the name of reconstruction task
    :param forecast_task_name: the name of forecast task

    :return: the object of keras.models Model
    """

    # attr embedding
    attr_embeds_list = []
    for attr_col in attr_columns:
        attr_embed = Embedding(input_dim=attr_col.vocab_size,
                               output_dim=attr_col.embed_dim,
                               embeddings_regularizer=tf.keras.regularizers.l2(attr_col.l2))(attr_col.input_tensor)
        attr_embeds_list.append(attr_embed)

    attr_embeds = Concatenate(axis=1)(attr_embeds_list)

    # Spatial Model
    graph_attention_embeds = GraphAttention(proj_dim=attr_attention_embed_dim)(attr_embeds)
    attention_embeds = Flatten()(graph_attention_embeds)
    cross_vector = CrossNet(num_layers=num_cross_layers)(attention_embeds)
    attr_latent_vec = Dense(attr_output_dim)(cross_vector)

    # Temporal Model
    _omit_pred_part = False
    if len(sequence_columns) == 1:
        _omit_pred_part = True

    # history
    hist_seq_col = sequence_columns[0]

    hist_cnn_embeds = Conv2D(filters=cnn_filters,
                             kernel_size=cnn_kernel_size,
                             data_format="channels_last")(hist_seq_col.input_tensor)
    _hist_cnn_embeds = tf.squeeze(hist_cnn_embeds, axis=-1)
    hist_cnn_feats = tf.transpose(_hist_cnn_embeds, perm=[0, 2, 1])

    hist_fw_lstm = LSTM(units=lstm_output_dim)(hist_cnn_feats)
    hist_bw_lstm = LSTM(units=lstm_output_dim, go_backwards=True)(hist_cnn_feats)
    hist_lstm = tf.add(hist_fw_lstm, hist_bw_lstm)

    if not recons_steps:
        recons_steps = hist_seq_col.input_tensor.get_shape()[-2]
    _recons_attr_vec = RepeatVector(n=recons_steps)(attr_latent_vec)
    hist_outputs = tf.matmul(_recons_attr_vec, tf.expand_dims(hist_lstm, axis=-1), name=recons_task_name)

    # future
    if not _omit_pred_part:
        fut_seq_col = sequence_columns[1]
        fut_cnn_embeds = Conv2D(filters=cnn_filters,
                                kernel_size=cnn_kernel_size,
                                data_format="channels_last")(fut_seq_col.input_tensor)
        _fut_cnn_embeds = tf.squeeze(fut_cnn_embeds, axis=-1)
        fut_cnn_feats = tf.transpose(_fut_cnn_embeds, perm=[0, 2, 1])

        fut_fw_lstm = LSTM(units=lstm_output_dim)(fut_cnn_feats)
        fut_bw_lstm = LSTM(units=lstm_output_dim, go_backwards=True)(fut_cnn_feats)
        fut_lstm = tf.add(fut_fw_lstm, fut_bw_lstm)

        concat_lstm = Concatenate()([hist_lstm, fut_lstm])
    else:
        concat_lstm = hist_lstm

    temporal_vec = Dense(units=lstm_output_dim)(concat_lstm)

    _forecast_attr_vec = RepeatVector(n=forecast_steps)(attr_latent_vec)
    fut_outputs = tf.matmul(_forecast_attr_vec, tf.expand_dims(temporal_vec, axis=-1), name=forecast_task_name)

    model = Model(
        [[attr_col.input_tensor for attr_col in attr_columns],
         [seq_col.input_tensor for seq_col in sequence_columns]],
        [hist_outputs, fut_outputs])
    return model
