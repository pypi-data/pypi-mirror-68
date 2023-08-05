def transpose_without_numpy(matrix):
  import numpy as np
  import copy
  #make a copy of original matrix
  if type(matrix) is np.ndarray:
    copy_m = matrix.copy()
  else:
    copy_m = copy.deepcopy(matrix)
    
  #use basic formula for transpose which is 
  #B_i_j = A_i_j
  for n in range(len(matrix)):
    for n2 in range(len(matrix)):
      copy_m[n][n2] = matrix[n2][n]
  return copy_m
