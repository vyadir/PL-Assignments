def TablaSimplexAmpliada(c, T):
    
    print(f"Restricción original:\n{T}")
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
        
    print(f"\nRestricción con variables artificales:\n{T_trans}")
    
    #transpuesta de T1_trans
    T1_trans = [[fila[i] for fila in T_trans] for i in range(len(T_trans[0]))]
    
    def pivoteo(tabla):
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
        print("\nTabla simplex")
        print(T1_trans)
    
    else:
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
        print("prueba",T1_trans)
        print("\nTabla simplex ampliada")
        print(pivoteo(T1_trans))
        print("\nVariables artificiales:", ', '.join(variables_artificiales))
        
    
# Ejemplo 
#c = [-3,-2]
#T = [[2, 5,'<=', 35], [-3, 2,'>=', -18],[2,4,"<=",26]]


c = [-2,-5]
T = [[1,6,'<=', 20], [1,1,'<=', 60],[1,0,"<=",40]]  
tabla_ampliada = TablaSimplexAmpliada(c, T)
