import tensorflow as tf
import numpy as np
from engine.env import Env
import copy
import random
import time


class NeuralNetwork():

    def __init__(self, batch_size=256, learning_rate=0.1, epochs=10, network_path=None):
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
        self.model.add(tf.keras.layers.Dense(42, input_shape=(42,), activation='relu'))
        self.model.add(tf.keras.layers.Dense(7, activation='softmax'))
        self.model.compile(loss='caterogical_crossentrophy', optimizer='rmsprop', metrics=['accuracy'])


    def train(self, training_data):
        # normalize input shape:
        for game in training_data:
            for g in game:
                g[0] = np.reshape(g[0], 42)  

        input_states = []
        rewards = []
        who_to_move = []
        for game in training_data: # NN train one game at time
            for g in game: # we take every state after move
                if g[1] == 1: # normalize input states and rewards
                    input_states.append(g[0])
                    who_to_move.append(g[1])
                    rewards.append(g[2]) # g[2] is reward !!!  g[1] is who to move
                else:
                    input_states.append(np.multiply(g[0], -1))
                    who_to_move.append(g[1] * -1)
                    rewards.append(g[2] * -1)
                print('input states: ', input_states) # it works


        return None


    def predict(self, game_env: Env):
        
        input = np.reshape(game_env.board.board, 42)
        print('reshaped: ', input)
        # return self.model.predict(game_env.board.board)
        return None


    def save_model(self):
        time_string = time.strftime("%m-%d-%Y_%H-%M-%S", time.localtime())

        self.model.save('models/model_'+time_string)