'''
action in this game can be divide into 2 parts:
    1. do notion,
    2. long tap for n seconds,where n: 0<n<max, if n > max , game would be over.
For long tap, divide n seconds into m actions, the stride of time is n/m. So the final layer would have
m units standing for m action.
'''
import tensorflow as tf
import numpy as np
import random
from collections import deque

# Hyper Parameters
FRAME_PER_ACTION = 1
OBSERBR = 1 # timesteps to observr before training
EXPLORE = 200000 # frame over which to anneal epsion
FINAL_EPSILON = 0
INITIAL_EPSILON = 0
REPLAY_MEMORY = 50000
BATCH_SIZE = 32

class BrainDQN:
    def __init__(self,actions):
        # init replay memory
        self.replayMemory = deque()
        # init some paprameter
        self.timeStep = 0
        self.actions = actions
        # init Q network
        self.createQNetwork()

    def createQNetwork(self):
        # network weights
        #input: batch_size x 
        W_conv1 = self.weight_variable([8,8,4,32])
        b_conv1 = self.bias_variable([32])

        W_conv2 = self.weight_variable([4,4,32,64])
        b_conv2 = self.weight_variable([64])

        W_conv3 = self.weight_variable([3,3,64,64])
        b_conv3 = self.bias_variable([64])

        W_fc1 = self.weight_variable([])

    def weight_variable(self,shape):
        initial = tf.truncated_normal(shape,stddev=0.01)
        return tf.Variable(initial,dtype=tf.float32)

    def bias_variable(self,shape):
        initial = tf.truncated_normal(shape,stddev=0.01)
        return tf.Variable(initial)

    def conv2d(self,x,W,stride):
        return tf.nn.conv2d(x,W,strides=[1,stride,stride,1],padding="SAME")

    def max_pool_2x2(self,x):
        return tf.nn.max_pool(x,ksize=[1,2,2,1],strides="SAME")
