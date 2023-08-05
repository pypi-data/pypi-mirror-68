def transpose_without_numpy(matrix):
  import numpy as np
  #make a copy of original matrix
  if type(copy) is np.ndarray:
    copy = matrix.copy()
  else:
    copy = matrix
    
  #use basic formula for transpose which is 
  #B_i_j = A_i_j
  for n in range(len(matrix)):
    for n2 in range(len(matrix)):
      copy[n][n2] = matrix[n2][n]
  return copy
