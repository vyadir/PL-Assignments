"""
    Básicamente el algoritmo se encarga de realizar ambas versiones del método Simplex 
    (con y sin variables artificiales ), es decir, recibe la matriz inicial del método Simplex y 
    si tiene variables articiales.
"""

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
                # Encontrar el indice del menor numero positivo
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
    #Obtiene numero de filas y columnas de la tabla
    NFilas, NColumnas = len(T), len(T[0])
    #Vector de ceros
    VectorSolucion = [0]*(NColumnas-1)
    #Llena los valores si los valores corresponden a a variables no basicas.
    for i in range(NFilas-1):
        for j in range(NColumnas-1):
            if T[i][j] == 1 and T[NFilas-1][j]==0:
                VectorSolucion[j] = T[i][NColumnas-1]
    return VectorSolucion



    

