def create_empty_matrix(shape = (4, 4)):
  rows = shape[0]
  cols = shape[1]
  matrix = []
  for i in range(rows):
    matrix.append([0 for i in range(cols)])
  return matrix
def transpose_without_numpy(matrix):
  '''it returns transpose of a matrix without any use of numpy'''
  #get shape of matrix
  rows = len(matrix)
  cols = len(matrix[0])
  #create empty matrix with shape = (cols, rows)
  transpose = []
  for i in range(cols):
    transpose.append([0 for j in range(rows)])
  #use basic formula for transpose which is 
  #B_i_j = A_i_j
  for n in range(len(transpose)):
    for n2 in range(len(matrix)):
      transpose[n][n2] = matrix[n2][n]
  return transpose
