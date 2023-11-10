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
import copy

#Operaciones sobre las filas de una matriz
def Escalamiento(matriz, k, i):
    # Verifica que la fila dada exista y que el factor no sea 0.
    if i <= len(matriz) and k != 0:
        for j in range(len(matriz[i-1])):
            matriz[i-1][j] *= k  # Multiplica cada elemento de la fila por k.
    else:
        print('La entrada de la fila es invalida')  # Mensaje de error.
    return matriz


def Pivoteo(matriz, i, k, j):
    # Verifica que las filas dadas existan y que el factor no sea 0.
    if (i and j) <= len(matriz) and k != 0:
        n = len(matriz[i-1])  # Longitud de la fila i.
        # Verifica que ambas filas tengan la misma longitud.
        if n == len(matriz[j-1]):
            for elemento_n in range(n):
                matriz[i-1][elemento_n] += k * matriz[j-1][elemento_n]  # Suma k veces la fila j a la fila i.
    return matriz

#Matriz Aumentada

def TablaSimplexAmpliada(c, T, z0):
    
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
            variables_artificiales.append(f'{num_variables + num_artificiales}')  # Agregar la variable artificial a la lista
    
    # Añadir el vector b a T_trans:
    b = []
    for restriccion in T:
        b.append(restriccion[-1])
    T_trans.append(b)
    
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
        T1_trans[-1][-1]=-z0
        # Devolver la tabla normal
        isAmpliada = False
    else:
        a=len(T1_trans[0])-len(c)-1
        for i in range(a):
            c.append(0)
        c.append(0)
        T1_trans.append(c)
        T1_trans[-1][-1]=-z0
        # Devolver la tabla ampliada y la lista de variables artificiales
        b=len(T1_trans[0])-num_artificiales-1
        M=[]
        for i in range(b):
            M.append(0)
        for i in range(num_artificiales):
            M.append(1)
        M.append(0)
        T1_trans.append(M)
        #Importante no borrar
        pivoteo(T1_trans)
        print("\nVariables artificiales:", ', '.join(variables_artificiales))
        isAmpliada = True
    
    return T1_trans, isAmpliada, variables_artificiales

#Simplex (Taylor's Version), asumamos que el programa se encuentra de antemano en su forma canonica.

def AlgoritmoSimplex(Matriz, EsAmpliado):
    NFilas, NColumnas = len(Matriz), len(Matriz[0])
    Ejecutar = True
    while(Ejecutar):
        #Si todos los coeficientes de la funcion objetivo son no negativos, se finaliza automaticamente
        if min(Matriz[NFilas-1][0:NColumnas-1])>=0:
            Ejecutar = False

        if Ejecutar:
            #Encontrar columna pivote, recorre la funcion objetivo y devuelve el indice del menor elemento
            columna_pivote = 0
            for i in range(0, NColumnas-1):
                if (Matriz[NFilas-1][i] < Matriz[NFilas-1][columna_pivote]):
                    columna_pivote = i
            fila_pivote = -1
            #Encontrar Pivote

            #Recordar que la ultima fila puede variar si es ampliado o no
            if EsAmpliado:
                CantidadFilasSimplex=NFilas-2
            else:
                CantidadFilasSimplex = NFilas - 1
            for i in range(CantidadFilasSimplex):
                if Matriz[i][columna_pivote]>0:
                    cociente = Matriz[i][NColumnas-1]/Matriz[i][columna_pivote]
            if cociente > 0:
                for i in range(0, CantidadFilasSimplex):
                    if Matriz[i][columna_pivote]>0:
                        cocienteFila = Matriz[i][NColumnas-1]/Matriz[i][columna_pivote]
                        if cocienteFila > 0 and cocienteFila <= cociente:
                            fila_pivote = i
                            cociente = cocienteFila
            if fila_pivote == -1:
                print('El programa no tiene solucion optima')
                Ejecutar = False
                Matriz = []
                
        if Ejecutar:
            #Proceso de pivote
            ElementoPivote = Matriz[fila_pivote][columna_pivote]
            #Primer paso pivote 
            Matriz = Escalamiento(Matriz, 1/ElementoPivote, fila_pivote+1)
            #Segundo paso pivoteo
            for i in range(0, NFilas):
                if i != fila_pivote:
                    Valor_k = -Matriz[i][columna_pivote]
                    Matriz = Pivoteo(Matriz, i+1, Valor_k, fila_pivote+1)
    return Matriz

