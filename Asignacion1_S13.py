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

# Función para permutar dos filas de una matriz
def Permutacion(matriz, i, j):
    # Verifica si i y j están dentro del rango de las filas de la matriz
    if (i and j) <= len(matriz):
        # Guarda temporalmente la fila i
        auxiliar = matriz[i]
        # Intercambia la fila i con la fila j
        matriz[i] = matriz[j]
        # Coloca la fila original i en la posición j
        matriz[j] = auxiliar
    # Retorna la matriz con las filas permutadas
    return matriz

# Función para escalar (multiplicar) una fila de una matriz por un factor k
def Escalamiento(matriz, k, i):
    # Verifica si i está dentro del rango y k no es cero
    if i < len(matriz) and k != 0:
        # Itera sobre cada elemento de la fila i
        for j in range(len(matriz[i])):
            # Multiplica el elemento por k
            matriz[i][j] *= k
    else:
        # Si i está fuera de rango o k es cero, imprime un mensaje de error
        print('La entrada de la fila es inválida')
    # Retorna la matriz escalada
    return matriz

# Función para realizar un pivoteo entre dos filas de una matriz
def Pivoteo(matriz, i, k, j):
    # Verifica si i y j están dentro del rango y k no es cero
    if (i and j) < len(matriz) and k != 0:
        # Obtiene la longitud de la fila i
        n = len(matriz[i])
        # Itera sobre cada elemento de la fila i
        for elemento_n in range(n):
            # Suma a la fila i, k veces la fila j
            matriz[i][elemento_n] += k * matriz[j][elemento_n]
    # Retorna la matriz con el pivoteo realizado
    return matriz

# Implementación del método Simplex
def algoritmo_simplex(T):
    # Obtiene las dimensiones de la tabla T
    m, n = len(T), len(T[0])
    # Mientras hayan coeficientes negativos en la fila objetivo
    while any(x < 0 for x in T[-1][:-1]):
        # Determina la columna pivote (la que tiene el coeficiente más negativo)
        columna_pivote = T[-1].index(min(T[-1][:-1]))
        # Si todos los coeficientes de la columna pivote son negativos, no hay solución óptima
        if all(x <= 0 for x in [fila[columna_pivote] for fila in T[:-1]]):
            raise ValueError("El problema no tiene solución óptima finita.")
        
        # Calcula las proporciones para determinar la fila pivote
        proporciones = [fila[-1] / fila[columna_pivote] if fila[columna_pivote] > 0 else float('inf') for fila in T[:-1]]
        fila_pivote = proporciones.index(min(proporciones))
        
        # Escala la fila pivote para que el elemento pivote sea 1
        Escalamiento(T, 1/T[fila_pivote][columna_pivote], fila_pivote)
        
        # Realiza las operaciones de pivoteo para que todos los otros elementos de la columna pivote sean cero
        for i in range(m):
            if i != fila_pivote:
                factor = T[i][columna_pivote]
                Pivoteo(T, i, -factor, fila_pivote)
    # Retorna la tabla T después de aplicar el método Simplex
    return T

# Construye la tabla inicial para el método Simplex
def construir_tabla(A, b, c):
    # Obtiene las dimensiones de la matriz A
    m, n = len(A), len(A[0])
    tabla = []
    # Agrega las filas correspondientes a las restricciones, añadiendo variables de holgura
    for i in range(m):
        fila = list(A[i])
        # Añade las variables de holgura
        for j in range(m):
            fila.append(1 if i == j else 0)
        fila.append(b[i])
        tabla.append(fila)
    # Añade la fila objetivo al final
    fila_objetivo = list(c) + [0] * m + [0]
    tabla.append(fila_objetivo)
    # Retorna la tabla inicial
    return tabla

# Resuelve un problema de programación lineal utilizando el método Simplex
def resolver_simplex(A, b, c):
    # Construye la tabla inicial
    tabla = construir_tabla(A, b, c)
    try:
        # Aplica el método Simplex
        resultado = algoritmo_simplex(tabla)
        # Obtiene el valor óptimo y la solución óptima
        valor_optimo = resultado[-1][-1]
        solucion = [fila[-1] for fila in resultado[:-1]]
        return f"Solución óptima: {solucion[:len(c)]}, Valor óptimo: {valor_optimo}"
    except ValueError as e:
        # En caso de error, retorna el mensaje de error
        return str(e)
    
