# coding: utf-8
"""
@author: Nelson Zhao
@date:   2020-05-02 15:41
@email:  dutzhaoyeyu@163.com
"""

from tensorflow.keras.utils import plot_model
from deepforecast.features import SparseColumn, SequenceColumn
from deepforecast.models.sttf import STTF

attr_feats = ["age", "user", "platform"]
sequence_feats = ["history", "future"]

attr_columns = []
for feat in attr_feats:
    col = SparseColumn(name=feat, vocab_size=10, embed_dim=8)
    attr_columns.append(col)

sequence_columns = []
hist_col = SequenceColumn(name="history", num_seq=5, seq_steps=28, dim=1)
sequence_columns.append(hist_col)
fut_col = SequenceColumn(name="future", num_seq=4, seq_steps=7, dim=1)
sequence_columns.append(fut_col)

model = STTF(attr_columns, sequence_columns, attr_attention_embed_dim=12)
model.summary()
plot_model(model, show_shapes=True)
model.compile(optimizer="rmsprop",
              loss=["mse", "mse"],
              loss_weights=[0.2, 0.8],
              metrics=["mse"])
