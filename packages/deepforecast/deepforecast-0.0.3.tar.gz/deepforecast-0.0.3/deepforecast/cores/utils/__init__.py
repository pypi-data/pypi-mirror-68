# coding: utf-8
"""
@author: Nelson Zhao
@date:   2020/5/5 9:44 PM
@email:  dutzhaoyeyu@163.com
"""
from tensorflow.keras import models
from deepforecast.layers import custom_objects


def save_model(obj, filepath):
    models.save_model(obj, filepath)


def load_model(filepath):
    model = models.load_model(filepath, custom_objects)
    return model
