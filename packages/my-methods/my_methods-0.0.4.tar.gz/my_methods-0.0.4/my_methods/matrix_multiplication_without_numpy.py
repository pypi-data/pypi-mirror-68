def assert_matrix(b):
  #check if all lists of list have same number of elements, all are integers
  n = 0
  while n < len(b) - 1:
    if type(b[n]) is list and type(b[n + 1]) is list:
      #check if lists of list is equal for all
      if len(b[n]) == len(b[n + 1]):
          n += 1
          continue
      else:
        raise ValueError('lists of lists doesn\'t have same number of items')
    #check if it is integers
    elif type(b[n] is int) and type(b[n + 1]) is int:
      n += 1
      continue
    else:
      raise TypeError('items in list must be integers and must have same type')

#transpose of a matrix
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

def matrix_mul(a, b):
  assert_matrix(a)
  assert_matrix(b)
  shape_a = (len(a), len(a[0]))
  shape_b = (len(b), len(b[0]))
  out_shape = (shape_a[0], shape_b[1])
  #if type of elemennts in list is also a list
  if type(b[0]) is list and type(a[0]) is list:
    #check if columns of a are equal to rows of b
    if shape_a[1] == shape_b[0]:
      #create an empty list to append elements
      f_list = []
      for n1, i in enumerate(a):
        f = []
        for n2 in range(len(b[0])):
          s = 0 #intialize sum of multiplications
          for n3, j in enumerate(i):
            s += j * b[n3][n2]
          f.append(s)
        f_list.append(f)
      shape_f = (len(f_list), len(f_list[0]))
      return f_list
    else:
      raise ValueError(f'Can\'t multiply diffrent dimensions matrix no. of columns of {a} must be equal to no. of rows of {b}')
    #b = transpose(b)
  if type(b[0]) is int and type(a[0]) is int:
    #assert the length of both matrces
    if len(a) == 1 and len(b) == 1:
      return [a[0] * b[0]]
    else:
      raise ValueError(f'Can\'t multiply diffrent dimensions matrix no. of columns of {a} must be equal to no. of rows of {b}')
  else:
    raise ValueError(f'matrices {a} and {b} deosn\'t have same type of elements')
