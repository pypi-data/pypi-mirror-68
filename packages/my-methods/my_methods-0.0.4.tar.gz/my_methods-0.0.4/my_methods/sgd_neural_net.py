class SGDNeuralNet:
  import numpy as np
  def __init__(self):
    self.total_error = 0
    self.dense_layers = {}
    self.n_dense_layers = 0
  
  #define relu function for +ve real numbers
  def relu(self, outputs):
    import numpy as np
    return np.maximum(0, outputs)# returns outputs if outputs > 0
                       # return 0 otherwise
  #relu derivative
  def relu2deriv(self, output):
    return output > 0 # returns 1 for outputs > 0
                    # return 0 otherwise
  
  #define sigmoid function for outputs in terms of probability
  def sigmoid(self, outputs):
    import numpy as np
    return 1/(1 + np.exp(-outputs))
  
  '''def initialize_weights(self, shape, **kwargs):
    import numpy as np
    mean = kwargs.get('mean')
    sigma = kwargs.get('sigma')
    random_state = kwargs.get('random_state')
    if not mean:
      mean = 0
    if not sigma:
      sigma = 1
    if random_state:
      np.random.seed(random_state)
    rows, cols = shape
    return sigma * np.random.randn(rows, cols) + mean'''
  def initialize_weights(self, shape, **kwargs):
    import numpy as np
    sigma = kwargs.get('sigma')
    mean = kwargs.get('mean')
    random_state = kwargs.get('random_state')
    if random_state:
      np.random.seed(random_state)
    if not mean:
      mean = 1
    if not sigma:
      sigma = 2
    return sigma *np.random.random(shape) - mean
  
  def dense_layer(self, hidden_nodes, activation = None):
    self.n_dense_layers += 1
    layer_name ='_' + str(self.n_dense_layers)
    self.dense_layers['hidden_nodes' + layer_name] = hidden_nodes
    self.dense_layers['activation' + layer_name] = activation
    
  
  #fit neural_net
  def fit(self, X, y, epochs = 100, alpha = .01,n_percent = 10, **kwargs):
    import numpy as np
    assert(X.ndim == 2)
    assert(y.ndim == 2)
    if not (y.shape[1] == 1 and y.shape[0] >= y.shape[1]):
      raise TypeError('dependent variable must be a row vector')
      
    rows, cols = X.shape
    features = cols
    n = 1
    self.layers_identity = {}
    n_features = features
    #initialize weights
    while n <= self.n_dense_layers:
      hidden_nodes = self.dense_layers['hidden_nodes' + '_' + str(n)]
      name = '_' + str(n)
      self.layers_identity['weights' + name] = self.initialize_weights((n_features, hidden_nodes), **kwargs)
      self.layers_identity['activation' + name] = self.dense_layers.get('activation' + name)
      n_features = self.dense_layers.get('hidden_nodes' + name)
      n += 1
    for epoch in range(epochs):
      self.total_error = 0
      for sample in range(len(X)):
        x = X[sample:sample+1, :]
        target = y[sample:sample +1, :]
        n = 1
        input = x
        self.layer_wise_input = {}
        self.layer_wise_output = {}
        while n <= self.n_dense_layers:
          name = '_' + str(n)
          self.layer_wise_input['layer' + name] = input
          output = input @ self.layers_identity['weights' + name]
          if self.layers_identity['activation' + name] == 'relu':
            output = self.relu(output)
          if self.layers_identity['activation' + name] == None:
            output = output
          self.layer_wise_output['layer' + name] = output
          input = output
          n += 1
        error = (output - target)**2
        self.total_error += error
        delta = output - target
        self.weight_deltas = {}
        n = 1
        while n <= self.n_dense_layers:
          name = '_' + str(n)
          self.weight_deltas['weight_delta' + name] = delta*self.layer_wise_input['layer' + name].T 
          if self.layers_identity['activation'  + name] == 'relu':
            deriv = self.relu2deriv(self.layer_wise_output['layer' + name])
          else:
            deriv = 1
          self.layers_identity['weights' + name] -= self.weight_deltas['weight_delta' + name]*alpha*deriv
          n += 1
      if (epoch + 1) % n_percent == 0:
        print(f'Iteration no. {epoch + 1} / {epochs}, error is {np.sum(self.total_error)}')
      
  def predict(self, X):
    import numpy as np
    '''X must be a 2 d array'''
    input = X
    n = 1
    while n <= self.n_dense_layers:
      name = '_' + str(n)
      out = input @ self.layers_identity['weights' + name]
      activation = self.layers_identity['activation' + name]
      if activation == 'relu':
        out = self.relu(out)
      if activation == None:
        out = out

      input = out
      n += 1
    return out
  def score(self, X, y):
    import numpy as np
    output = self.predict(X)
    from sklearn.metrics import r2_score
    return r2_score(y, output)
  
  #error function
  def error(self, X, y):
    import numpy as np
    output = self.predict(X)
    return np.sum((output - y))
    
  #sum of squared_error
  def mean_squared_error(self, X, y):
    import numpy as np
    output = self.predict(X)
    from sklearn.metrics import mean_squared_error
    return mean_squared_error(y, output)
    
