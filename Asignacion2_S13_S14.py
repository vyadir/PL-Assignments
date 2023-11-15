def TablaSimplexAmpliada(c, T):
    
    print("Restricción original: ",T)
    num_restricciones = len(T)
    num_variables = 0
    num_artificiales = 0
    
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
    
    # Añadir el vector b a T_trans:
    b = []
    for restriccion in T:
        b.append(restriccion[-1])
    T_trans.append(b)
        
    print("Restricción con variables artificales: ",T_trans)
    
    # Creación de la tabla simlex estándar canónica
    tabla = []
    if num_artificiales == 0:
        # Devolver la tabla normal
        print(tabla)
    
    else:
        # Devolver la tabla ampliada y la lista de variables artificiales
        print(tabla)
    
# Ejemplo 
c = [5, 7]
T = [[7, 2, '>=', 5], [8, 9, '<=', 4], [-2, 5, '=', 6]]

tabla_ampliada = TablaSimplexAmpliada(c, T)
