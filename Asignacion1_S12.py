"""
    Creado por Yadir Vega
    Descripción: 

            Programar en python el algoritmo de simplex. Para esto suponga que recibe una matriz T de tamaño m x n
            que representa la tabla inicial del simplex ya dada en forma estándar canónica. Deberá conseguir la tabla final de simplex.

            Una vez logrado, modifica la función para generar otra función que realice
            la primera fase para programas ampliados. En ese caso, se deberá recibir la
            tabla ampliada y realizar el trabajo de optimización de la función auxiliar o
            función de penalización.

            Al final, de encontrar solución, esta segunda función retornará una nueva tabla
            para el programa original, eliminado las variables artificiales y la función de
            penalización, de manera que pueda ser resuelto por la primera función realizada.

    Las funciones permutación, escalamiento y pivoteo fueron las creadas en semana 11, que las integro para ir reciclando código.

"""

# Permuta dos filas en una matriz.
def Permutacion(matrix, i, j):
    # Comprueba que las filas dadas existen en la matriz.
    if (i and j) <= len(matrix):
        auxiliar = matrix[i - 1]  # Almacena temporalmente una fila.
        matrix[i - 1] = matrix[j - 1]  # Intercambia las filas.
        matrix[j - 1] = auxiliar
    return matrix

# Escala una fila de la matriz por un factor.
def Escalamiento(matrix, k, i):
    # Verifica que la fila dada exista y que el factor no sea 0.
    if i <= len(matrix) and k != 0:
        for j in range(len(matrix[i-1])):
            matrix[i-1][j] *= k
    else:
        print('La entrada de la fila es invalida')
    return matrix

# Agrega un múltiplo de una fila a otra fila en la matriz.
def Pivoteo(matrix, i, k, j):
    # Verifica que las filas dadas existan y que el factor no sea 0.
    if (i and j) <= len(matrix) and k != 0:
        n = len(matrix[i-1])
        # Asegura que ambas filas tengan la misma longitud.
        if n == len(matrix[j-1]):
            for elemento_n in range(n):
                matrix[i-1][elemento_n] += k * matrix[j-1][elemento_n]
    return matrix

# Implementación del método Simplex.
def simplex(T):
    # Obtiene las dimensiones de la tabla.
    m, n = len(T), len(T[0])
    # Mientras haya coeficientes negativos en la función objetivo.
    while any(x < 0 for x in T[-1][:-1]):
        # Encuentra la columna pivote.
        col_pivote = T[-1].index(min(T[-1][:-1]))
        # Calcula la fila pivote basada en las restricciones.
        if all(x <= 0 for x in [row[col_pivote] for row in T[:-1]]):
            raise ValueError("El problema no tiene solución óptima finita.")
        ratios = [row[-1] / row[col_pivote] if row[col_pivote] > 0 else float('inf') for row in T[:-1]]
        fila_pivote = ratios.index(min(ratios))
        # Realiza operaciones de fila para hacer el elemento pivote 1 y otros elementos en esa columna 0.
        pivot_val = T[fila_pivote][col_pivote]
        T[fila_pivote] = [x / pivot_val for x in T[fila_pivote]]
        for i in range(m):
            if i != fila_pivote:
                factor = T[i][col_pivote]
                T[i] = [x - factor * y for x, y in zip(T[i], T[fila_pivote])]
                
    return T

# Realiza una primera fase para manejar variables artificiales.
def primera_fase(tabla):
    m, n = len(tabla), len(tabla[0])
    # Número de variables artificiales.
    num_vars_artificiales = m - 1
    # Crea una fila de penalización para las variables artificiales.
    fila_penalizacion = [-1 if i < n - 1 - num_vars_artificiales else 0 for i in range(n)]
    tabla.insert(m - 1, fila_penalizacion)
    try:
        tabla = simplex(tabla)
    except Exception as e:
        raise ValueError(f"Error durante la primera fase del Simplex: {e}")
    # Si el valor en la fila de penalización no es 0, no hay solución factible.
    if tabla[-2][-1] != 0:
        return None
    # Elimina la fila de penalización y las variables artificiales.
    tabla.pop(-2)
    for i in range(m - 1):
        del tabla[i][-2-num_vars_artificiales:-2]
    del tabla[-1][-2-num_vars_artificiales:-2]
    return tabla

# Función principal para resolver la tabla Simplex.
def resolver(tabla):
    try:
        result = simplex(tabla)
        return result
    except ValueError as e:
        return str(e)

# Caso de prueba.
matriz_prueba = [
    [2, 1, 1, 0, 0, 0, 6],
    [2, 1, 0, 1, 0, 0, 6],
    [1, 2, 0, 0, 1, 0, 6],
    [-4, -3, 0, 0, 0, 1, 0]
]

# Ejecución principal.
if __name__ == '__main__':
    solucion = resolver(matriz_prueba)
    # Muestra la solución o el error.
    if isinstance(solucion, list):
        for fila in solucion:
            print(fila)
    else:
        print(solucion)
