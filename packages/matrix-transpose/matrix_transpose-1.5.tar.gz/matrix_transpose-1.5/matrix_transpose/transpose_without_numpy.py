def transpose_without_numpy(matrix):
  import numpy as np
  #make a copy of original matrix
  if type(matrix) is np.ndarray:
    copy = matrix.copy()
  else:
    import copy
    copy_m = copy.deepcopy(matrix)
    
  #use basic formula for transpose which is 
  #B_i_j = A_j_i
  for n1 in range(len(matrix)):
    for n2 in range(len(matrix[0])):
      copy_m[n1][n2] = matrix[n2][n1]
  return copy_m
