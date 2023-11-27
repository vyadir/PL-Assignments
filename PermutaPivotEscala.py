"""
        Estas funciones llevan a cabo operaciones elementales sobre las filas de una matriz.
"""

def Escalamiento(matrix, k, i):
    if i<=len(matrix) and k!=0:
        for j in range(len(matrix[i-1])): #Toma cada valor de la fila i
            matrix[i-1][j] = k* matrix[i-1][j] #Multiplica el valor por k
    else:
        print('La entrada de la fila es invalida')
    return matrix # Devuelve la matriz ya con el escalamiento

def Permutacion(matrix,i,j):
    if (i and j ) <= len(matrix): # Valida las filas ingresadas
    
        # Guarda los datos de la fila i y cambia los valores de las filas
        auxiliar = matrix[i-1] 
        matrix[i-1]=matrix[j-1] 
        matrix[j-1]=auxiliar 
        
    return matrix # Devuelve la matriz ya con la permutacion

def Pivoteo(matrix,i,k,j):
    if ((i and j ) <= len(matrix) and k!=0): # Valida los valores
        n = len(matrix[i-1])
        if n==len(matrix[j-1]):
            for elemento_n in range(0,n):

                #Toma el elemento de la fila j, lo multiplica por k y lo
                #suma con el elemento de la fila i
                matrix[i-1][elemento_n]=matrix[i-1][elemento_n] + k*matrix[j-1][elemento_n]
    return matrix #Devuelve la matriz con el pivoteo


# Prueba 
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
prueba_escalamiento = Escalamiento(matriz, 100,3)
print(prueba_escalamiento)
prueba_permutacion=Permutacion(matriz, 1, 2) 
print(prueba_permutacion)
prueba_pivoteo=Pivoteo(matriz, 1,10,2)
print(prueba_pivoteo)


"""
    Salida: 

    [[1, 2, 3], [4, 5, 6], [700, 800, 900]]
    [[4, 5, 6], [1, 2, 3], [700, 800, 900]]
    [[14, 25, 36], [1, 2, 3], [700, 800, 900]]
"""