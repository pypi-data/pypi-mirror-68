# coding: utf-8
"""
@author: Nelson 
@date:   2020-05-02 12:30
@email:  
"""
from .seq2seq import Encoder, Decoder

custom_objects = {
    "Encoder": Encoder,
    "Decoder": Decoder
}