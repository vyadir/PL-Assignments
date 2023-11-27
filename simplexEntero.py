import copy
import math

"""
    Ahora, se utiliza todo el código anterior para implementar la parte de programación entera.
"""
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
            #Encontrar Pivote

            #Recordar que la ultima fila puede variar si es ampliado o no
            if EsAmpliado:
                CantidadFilasSimplex=NFilas-2
            else:
                CantidadFilasSimplex = NFilas - 1
            
            VectorCocientes = [-float('inf')]*CantidadFilasSimplex
            for i in range(CantidadFilasSimplex):
                if Matriz[i][columna_pivote]!=0:
                    VectorCocientes[i] = Matriz[i][NColumnas-1]/Matriz[i][columna_pivote]
            Cocientes_Postivos = [numero for numero in VectorCocientes if numero >= 0]
            if Cocientes_Postivos:
                # Encontrar el índice del menor número positivo
                fila_pivote = VectorCocientes.index(min(Cocientes_Postivos))
            else:
                Ejecutar = False
                T = []
            
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

def obtenerVector(T):
    NFilas, NColumnas = len(T), len(T[0])
    VectorSolucion = [0]*(NColumnas-1)
    for i in range(NFilas-1):
        for j in range(NColumnas-1):
            if T[i][j] == 1 and T[NFilas-1][j]==0:
                VectorSolucion[j] = T[i][NColumnas-1]
    return VectorSolucion

def contadorNodo():
    global nodoContador
    nodoContador+=1

def simplexEntero(Matriz, padre, T, numNodo, c, z0, EsAmpliado, Artificiales):
    global nodoContador
    NColumnas = len(T[0])
    
    if EsAmpliado:
        VectorArtificiales=[]
        for _ in Artificiales:
            VectorArtificiales.append(int(_))
        VectorArtificiales.sort(reverse=True)
        
        Matriz=AlgoritmoSimplex(Matriz, True)
        del(Matriz[-1])
        for i in range(len(Matriz)):
            for IndiceArtificial in VectorArtificiales:
                del(Matriz[i][IndiceArtificial-1])
                
    Matriz=AlgoritmoSimplex(Matriz, False)
    solucion=obtenerVector(Matriz)

    vectorSoloVar=[]
    for i in range(NColumnas-2):
        vectorSoloVar.append(solucion[i])
    optimo=Matriz[-1][-1]
    print("----------------------------------------------")
    print("\nNodo:", numNodo, "| Hijo de:",padre)
    print("T usado:", T, "\nResultados:")
    print("z*:",optimo)
    print("Vector de solución:", vectorSoloVar)

    
    #Verificar que los valores son enteros
    todosEnteros=True
    valor=0
    var=0
    for num in solucion:
        if num % 1 != 0: #Si se encuentra un valor no entero
            todosEnteros=False
            valor=num #Se toma el primer valor no entero
            var=solucion.index(num)
            break
        
    if todosEnteros:
        if optimo == 0:
            print("Solución no factible")
        else:
            print("Converge con solución:", optimo)
    else:
        v1 = math.floor(valor)
        v2 = math.ceil(valor)
        cCopiado=copy.deepcopy(c)
        c2=copy.deepcopy(c)
        #Crear las nuevas restricciones
        
        #--------------------------------------------------------
        
        nuevaRest1 = [0]*(NColumnas) #Tamaño de la restriccion
        nuevaRest1[-2]="<=" #Añadir el menor o igual
        nuevaRest1[-1]=v1 # ... al piso del numero no entero
        nuevaRest1[var]=1        
        T1=copy.deepcopy(T) #Tomar el T actual
        T1.append(nuevaRest1) #Añadir el T al vector de restricciones        
        T11=copy.deepcopy(T1) #Guardar el T1 actual
        [Matriz1, Amp1, Art1]=TablaSimplexAmpliada(c, T1, z0)
        
        #Recalcular el simplex entero
        contadorNodo()
        simplexEntero(Matriz1, numNodo, T11, nodoContador, cCopiado, z0, Amp1, Art1) 
        
        #------------------ División ---------------------------
        
        nuevaRest2 = [0]*(NColumnas)
        nuevaRest2[-2]=">=" #Añadir el mayor o igual
        nuevaRest2[-1]=v2 # ... al techo del numero no entero
        nuevaRest2[var]=1
        T2=copy.deepcopy(T)
        T2.append(nuevaRest2)
        T22=copy.deepcopy(T2)
        [Matriz2, Amp2, Art2]=TablaSimplexAmpliada(c2, T2, z0)
        #Recalcular el simplex entero
        contadorNodo()
        simplexEntero(Matriz2, numNodo, T22, nodoContador, cCopiado, z0, Amp2, Art2)        
    return
    

# Ejemplo 
c=[-10,-1]
T=[[1, 6, '<=', 50], [12, 1, '<=', 60]]
z0=0
nodoContador=1
T_inicial=copy.deepcopy(T)
c_inicial=copy.deepcopy(c)

[MatrizA, Ampliado, Artificiales]=TablaSimplexAmpliada(c, T, z0)
simplexEntero(MatrizA, 0, T_inicial, 1, c_inicial, z0, Ampliado, Artificiales)

