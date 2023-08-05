def initialize_weights(shape, **kwargs):
  '''
  shape must be a tuple containig rows and column as number
  **kwargs is
  sigma, mean, for standard normal distribution by default it's 1, 0 respectively
  
  random_state = seed parameter
  '''
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
  rows, columns = shape
  weights = sigma * np.random.randn(rows, columns) + mean
  return weights