def TablaSimplexAmpliada(c, T):
    """
    Genera la tabla ampliada para el algoritmo del simplex.
    
    Parámetros:
        c: lista de coeficientes de la función objetivo.
        T: lista de listas que representan las restricciones.
        
    Retorna:
        T1_trans: tabla ampliada.
        tiene_artificiales: booleano que indica si se añadieron variables artificiales.
        vars_artificiales: lista de nombres de variables artificiales.
    """
    
    num_restricciones = len(T)
    num_variables = len(c)
    num_artificiales = 0
    variables_artificiales = []
    
    # Contando las variables de holgura y exceso.
    for restriccion in T:
        if '<=' in restriccion or '>=' in restriccion:
            num_variables += 1
    
    # Transponiendo la matriz T para trabajar con filas en lugar de columnas.
    T_trans = []
    for i in range(num_variables):
        fila = []
        for restriccion in T:
            if i < len(restriccion) - 2:
                fila.append(restriccion[i])
            else:
                fila.append(0)
        T_trans.append(fila)
        
    # Creando la matriz identidad.
    vector_Iden = []
    for i in range(num_restricciones):
        vi = [0]*num_restricciones
        vi[i] = 1
        vector_Iden.append(vi)
    
    # Añadiendo variables artificiales si son necesarias.
    for vector in vector_Iden:
        if vector not in T_trans:
            T_trans.append(vector)
            num_artificiales += 1
            variables_artificiales.append(f'x{num_variables + num_artificiales}')
    
    # Extrayendo el vector b (lado derecho de las restricciones).
    b = []
    for restriccion in T:
        b.append(restriccion[-1])
    T_trans.append(b)
    
    # Volviendo a transponer para tener la matriz en su forma original.
    T1_trans = [[fila[i] for fila in T_trans] for i in range(len(T_trans[0]))]
    
    # Añadiendo la función objetivo a la tabla.
    c = c + [0]*(len(T1_trans[0])-len(c)-1)
    c.append("z")
    T1_trans.append(c)
    
    # Si hay variables artificiales, añadimos una fila con el coeficiente M.
    if num_artificiales > 0:
        M = [0]*(len(T1_trans[0])-num_artificiales-1) + [1]*num_artificiales
        M.append("M")
        T1_trans.append(M)
        return T1_trans, True, variables_artificiales
    else:
        return T1_trans, False, []

def resolver_programacion_lineal(c, T):
    """
    Resuelve un problema de programación lineal.
    
    Parámetros:
        c: lista de coeficientes de la función objetivo.
        T: lista de listas que representan las restricciones.
        
    Retorna:
        Solución óptima y valor óptimo.
    """
    
    tabla_ampliada, tiene_artificiales, vars_artificiales = TablaSimplexAmpliada(c, T)
    
    # Si hay variables artificiales, ejecutamos el simplex dos veces.
    if tiene_artificiales:
        optimizado = algoritmo_simplex(tabla_ampliada[:-1])
        
        if any(row[-1] > 0 for var in vars_artificiales for row in optimizado if var in row):
            return "El programa no es factible."
        
        tabla_ampliada = [row[:-len(vars_artificiales)] for row in optimizado] + [tabla_ampliada[-1][:-len(vars_artificiales)]]
    
    # Resolviendo el problema.
    try:
        print(tabla_ampliada)
        resultado = algoritmo_simplex(tabla_ampliada)
        valor_optimo = resultado[-1][-1]
        solucion = [fila[-1] for fila in resultado[:-1]]
        return f"Solución óptima: {solucion[:len(c)]}, Valor óptimo: {valor_optimo}"
    except ValueError as e:
        return str(e)

# Ejemplo de uso.
c = [5, 7]
T = [[7, 2, '>=', 5], [8, 9, '<=', 4], [-2, 5, '=', 6]]
print(resolver_programacion_lineal(c, T))

