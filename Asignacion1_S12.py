"""
    Creado por Yadir Vega
    Descripción: 

            Programar en python el algoritmo de simplex. Para esto suponga que recibe una matriz T de tamaño m x n
            que representa la tabla inicial del simplex ya dada en forma estándar canónica. Deberá conseguir la 
            tabla final de simplex.

            Una vez logrado, modifica la función para generar otra función que realice
            la primera fase para programas ampliados. En ese caso, se deberá recibir la
            tabla ampliada y realizar el trabajo de optimización de la función auxiliar o
            función de penalización.

            Al final, de encontrar solución, esta segunda función retornará una nueva tabla
            para el programa original, eliminado las variables artificiales y la función de
            penalización, de manera que pueda ser resuelto por la primera función realizada.

    Las funciones Permutacion, Escalamiento y Pivoteo fueron las creadas en semana 11, que las integro para ir reciclando código.

"""

# Función que intercambia dos filas en una matriz.
def Permutacion(matriz, i, j):
    # Verifica si las filas dadas están dentro del rango de la matriz.
    if (i and j) <= len(matriz):
        auxiliar = matriz[i - 1]  # Guarda temporalmente la fila i.
        matriz[i - 1] = matriz[j - 1]  # Sustituye la fila i por la fila j.
        matriz[j - 1] = auxiliar  # Sustituye la fila j con la fila i original (guardada en auxiliar).
    return matriz

# Función que multiplica una fila de la matriz por un factor k.
def Escalamiento(matriz, k, i):
    # Verifica que la fila dada exista y que el factor no sea 0.
    if i <= len(matriz) and k != 0:
        for j in range(len(matriz[i-1])):
            matriz[i-1][j] *= k  # Multiplica cada elemento de la fila por k.
    else:
        print('La entrada de la fila es invalida')  # Mensaje de error.
    return matriz

# Función que suma un múltiplo k de la fila j a la fila i.
def Pivoteo(matriz, i, k, j):
    # Verifica que las filas dadas existan y que el factor no sea 0.
    if (i and j) <= len(matriz) and k != 0:
        n = len(matriz[i-1])  # Longitud de la fila i.
        # Verifica que ambas filas tengan la misma longitud.
        if n == len(matriz[j-1]):
            for elemento_n in range(n):
                matriz[i-1][elemento_n] += k * matriz[j-1][elemento_n]  # Suma k veces la fila j a la fila i.
    return matriz

# Función que implementa el algoritmo de simplex.
def algoritmo_simplex(T):
    m, n = len(T), len(T[0])  # Dimensiones de la matriz.
    # Mientras haya valores negativos en la fila de la función objetivo.
    while any(x < 0 for x in T[-1][:-1]):
        columna_pivote = T[-1].index(min(T[-1][:-1]))  # Encuentra la columna con el valor más negativo.
        # Si todos los valores de la columna pivote son no positivos, el problema no tiene solución finita.
        if all(x <= 0 for x in [fila[columna_pivote] for fila in T[:-1]]):
            raise ValueError("El problema no tiene solución óptima finita.")
        # Calcula las proporciones para determinar la fila pivote.
        proporciones = [fila[-1] / fila[columna_pivote] if fila[columna_pivote] > 0 else float('inf') for fila in T[:-1]]
        fila_pivote = proporciones.index(min(proporciones))
        # Normaliza la fila pivote.
        valor_pivote = T[fila_pivote][columna_pivote]
        T[fila_pivote] = [x / valor_pivote for x in T[fila_pivote]]
        # Hace cero los demás valores de la columna pivote.
        for i in range(m):
            if i != fila_pivote:
                factor = T[i][columna_pivote]
                T[i] = [x - factor * y for x, y in zip(T[i], T[fila_pivote])]
    return T

# Función que maneja la primera fase del simplex para tratar con variables artificiales.
def fase_inicial(tabla):
    m, n = len(tabla), len(tabla[0])  # Dimensiones de la matriz.
    numero_vars_artificiales = m - 1  # Número de variables artificiales necesarias.
    # Crea una fila de penalización.
    fila_penalizacion = [-1 if i < n - 1 - numero_vars_artificiales else 0 for i in range(n)]
    tabla.insert(m - 1, fila_penalizacion)
    # Resuelve el problema de optimización con la función de penalización.
    try:
        tabla = algoritmo_simplex(tabla)
    except Exception as e:
        raise ValueError(f"Error durante la primera fase del Simplex: {e}")
    # Si el valor en la fila de penalización no es 0, el problema original no tiene solución factible.
    if tabla[-2][-1] != 0:
        return None
    # Elimina la fila de penalización y las variables artificiales.
    tabla.pop(-2)
    for i in range(m - 1):
        del tabla[i][-2-numero_vars_artificiales:-2]
    del tabla[-1][-2-numero_vars_artificiales:-2]
    return tabla

# Función principal que resuelve el problema de optimización.
def resolver_simplex(tabla):
    try:
        resultado = algoritmo_simplex(tabla)  # Resuelve el problema usando el algoritmo de simplex.
        return resultado
    except ValueError as e:  # Captura errores durante la ejecución del algoritmo.
        return str(e)

# Punto de entrada del programa.
if __name__ == '__main__':
    # Define una matriz con un ejercicio que requiere variables artificiales
    matriz_prueba = [[2, 1, 1, 0, 0, 18], [2, 3, 0, 1, 0, 42], [3, -2, 0, 0, 1, 5], [-3, -2, 0, 0, 0, 0]]
    #[[2, 5, 1, 0, 0, 0, 35], [-3, 2, 0, -1, 0, 1, -18], [2, 4, 0, 0, 1, 0, 26], [-3, -2, 0, 0, 0, 0, 0], [3, -2, 0, 1, 0, 0, 18]]
    #[[1, 1, -1, 0, 0, 5],[2, 3, 0, 1, 0, 12],[0, 1, 0, 0, 1, 3],[-2, -3, 0, 0, 0, 0],[0, 0, 0, 0, -1, -3]]
    # Define una matriz con un ejercicio que NO requiere variables artificiales
    matriz_prueba2  = [[2, 1, 1, 0, 18],[2, 3, 0, 1, 42],[-3, -1, 0, 0, 0]]
    
    # Ejecuta la primera fase del Simplex.
    matriz_transformada = fase_inicial(matriz_prueba)
    
    #print('Para el ejercicio con variables artificiales')
    # Si la fase inicial fue exitosa y la matriz transformada no es None, ejecuta el algoritmo Simplex.
    if matriz_transformada:
        solucion = resolver_simplex(matriz_transformada)
        
        # Muestra la solución.
        if isinstance(solucion, list):
            for fila in solucion:
                print(fila)
        else:
            print(solucion)  # Muestra el mensaje de error si hubo alguno.
    else:
        print("El problema no tiene solución factible.")

    # Para el ejercicio sin variables artificiales
    print('\n\nPara el ejercicio SIN variables artificiales')
    solucion2 = resolver_simplex(matriz_prueba2)
    # Muestra la solución.
    if isinstance(solucion2, list):
        for fila in solucion2:
            print(fila)
    else:
        print(solucion2)  # Muestra el mensaje de error si hubo alguno.



