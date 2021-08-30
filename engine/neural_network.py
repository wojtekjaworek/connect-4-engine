import tensorflow as tf
import numpy as np
from numpy.lib.utils import who
from engine.env import Env
import copy
import random
import time


class NeuralNetwork():

    def __init__(self, batch_size, learning_rate, epochs, network_path=None):
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.epochs = epochs
        

        if network_path is None:
            self.init_network()
        else:
            self.model = 2# load model
            None # TODO: handle linking existing network 


    def init_network(self):

        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.Input(shape=(42,)))
        self.model.add(tf.keras.layers.Dense(42, activation='relu'))
        self.model.add(tf.keras.layers.Dense(7, activation='softmax'))
        self.model.compile(loss='caterogical_crossentrophy', optimizer='rmsprop', metrics=['accuracy'])


    def train(self, training_data):
        
        return None


    def save_model(self):
        time_string = time.strftime("%m-%d-%Y_%H-%M-%S", time.localtime())

        self.model.save('models/model_'+time_string)