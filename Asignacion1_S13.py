"""
    Creado por Yadir Vega
    Descripción: 

            Con las funciones que tenemos se procederá construir un programa que reciba lo ingresado por el usuario organice las funciones para
            construir un programa funcional que resuelva paso a paso el programa lineal.
            
            - Sin variables artificiales: Datos de usuario → Construcción de la tabla simplex inicial, agregando las variables de holgura y superfluas necesarias.
            → Se construye la tabla final de simplex → se dar la respuesta, si hay solución dar la solución, en caso que ho haya indicarlo y mencionar las
            razones en un mensaje.

            - Con variables artificiales: Datos de usuario → Construcción de la tabla simplex ampliada → Optimización de la función de penalización. Si las
            variables artificiales no son cero en la tabla final ampliada, dar mensaje de la no factibilidad del programa, de lo contrario retornar la tabla sin
            variables artificiales y sin la función objetivo → enviar la nueva tabla a la función que construye la tabla final de simplex → se dar la respuesta, si
            hay solución dar la solución, en caso que ho haya indicarlo y mencionar
            las razones en un mensaje.

"""

def TablaSimplexAmpliada(c, T):
    # Variable que guardara valor booleano de si el sistema es ampliado o no.
    A = False
    #print(f"Restricción original:\n{T}")
    num_restricciones = len(T)
    num_variables = 0
    num_artificiales = 0
    variables_artificiales = []  # Lista para almacenar las variables artificiales
    
    # Contar la cantidad de variables:
    for restriccion in T:
        var_max = len(restriccion)-2
        if var_max > num_variables:
            num_variables = var_max # Toma el número más grande de variables
            
    var_originales=num_variables 
    #print(var_originales)

    # Añadir variables de holgura y superfluas:
    for restriccion in T:
        if '<=' in restriccion or '>=' in restriccion:
            num_variables += 1
    #print(num_variables)
    
    # Añadir las variables faltantes a las restricciones
    for restriccion in T:
        var_actuales = len(restriccion)-2
        var_faltantes = num_variables - var_actuales
        if var_faltantes > 0:
            for i in range(var_faltantes):
                # Añade ceros faltantes a la restriccion 
                restriccion.insert(var_actuales + i, 0) 
                
        # Añade 1 o -1 en la posicion de la variable de holgura o superflua
        if '<=' in restriccion:
            restriccion[var_originales + T.index(restriccion)]=1
        if '>=' in restriccion:
            restriccion[var_originales + T.index(restriccion)]=-1
            
    # Comprobar si los vectores Identidad están en T
    T_trans=[]
    for i in range(num_variables):
        fila = []
        for restriccion in T:
            fila.append(restriccion[i])
        T_trans.append(fila)
    
    # Crear los vectores (1,0,0...), (0,1,0,...)
    vector_Iden=[]
    for i in range(num_restricciones):
        vi=[0]*num_restricciones
        vi[i]=1
        vector_Iden.append(vi)
        
    # Comprobar si los vectores se encuentran en T_trans:
    for vector in vector_Iden:
        if vector not in T_trans:
            T_trans.append(vector)
            num_artificiales += 1   
            variables_artificiales.append(f'x{num_variables + num_artificiales}')  # Agregar la variable artificial a la lista
    
    # Añadir el vector b a T_trans:
    b = []
    for restriccion in T:
        b.append(restriccion[-1])
    T_trans.append(b)
        
    #print(f"\nRestricción con variables artificales:\n{T_trans}")
    
    #transpuesta de T1_trans
    T1_trans = [[fila[i] for fila in T_trans] for i in range(len(T_trans[0]))]
    
    def pivoteo2(tabla):
        num_fil = len(tabla)
        num_col = len(tabla[0])

        # Buscar el penúltimo elemento en la última fila
        penultimo_elem = tabla[num_fil - 1][num_col - 2]

        # Buscar la fila que tiene un "1" en la misma columna que el penúltimo elemento
        pivot_row = -1
        for i in range(num_fil - 1):
            if tabla[i][num_col - 2] == 1:
                pivot_row = i
                break

        # Realizar la operación F_ultima - F_encontrada
        if pivot_row != -1:
            for i in range(num_col):
                tabla[num_fil - 1][i] -= tabla[pivot_row][i]

        return tabla

    
    # Creación de la tabla simlex estándar canónica
    if num_artificiales == 0:
        a=len(T1_trans[0])-len(c)-1
        for i in range(a):
            c.append(0)
        c.append(0)
        T1_trans.append(c)
        # Devolver la tabla normal
        #print("\nTabla simplex")
        #print(T1_trans)
    
    else:
        A=True
        a=len(T1_trans[0])-len(c)-1
        for i in range(a):
            c.append(0)
        c.append(0)
        T1_trans.append(c)
        # Devolver la tabla ampliada y la lista de variables artificiales
        b=len(T1_trans[0])-num_artificiales-1
        M=[]
        for i in range(b):
            M.append(0)
        for i in range(num_artificiales):
            M.append(1)
        M.append(0)
        T1_trans.append(M)
        #print("prueba",T1_trans)
        #print("\nTabla simplex ampliada")
        return pivoteo2(T1_trans),A
        #print("\nVariables artificiales:", ', '.join(variables_artificiales))
        
    

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
    


def iniciar_programa(c, T):
    matriz, esAmpliado = TablaSimplexAmpliada(c,T)
    print(matriz,esAmpliado)
    solucion = None
    if esAmpliado:
        matriz_t = fase_inicial(matriz)
        if matriz_t:
            solucion = resolver_simplex(matriz_t)
    else:
        solucion = resolver_simplex(matriz)


    if isinstance(solucion, list):
        for fila in solucion:
            print(fila)
    else:
        print(solucion)



# Punto de entrada del programa.
if __name__ == '__main__':
    c = [-2,-5]
    T = [[1,6,'<=', 20], [1,1,'<=', 60],[1,0,"<=",40]]  
    iniciar_programa(c, T)