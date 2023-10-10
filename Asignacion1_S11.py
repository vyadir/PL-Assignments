"""
Descripción de la tarea:
        Lleva a cabo operaciones elementales sobre las filas de una matriz
        (deben probarlas, validarlas y documentarlas). Aunque estas operaciones pueden implementarse de 
        manera sencilla con matrices elementales, procuraremos evitar esta aproximación para garantizar la mayor 
        eficiencia computacional posible en las funciones generadas.
        
        Se deben crear tres funciones con los siguientes nombres:
         - Escalamiento(M:matrix (m x n),k:double,i:int)
         - Permutacion(M:matrix (m x n),i:int,j:int)
         - Pivoteo(M:matrix (mxn),i:int,k:double,j:int)
"""
# Matriz ejemplo
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

def Escalamiento(matrix, k, i):
    if i<=len(matrix) and k!=0:
        for j in range(len(matrix[i-1])):
            matrix[i-1][j] = k* matrix[i-1][j]
    else:
        print('La entrada de la fila es invalida')
    return matrix

#prueba_escalamiento = Escalamiento(matriz, 100,3)
#print(prueba_escalamiento)

def Permutacion(matrix,i,j):
    if (i and j ) <= len(matrix):
        auxiliar = matrix[i-1]
        matrix[i-1]=matrix[j-1]
        matrix[j-1]=auxiliar
    return matrix
#prueba_permutacion=Permutacion(matriz, 1, 2) 

#print(prueba_permutacion)
def Pivoteo(matrix,i,k,j):
    if ((i and j ) <= len(matrix) and k!=0):
        n = len(matrix[i-1])
        if n==len(matrix[j-1]):
            for elemento_n in range(0,n):
                matrix[i-1][elemento_n]=matrix[i-1][elemento_n]+k*matrix[j-1][elemento_n]
    return matrix

prueba_pivoteo=Pivoteo(matriz, 1,10,3)
print(prueba_pivoteo)
