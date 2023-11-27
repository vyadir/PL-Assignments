"""
    Estados solicitados en el requeirmiento
"""

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
        
        #Simplex para prgramas aumentados
        AlgoritmoSimplex(Tabla, True)
        print(Tabla)
        if Tabla:
            #Commpara que el programa se encuentre en forma estandar y canonica para devolver el vector solucion
            
            SolucionProgramaAmplicado = obtenerVector(Tabla)
            Validacion = True
            for IndiceArtificial in VectorArtificiales:
                #Valida que el vector del sistema ampliado tenga las variables artificiales iguales a 0
                if SolucionProgramaAmplicado[(IndiceArtificial)-1] != 0:
                    Validacion = False
            if Validacion:

                #Proceso de poda
                del(Tabla[-1])
                for i in range(len(Tabla)):
                    for IndiceArtificial in VectorArtificiales:
                        del(Tabla[i][IndiceArtificial-1])
                #print(Tabla)
            else:
                Tabla = []
        else:
            pass
    Tabla = AlgoritmoSimplex(Tabla,False)
    return obtenerVector(Tabla),Tabla[-1][-1]

"""Estado 2 sera que el programa reciba un problema lineal, muestre la tabla 
simplex inicial y la tabla simplex final junto con la solucion o el mensaje
de fracaso. En caso de requerir variables artificiales, debera mostrar la 
tabla simplex intermedia."""
def IniciarProgramaEstado2(c,T,z0):
    Tabla, TieneArtificiales, Artificiales = TablaSimplexAmpliada(c, T,z0)
    lista = [TieneArtificiales]
    lista.append(copy.deepcopy(Tabla))
    if TieneArtificiales:
        #Cuales son las variables artificiales
        VectorArtificiales =[]
        for _ in Artificiales:
            VectorArtificiales.append(int(_))
        VectorArtificiales.sort(reverse=True)
        #Simplex para sistemas aumentados
        AlgoritmoSimplex(Tabla, True)
        lista.append(copy.deepcopy(Tabla))
        if Tabla:
            #Commpara que cada solucion de las variables artificiales del programa ampliado sea 0, es decir que converja
            SolucionProgramaAmplicado = obtenerVector(Tabla)
            Validacion = True
            for IndiceArtificial in VectorArtificiales:
                if SolucionProgramaAmplicado[(IndiceArtificial)-1] != 0:
                    Validacion = False
            if Validacion:
                #Proceso de poda
                del(Tabla[-1])
                for i in range(len(Tabla)):
                    for IndiceArtificial in VectorArtificiales:
                        del(Tabla[i][IndiceArtificial-1])
                #print(Tabla)
                #Captura de tabla intermmedia
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
        #Obtener solucion y la captura
        lista.append(Tabla)
        Sol = obtenerVector(Tabla)
        lista.append(Sol)
        pass
    else:

    return lista

# Estado 3 
def AlgoritmoSimplexPasoAPaso(Matriz, EsAmpliado):
    NFilas, NColumnas = len(Matriz), len(Matriz[0])
    Ejecutar = True

    #Primera iteracion 
    print('Primera iteracion ')
    Matrices = []
    Matrices.append(copy.deepcopy(Matriz))
    print(Matrices)
    input()

    
    while(Ejecutar):
        #Si todos los coeficientes de la funcion objetivo son no negativos, se finaliza automaticamente
        if min(Matriz[NFilas-1][0:NColumnas-1])>=0:
            print('Se encontro que todos los coeficientes de la funcion objetivo son no negativos, fin del programa')
            input()
            Ejecutar = False

        if Ejecutar:
            #Encontrar columna pivote, recorre la funcion objetivo y devuelve el indice del menor elemento
            columna_pivote = 0
            for i in range(0, NColumnas-1):
                if (Matriz[NFilas-1][i] < Matriz[NFilas-1][columna_pivote]):
                    columna_pivote = i
            print('Columna pivote:', columna_pivote+1, ' dado que ', Matriz[NFilas-1][columna_pivote], ' es el menor coeficiente negativo de la funcion objetivo')
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
                print('Fila pivote:', fila_pivote+1, ' dado que ', Matriz[fila_pivote][NColumnas-1], '/', Matriz[fila_pivote][columna_pivote] ,' es el menor cociente no negativo')
                print('De esta manera el elemento pivote ')
                input()
            else:
                Ejecutar = False
                T = []
        if Ejecutar:
            print('Proceso de pivoteo:')
            input()
            #Proceso de pivote
            print('Elemento pivote se encuentra en la posicion', fila_pivote+1, ',', columna_pivote+1)
            
            ElementoPivote = Matriz[fila_pivote][columna_pivote]

            print('Elemento pivote corresponde a', ElementoPivote)
            input()
            #Primer paso pivote 
            Matriz = Escalamiento(Matriz, 1/ElementoPivote, fila_pivote+1)
            print('Se multiplica fila ', fila_pivote+1, ' por ', 1/ElementoPivote)
            input()
            #Segundo paso pivoteo
            for i in range(0, NFilas):
                if i != fila_pivote:
                    Valor_k = -Matriz[i][columna_pivote]
                    print('A la fila ', i+1, ' se le suma ', Valor_k, ' veces la fila ', fila_pivote+1)
                    print('El resultado del proceso es: ')
                    Matriz = Pivoteo(Matriz, i+1, Valor_k, fila_pivote+1)
                    print(Matriz)
                    input()
            Matrices.append(copy.deepcopy(Matriz))
    return Matriz