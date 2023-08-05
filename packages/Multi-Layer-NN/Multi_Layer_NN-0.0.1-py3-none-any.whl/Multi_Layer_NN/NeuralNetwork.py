#!/usr/bin/env python
# coding: utf-8

# In[1]:
#

import numpy as np
import matplotlib.pyplot as plt



class Multi_Layer_NN:
    """
    A Neural Network that can be either trained on data, 
    or initialized with existing weights.
    
    Parameters
    ----------
    dimensions: dict, a dictionary containing the weight matrices and bias vectors.
    E.g. dimensions = {"W1": [[1, 0.5, 2],[0.25,0.75,1.5]], "b1":[1,2,1]} initializes a one 
    layer perceptron that takes three input elements and has two nodes.
    """
    
    def __init__(self, parameters={}):
        self.parameters = parameters #neural network parameters
        if self.parameters:
            L = len(self.parameters) // 2
            for i in range(1, L):
                W_prev = self.parameters["W" + str(i)]
                b_prev = self.parameters["b" + str(i)]
                W_next = self.parameters["W" + str(i+1)]
                b_next = self.parameters["b" + str(i+1)]
                
                assert(W_prev.shape[0] == b_prev.shape[0]), "Dimensions of the W and b vectors in the {}-th layer do not match!".format(i)
                assert(b_prev.shape[1] == 1),"Dimensions of the b vector in the {}-th layer are not correct!".format(i)
                assert(W_next.shape[1] == W_prev.shape[0]),"Dimensions of the {}-th and {}-th layer do not match!".format(i, i+1)
                
    def init_params(self, hidden_dims, eps=0.01):
        """
        Initializes the weight matrices and bias vectors with appropriate dimensions with 
        random numbers in the intervall [-eps, +eps].
        
        Parameters
        ----------
        hidden_dims: list, contains the dimensions (number of nodes) for each layer.
        E.g. init_params([1,2,1])
        """
        
        #random parameter initialization
        for i in range(1, len(hidden_dims)):
            self.parameters["W" + str(i)] = np.random.randn(hidden_dims[i], hidden_dims[i-1]) * np.sqrt(2/hidden_dims[i-1])
            self.parameters["b" + str(i)] = np.random.randn(hidden_dims[i], 1)

            
                                                            
    def forward_prop_linear(self, A, W, b):
        """ Performs linear forward propagation (without activation function)"""
        Z = np.dot(W, A) + b
        cache = (A, W, b)
        
        return Z, cache
    
    
    def sigmoid(self, Z):
        """
        Sigmoid activation function
        returns the output of the sigmoid function and the input aswell (needed for backpropagation)
        """
    
        A = 1/(1 + np.exp(-Z))
        cache = Z
        
        return A, cache
    
    
    def relu(self, Z):
        """
        ReLu activation function
        returns output of the ReLu function and the input aswell (needed for backpropagation)
        """
        
        A = np.maximum(0, Z)
        cache = Z
        
        return A, cache
    
    
    def sigmoid_backward(self, dA, cache):
        """backward propagation for the sigmoid activation function"""
        Z = cache
        dZ = dA * self.sigmoid(Z)[0] * (1 - self.sigmoid(Z)[0])
        
        return dZ
    
    
    def relu_backward(self, dA, cache):
        """backward propagation for the ReLu activation function"""
        Z = cache
        dZ = np.array(dA, copy = True)
        dZ[Z<=0] = 0
        
        return dZ
    
    
    def forward_prop_activation(self, A_prev, W, b, activation = "relu"):
        """Performs linear forward propagation (with activation function)"""
        
        if activation == "sigmoid":
            Z, linear_cache = self.forward_prop_linear(A_prev, W, b)
            A, activation_cache = self.sigmoid(Z)
            cache = (linear_cache, activation_cache)
            
        elif activation == "relu":
            Z, linear_cache = self.forward_prop_linear(A_prev, W, b)
            A, activation_cache = self.relu(Z)
            cache = (linear_cache, activation_cache)
        
        return A, cache
    
    
    def total_forward(self, X):
        """Forward propagation through the whole network"""
        caches = []
        A = X
        L = len(self.parameters)//2 #total number of layers
        
        for i in range(1, L):
            A_prev = A
            A, cache = self.forward_prop_activation(A_prev, self.parameters["W" + str(i)], self.parameters["b" + str(i)], activation = "relu")
            caches.append(cache)
            
        AL, cache = self.forward_prop_activation(A, self.parameters['W' + str(L)], self.parameters['b' + str(L)], activation = "sigmoid")
        caches.append(cache)
        
        return AL, caches
    
    
    def compute_cost(self, AL, Y, lambd):
        """total cost of the batch"""
        m = Y.shape[1]#number of samples in the batch
        
        #cost = -1 / m * np.sum(Y * np.log(AL) + (1-Y) * np.log(1-AL))
        L = len(self.parameters) // 2
        L2_regularization_cost = 0
        for i in range(1, L + 1):
                W = self.parameters["W" + str(i)]
                L2_regularization_cost += np.sum(W**2)
        
        L2_regularization_cost *= (1/m) * (lambd/2)
        cross_entropy_cost = (1/m) * (-np.dot(Y,np.log(AL).T) - np.dot(1-Y, np.log(1-AL).T))
        cost = np.squeeze(L2_regularization_cost + cross_entropy_cost) 

        return cost
    
    
    def back_prop_linear(self, dZ, cache, lambd):
        """back propagation without activation"""
        A_prev, W, b = cache
        m = A_prev.shape[1] #number of samples in the batch


        dW = 1 / m * np.dot(dZ, A_prev.T) + lambd / m * W
        db = 1 / m * np.sum(dZ, axis=1, keepdims=True)
        dA_prev = np.dot(W.T, dZ)

        return dA_prev, dW, db
    
    
    def back_prop_activation(self, dA, cache, activation, lambd):
        """back propagation with activation"""
        linear_cache, activation_cache = cache

        if activation == "relu":
            dZ = self.relu_backward(dA, activation_cache)
            dA_prev, dW, db = self.back_prop_linear(dZ, linear_cache, lambd)


        elif activation == "sigmoid":
            dZ = self.sigmoid_backward(dA, activation_cache)
            dA_prev, dW, db = self.back_prop_linear(dZ, linear_cache, lambd)

        return dA_prev, dW, db
    
    
    def total_backprop(self, AL, Y, caches, lambd):
        """back propagation through the entire neural network"""
        
        grads = {} #dictionary containing the gradient values for the parameters
        L = len(caches)
        m = AL.shape[1] #number of samples in the batch
        Y = Y.reshape(AL.shape)

        dAL = - (np.divide(Y, AL) - np.divide(1 - Y, 1 - AL))

        current_cache = caches[L-1]
        grads["dA" + str(L-1)], grads["dW" + str(L)], grads["db" + str(L)] = self.back_prop_activation(dAL, current_cache, 'sigmoid', lambd)

        for l in reversed(range(L-1)):

            current_cache = caches[l]
            dA_prev_temp, dW_temp, db_temp = self.back_prop_activation(grads["dA" + str(l + 1)], current_cache, 'relu', lambd)
            grads["dA" + str(l)] = dA_prev_temp
            grads["dW" + str(l + 1)] = dW_temp
            grads["db" + str(l + 1)] = db_temp


        return grads
        
        
    def update_parameters(self, grads, learning_rate, optimization, beta1, beta2, v , s , t ):
        """updates the parameters"""
        
        L = len(self.parameters) // 2 
        
        if optimization == "gd":
            
            for l in range(0, L):
                self.parameters["W" + str(l+1)] = self.parameters["W" + str(l+1)] - learning_rate * grads["dW" + str(l+1)]
                self.parameters["b" + str(l+1)] = self.parameters["b" + str(l+1)] - learning_rate * grads["db" + str(l+1)]
                
            return 0, 0 #arbitrary placeholders
            
        elif optimization == "momentum":
            v = self.initialize_velocity()
            self.update_parameters_with_momentum(grads, v, beta1, learning_rate, s)
                
            return v, 0 #arbitrary placeholder
                
        elif optimization == "adam":
            v, s = self.initialize_adam()
            self.update_parameters_with_adam(grads, v, s, t ,learning_rate,
                                beta1, beta2)
            return v, s

        
    def train_model(self, X, Y, learning_rate = 0.0075, epochs = 1000, lambd = 0.1, batch_size = 64, optimization = "gd",
                    beta1 = 0.9, beta2 = 0.999, print_cost = False, plot = False):
        """Trains the model on the training data X and the labels Y"""
        
        if optimization == "momentum":
            v = self.initialize_velocity()
            s = 0
            
        elif optimization == "adam":
            v, s = self.initialize_adam()
            
        else:
            v, s = 0, 0
            
        costs = []                     

        # Loop (gradient descent)
        for i in range(0, epochs): #iterate over epochs
            batch = self.random_mini_batches(X, Y, mini_batch_size = batch_size)
            #first dimension of batch specifies the specific batch, second dimension specifies X and Y
            for j in range(0, len(batch)): #iterate over mini batches
                X_batch = batch[j][0]
                Y_batch = batch[j][1]
                # Forward propagation: [LINEAR -> RELU]*(L-1) -> LINEAR -> SIGMOID.
                AL, caches = self.total_forward(X_batch)

                cost = self.compute_cost(AL, Y_batch, lambd)
                grads = self.total_backprop(AL, Y_batch, caches, lambd)
                
                v, s =  self.update_parameters(grads, learning_rate, optimization, beta1, beta2, v, s, i+10)
            
            
            # Print the cost every 100th training example
            if print_cost and i % 100 == 0:
                print ("Cost after iteration %i: %f" %(i, cost))
            if print_cost and i % 100 == 0:
                costs.append(cost)

        if plot:
            plt.plot(np.squeeze(costs))
            plt.ylabel('cost')
            plt.xlabel('iterations (per tens)')
            plt.title("Learning rate =" + str(learning_rate))
            plt.show()


    def predict(self, X, Y, print_acc = False):
        """
        Predicts the outcome of feature vectors using the trained Neural Network model.

        Arguments:
        X: input feature vectors

        Returns:
        p: predictions for the given feature vectors
        """

        m = X.shape[1]
        n = len(self.parameters) // 2 # number of layers in the neural network
        p = np.zeros((1,m))

        # Forward propagation
        probas, caches = self.total_forward(X)


        # convert probas to 0/1 predictions
        for i in range(0, probas.shape[1]):
            if probas[0,i] > 0.5:
                p[0,i] = 1
            else:
                p[0,i] = 0

        if print_acc:
            print("Accuracy: "  + str(np.sum((p == Y)/m)))

        return p[0]
    
    
    def random_mini_batches(self, X, Y, mini_batch_size):
        """
        Creates a list of random minibatches from (X, Y)

        """

        m = X.shape[1] # total number of training examples in one epoch
        mini_batches = []

        # Shuffle (X, Y)
        permutation = list(np.random.permutation(m))
        shuffled_X = X[:, permutation]
        shuffled_Y = Y[:, permutation].reshape((1,m))

        # Partition (shuffled_X, shuffled_Y)
        num_complete_minibatches = m // mini_batch_size # number of mini batches of size mini_batch_size
        for k in range(0, num_complete_minibatches):

            mini_batch_X = shuffled_X[:, k*mini_batch_size : (k+1)*mini_batch_size]
            mini_batch_Y = shuffled_Y[:, k*mini_batch_size : (k+1)*mini_batch_size]

            mini_batch = (mini_batch_X, mini_batch_Y)
            mini_batches.append(mini_batch)

        # Handling the case that the number of mini batches is not a power of 2
        if m % mini_batch_size != 0:

            mini_batch_X = shuffled_X[:,num_complete_minibatches * mini_batch_size:]
            mini_batch_Y = shuffled_Y[:,num_complete_minibatches * mini_batch_size:]

            mini_batch = (mini_batch_X, mini_batch_Y)
            mini_batches.append(mini_batch)

        return mini_batches
    
    
    def initialize_velocity(self):
        """
        Initializes the velocity as a python dictionary
        
        """

        L = len(self.parameters) // 2 # number of layers
        v = {}

        # Initialize velocity
        for l in range(L):
            v["dW" + str(l+1)] = np.zeros_like(self.parameters['W' + str(l+1)])
            v["db" + str(l+1)] = np.zeros_like(self.parameters['b' + str(l+1)])

        return v

    def update_parameters_with_momentum(self, grads, v, beta, learning_rate, s):
        """
        Update parameters using Momentum
        
        """

        L = len(self.parameters) // 2 # number of layers 
        
        # Momentum update for each parameter
        for l in range(L):

            # compute velocities
            v["dW" + str(l+1)] = beta * v["dW" + str(l+1)] + (1-beta) * grads['dW' + str(l+1)]
            v["db" + str(l+1)] = beta * v["db" + str(l+1)] + (1-beta) * grads['db' + str(l+1)]
            # update parameters
            self.parameters["W" + str(l+1)] = self.parameters["W" + str(l+1)] - learning_rate * v['dW' + str(l+1)]
            self.parameters["b" + str(l+1)] = self.parameters["b" + str(l+1)] - learning_rate * v['db' + str(l+1)]

        return v
    
    def initialize_adam(self) :
        """
        Initializes v and s as two python dictionaries with

        """

        L = len(self.parameters) // 2 # number of layers 
        v = {}
        s = {}

        # Initialize v, s. Input: "parameters". Outputs: "v, s".
        for l in range(L):
            v["dW" + str(l + 1)] = np.zeros_like(self.parameters["W" + str(l + 1)])
            v["db" + str(l + 1)] = np.zeros_like(self.parameters["b" + str(l + 1)])
            s["dW" + str(l+1)] = np.zeros_like(self.parameters["W" + str(l + 1)])
            s["db" + str(l+1)] = np.zeros_like(self.parameters["b" + str(l + 1)])

        return v, s
    
    def update_parameters_with_adam(self, grads, v, s, t = 0, learning_rate = 0.01,
                                beta1 = 0.9, beta2 = 0.999,  epsilon = 1e-8):
        """
        Update parameters using Adaptive Momentum Optimization

        """

        L = len(self.parameters) // 2                 # number of layers
        v_corrected = {}                         # Initializing first moment estimate, python dictionary
        s_corrected = {}                         # Initializing second moment estimate, python dictionary

        # Perform Adam update on all parameters
        for l in range(L):
            # Moving average of the gradients. Inputs: "v, grads, beta1". Output: "v".
            v["dW" + str(l + 1)] = beta1 * v["dW" + str(l + 1)] + (1 - beta1) * grads['dW' + str(l + 1)]
            v["db" + str(l + 1)] = beta1 * v["db" + str(l + 1)] + (1 - beta1) * grads['db' + str(l + 1)]

            # Compute bias-corrected first moment estimate. Inputs: "v, beta1, t". Output: "v_corrected".
            v_corrected["dW" + str(l + 1)] = v["dW" + str(l + 1)] / (1 - beta1**t)
            v_corrected["db" + str(l + 1)] = v["db" + str(l + 1)] / (1 - beta1**t)

            # Moving average of the squared gradients. Inputs: "s, grads, beta2". Output: "s".
            s["dW" + str(l + 1)] = beta2 * s["dW" + str(l + 1)] + (1 - beta2) * grads['dW' + str(l + 1)]**2
            s["db" + str(l + 1)] = beta2 * s["db" + str(l + 1)] + (1 - beta2) * grads['db' + str(l + 1)]**2

            # Compute bias-corrected second raw moment estimate. Inputs: "s, beta2, t". Output: "s_corrected".
            s_corrected["dW" + str(l + 1)] = s["dW" + str(l + 1)] / (1 - beta2**t)
            s_corrected["db" + str(l + 1)] = s["db" + str(l + 1)] / (1 - beta2**t)

            # Update parameters. Inputs: "parameters, learning_rate, v_corrected, s_corrected, epsilon". Output: "parameters".
            self.parameters["W" + str(l + 1)] = self.parameters["W" + str(l + 1)] - learning_rate * v_corrected["dW" + str(l + 1)] / (np.sqrt(s_corrected["dW" + str(l + 1)]) + epsilon)
            self.parameters["b" + str(l + 1)] = self.parameters["b" + str(l + 1)] - learning_rate * v_corrected["db" + str(l + 1)] / (np.sqrt(s_corrected["db" + str(l + 1)]) + epsilon)

        return v, s




