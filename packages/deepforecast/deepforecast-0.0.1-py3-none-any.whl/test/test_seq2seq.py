# coding: utf-8
"""
@author: Nelson Zhao
@date:   2020/5/5 9:13 PM
@email:  dutzhaoyeyu@163.com
"""
import pickle
from tensorflow.keras.layers import Input
from tensorflow.keras.models import save_model
from deepforecast.models.seq2seq import seq2seq

# load data
with open("../datasets/encoder_inputs_data", "rb") as f:
    encoder_inputs_data = pickle.load(f)
with open("../datasets/decoder_inputs_data", "rb") as f:
    decoder_inputs_data = pickle.load(f)
with open("../datasets/decoder_outputs_data", "rb") as f:
    decoder_outputs_data = pickle.load(f)


encoder_inputs = Input(shape=(28, 1))
decoder_inputs = Input(shape=(8, 1))
# build model
model = seq2seq(encoder_inputs,
                decoder_inputs,
                encoder_timesteps=28,
                encoder_input_dim=1,
                decoder_timesteps=8,
                decoder_input_dim=1)
model.summary()
model.compile(optimizer="rmsprop", loss="mse", metrics=["mse"])
model.fit(x=[encoder_inputs_data, decoder_inputs_data], y=[decoder_outputs_data], batch_size=64, epochs=10)
# save model
save_model(model, "seq2seq_model.h5")
print("save model successfully!")
# model = load_model("seq2seq_model.h5")
# print("load model successfully!")