def AlgoritmoSimplexPasoAPaso(Matriz, EsAmpliado):
    NFilas, NColumnas = len(Matriz), len(Matriz[0])
    Ejecutar = True
    Matrices=[]
    while(Ejecutar):
        #Si todos los coeficientes de la funcion objetivo son no negativos, se finaliza automaticamente
        if min(Matriz[NFilas-1][0:NColumnas-1])>=0:
            Ejecutar = False

        if Ejecutar:
            #Encontrar columna pivote, recorre la funcion objetivo y devuelve el indice del menor elemento
            columna_pivote = 0
            for i in range(0, NColumnas-1):
                if (Matriz[NFilas-1][i] < Matriz[NFilas-1][columna_pivote]):
                    columna_pivote = i
            fila_pivote = -1
            #Encontrar Pivote

            #Recordar que la ultima fila puede variar si es ampliado o no
            if EsAmpliado:
                CantidadFilasSimplex=NFilas-2
            else:
                CantidadFilasSimplex = NFilas - 1
            for i in range(CantidadFilasSimplex):
                if Matriz[i][columna_pivote]>0:
                    cociente = Matriz[i][NColumnas-1]/Matriz[i][columna_pivote]
            if cociente > 0:
                for i in range(0, CantidadFilasSimplex):
                    if Matriz[i][columna_pivote]>0:
                        cocienteFila = Matriz[i][NColumnas-1]/Matriz[i][columna_pivote]
                        if cocienteFila > 0 and cocienteFila <= cociente:
                            fila_pivote = i
                            cociente = cocienteFila
            if fila_pivote == -1:
                print('El programa no tiene solucion optima')
                Ejecutar = False
                Matriz = []
                
        if Ejecutar:
            #Proceso de pivote
            ElementoPivote = Matriz[fila_pivote][columna_pivote]
            #Primer paso pivote 
            Matriz = Escalamiento(Matriz, 1/ElementoPivote, fila_pivote+1)
            #Segundo paso pivoteo
            for i in range(0, NFilas):
                if i != fila_pivote:
                    Valor_k = -Matriz[i][columna_pivote]
                    Matriz = Pivoteo(Matriz, i+1, Valor_k, fila_pivote+1)
            Matrices.append(Matriz)
    return Matrices

def obtenerVector(T):
    NFilas, NColumnas = len(T), len(T[0])
    VectorSolucion = [0]*(NColumnas-1)
    for i in range(NFilas-1):
        for j in range(NColumnas-1):
            if T[i][j] == 1 and T[NFilas-1][j]==0:
                VectorSolucion[j] = T[i][NColumnas-1]
    return VectorSolucion
#Terminar S13

#Pruebas

#T = [[2,5,2,0,1,0,3], [1,2,4,0,0,1,6], [3,-2,1,1,0,0,4],[2,-3,1,0,0,0,-9/5]]
#T=[[4,2,1,0,32],[2,3,0,1,24],[-5,-4,0,0,0]]

