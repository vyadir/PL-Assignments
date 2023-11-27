"""
    Esta función recibe el sistema de restricciones de un programa de minimización y el vector $c$ correspondiente a 
    las constantes de $z=cx^T$, el programa retorna la tabla simplex estandar canónica y si es necesario devuelve la 
    tabla ampliada con las variables artificiales.

    Antes de definir esta función se necesita un paso antes para realizar el procedimiento de pivoteo en las variables 
    artificiales, por lo que se crea la función que se ve a continuación.
"""

def pivoteo(tabla):
    num_fil = len(tabla)
    num_col = len(tabla[0])

    # Buscar el penultimo elemento en la ultima fila
    penultimo_elem = tabla[num_fil - 1][num_col - 2]

    # Buscar la fila que tiene un "1" en la misma columna que el penultimo elemento
    pivot_row = -1
    for i in range(num_fil - 1):
        if tabla[i][num_col - 2] == 1:
            pivot_row = i
            break

    # Realizar la operacion F_ultima - F_encontrada
    if pivot_row != -1:
        for i in range(num_col):
            tabla[num_fil - 1][i] -= tabla[pivot_row][i]

    return tabla

def TablaSimplexAmpliada(c, T):
    
    num_restricciones = len(T)
    num_variables = 0
    num_artificiales = 0
    variables_artificiales = [] 
    
    # Contar la cantidad de variables:
    for restriccion in T:
        var_max = len(restriccion)-2
        if var_max > num_variables:
            num_variables = var_max # Toma el valor mas grande
            
    var_originales=num_variables # Guarda las variables originales

    # Verifica si hay variables de holgura o superfluas
    for restriccion in T:
        if '<=' in restriccion or '>=' in restriccion:
            num_variables += 1
    
    # Agrega las variables faltantes a las restricciones
    for restriccion in T:
        var_actuales = len(restriccion)-2
        var_faltantes = num_variables - var_actuales
        
        # Agrega ceros faltantes a la restriccion 
        if var_faltantes > 0:
            for i in range(var_faltantes):
                restriccion.insert(var_actuales + i, 0) 
                
        # Agrega 1 o -1 si es variable de holgura o superflua
        if '<=' in restriccion:
            restriccion[var_originales + T.index(restriccion)]=1
        if '>=' in restriccion:
            restriccion[var_originales + T.index(restriccion)]=-1
            
    # Ahora se va a comprobar si los vectores Identidad estan en T, primero se crea la matriz transpuesta, luego se verifica si los vectores identidad estan en ella. En caso que no, se agregan
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

            # Agregar la variable artificial a la lista
            variables_artificiales.append(f'x{num_variables + num_artificiales}')  
    
    # Agrega el vector b a T_trans:
    b = []
    for restriccion in T:
        b.append(restriccion[-1])
    T_trans.append(b)
    
    #transpuesta de T_trans
    T1_trans = [[fila[i] for fila in T_trans] for i in range(len(T_trans[0]))]
    
    # Creacion de la tabla simplex estandar canonica

    # Para el caso en que no hayan variables artificiales:
    if num_artificiales == 0:
        a=len(T1_trans[0])-len(c)-1
        for i in range(a):
            c.append(0)
        c.append("z")
        T1_trans.append(c)
        
        # Devolver la tabla normal
        return T1_trans, 0

    # En caso que si hayan variables artificiales:
    else:
        # Agregar al vector de constantes las variables que no se usan
        a=len(T1_trans[0])-len(c)-1
        for i in range(a):
            c.append(0)
        c.append("z")
        T1_trans.append(c)
        
        # Crear el vector de la tabla ampliada
        b=len(T1_trans[0])-num_artificiales-1
        M=[]
        for i in range(b):
            M.append(0)
        for i in range(num_artificiales):
            M.append(1)
        M.append("M")
        T1_trans.append(M)

        # Retornar la tabla ampliada y variables artificiales
        return pivoteo(T1_trans), variables_artificiales
    

# Prueba 
c = [5, 7]
T = [[7, 2, '>=', 5], [8, 9, '<=', 4], [-2, 5, '=', 6]]
[tabla_ampliada, artificiales] = TablaSimplexAmpliada(c, T)
print(tabla_ampliada)
print(artificiales)

"""
    Salida:
        [[7, 2, -1, 0, 1, 0, 5], [8, 9, 0, 1, 0, 0, 4], [-2, 5, 0, 0, 0, 1, 6], [5, 7, 0, 0, 0, 0, 'z'], [0, 0, 0, 0, 1, 1, 'M']]
        ['x5', 'x6']

"""