#Pruebas
"""Estado 1 sera que el programa reciba un problema lineal y retorne unicamente 
el resultado, la solucion optima o el mensaje de fracaso."""
def IniciarProgramaEstado1(c,T,z0):
    Tabla, TieneArtificiales, Artificiales = TablaSimplexAmpliada(c, T,z0)
    #print(TieneArtificiales)
    #print(Tabla)
    if TieneArtificiales:
        #Cuales son las variables artificiales
        VectorArtificiales =[]
        for _ in Artificiales:
            VectorArtificiales.append(int(_))
        VectorArtificiales.sort(reverse=True)
        #Simplex para sistemas aumentados
        AlgoritmoSimplex(Tabla, True)
        if Tabla:
            #Commpara que cada 
            SolucionProgramaAmplicado = obtenerVector(Tabla)
            Validacion = True
            for IndiceArtificial in VectorArtificiales:
                if SolucionProgramaAmplicado[(IndiceArtificial)-1] != 0:
                    Validacion = False
            if Validacion:
                #print('Programa ampliado converge y la penalización es nula')
                #print(Tabla)
                #Proceso de poda, corregir
                #print('Inicio proceso de poda')
                del(Tabla[-1])
                
                for i in range(len(Tabla)):
                    for IndiceArtificial in VectorArtificiales:
                        del(Tabla[i][IndiceArtificial-1])
                #print(Tabla)
            else:
                #print('Programa lineal ampliado no paga los pesos')
                Tabla = []
        else:
            #print('Programa sin solucion')
            pass
    #Simplex
    Tabla = AlgoritmoSimplex(Tabla,False)
    if Tabla:
        #print('Solucion del programa lineal ')
        #print(Tabla)
        #print(obtenerVector(Tabla))
        pass
    else:
        #print('Programa lineal sin solucion')
        pass
    return obtenerVector(Tabla),Tabla[-1][-1]

"""Estado 2 sera que el programa reciba un problema lineal, muestre la tabla 
simplex inicial y la tabla simplex final junto con la solucion o el mensaje
de fracaso. En caso de requerir variables artificiales, deber´a mostrar la 
tabla simplex intermedia."""
def IniciarProgramaEstado2(c,T,z0):
    Tabla, TieneArtificiales, Artificiales = TablaSimplexAmpliada(c, T,z0)
    lista = [TieneArtificiales]
    #print(TieneArtificiales)
    #print(Tabla)
    lista.append(copy.deepcopy(Tabla))
    if TieneArtificiales:
        #Cuales son las variables artificiales
        VectorArtificiales =[]
        for _ in Artificiales:
            VectorArtificiales.append(int(_))
        VectorArtificiales.sort(reverse=True)
        #Simplex para sistemas aumentados
        AlgoritmoSimplex(Tabla, True)
        #print(Tabla)
        lista.append(copy.deepcopy(Tabla))
        if Tabla:
            #Commpara que cada 
            SolucionProgramaAmplicado = obtenerVector(Tabla)
            Validacion = True
            for IndiceArtificial in VectorArtificiales:
                if SolucionProgramaAmplicado[(IndiceArtificial)-1] != 0:
                    Validacion = False
            if Validacion:
                #print('Programa ampliado converge y la penalización es nula')
                #print(Tabla)
                #Proceso de poda, corregir
                #print('Inicio proceso de poda')
                del(Tabla[-1])
                for i in range(len(Tabla)):
                    for IndiceArtificial in VectorArtificiales:
                        del(Tabla[i][IndiceArtificial-1])
                #print(Tabla)
                lista.append(copy.deepcopy(Tabla))
            else:
                #print('Programa lineal ampliado no paga los pesos')
                Tabla = []
        else:
            #print('Programa sin solucion')
            pass
    #Simplex
    Tabla = AlgoritmoSimplex(Tabla,False)
    if Tabla:
        #print('Solucion del programa lineal ')
        #print(Tabla)
        lista.append(copy.deepcopy(Tabla))
        Sol = obtenerVector(Tabla)
        lista.append(Sol)
        #print(obtenerVector(Tabla))
        pass
    else:
       #print('Programa lineal sin solucion')
       pass
    return lista

def IniciarProgramaPasoAPaso(c,T,z0):
    Tabla, TieneArtificiales, Artificiales = TablaSimplexAmpliada(c, T,z0)
    print(TieneArtificiales)
    print(Tabla)
    if TieneArtificiales:
        #Cuales son las variables artificiales
        VectorArtificiales =[]
        for _ in Artificiales:
            VectorArtificiales.append(int(_))
        VectorArtificiales.sort(reverse=True)
        #Simplex para sistemas aumentados
        AlgoritmoSimplex(Tabla, True)
        if Tabla:
            #Commpara que cada 
            SolucionProgramaAmplicado = obtenerVector(Tabla)
            Validacion = True
            for IndiceArtificial in VectorArtificiales:
                if SolucionProgramaAmplicado[(IndiceArtificial)-1] != 0:
                    Validacion = False
            if Validacion:
                print('Programa ampliado converge y la penalización es nula')
                print(Tabla)
                #Proceso de poda, corregir
                print('Inicio proceso de poda')
                del(Tabla[-1])
                
                for i in range(len(Tabla)):
                    for IndiceArtificial in VectorArtificiales:
                        del(Tabla[i][IndiceArtificial-1])
                print(Tabla)
            else:
                print('Programa lineal ampliado no paga los pesos')
                Tabla = []
        else:
            print('Programa sin solucion')
    #Simplex
    Tabla = AlgoritmoSimplex(Tabla,False)
    if Tabla:
        print('Solucion del programa lineal ')
        print(Tabla)
        print(obtenerVector(Tabla))
    else:
        print('Programa lineal sin solucion')
    return Tabla[-1][-1],Tabla,obtenerVector(Tabla)
# Estado 1 sera que el programa reciba un problema lineal y retorne unicamente el resultado, 
# la solucion optima o el mensaje de fracaso.
def estado1(c,T,z0):
    Tabla, TieneArtificiales, Artificiales = TablaSimplexAmpliada(c, T,z0)
    puntoOptimo = None
    if TieneArtificiales:
        matriz = AlgoritmoSimplex(Tabla, True)
        puntoOptimo = obtenerVector(matriz)
    else:
        matriz = AlgoritmoSimplex(Tabla, False)
        puntoOptimo = obtenerVector(matriz)
    return puntoOptimo, matriz[-1][-1]


# Estado 2 sera que el programa reciba un problema lineal, muestre la tabla 
# simplex inicial y la tabla simplex final junto con la solucion o el mensaje
# de fracaso. En caso de requerir variables artificiales, deber´a mostrar la tabla simplex intermedia.
"""
def estado2(c,T,z0):
    TablaIntermedia,TablaFinal=IniciarPrograma(c, T, z0)
    print(f"{TablaIntermedia}\n\n{TablaFinal}")

# La Estado 3 sera que el programa reciba un problema lineal y muestre todo el
# procedimiento paso a paso.
def estado3(c,T,z0):
    pass
"""

def administrador_estados(c,T,z0,estado):
    resultado = None
    puntoOptimo = None
    if estado == 1:
        puntoOptimo, resultado = IniciarProgramaEstado1(c,T,z0)
        print(f"\nEl resultado es {resultado} el cual se alcanza en {puntoOptimo}\n")
    elif estado == 2:
        lista=IniciarProgramaEstado2(c,T,z0)
        TieneArtificiales = lista[0]
        lista = IniciarProgramaEstado2(c,T,z0)
        if TieneArtificiales:
            print(f"La tabla inicial simplex es\n {lista[1]}\n\nLa tabla simplex previo a la convergencia de las variables artificiales es\n {lista[2]}\n\nLa tabla simplex luego de la poda de variables artificiales es\n {lista[3]}\n\nLa tabla final simplex es \n{lista[4]}\n\nLa solución óptima es\n{lista[5]}")
        else:
            print(f"La tabla inicial simplex es\n {lista[1]}\n\nLa tabla final simplex es \n{lista[2]}\n\nLa solución óptima es\n{lista[3]}")
    #elif estado ==3:
        #estado3(c,T,z0)
    #else:
        #print("El estado ingresado no es válido. Ingrese 1, 2 o 3") 
    #pass
    


# Ejemplo sin artificiales
c=[3,0,0,5,0]
T=[[2,0,1,-1,0,'=',2],[1,1,0,-3,0,'=',1],[-2,0,0,5,1,'=',3]]
z0=0


"""
# Ejemplo con artificiales
c=[3,-2]
T=[[2,1,'>=',4],[-1,1,'<=',4],[3,-1,'<=',15],[1,0,'<=',7]]
z0=-3
"""

administrador_estados(c,T,z0,2)

"""
IniciarPrograma(c, T, z0)
"""