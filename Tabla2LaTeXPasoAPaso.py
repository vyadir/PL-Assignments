"""
    Seguidamente, tomando como referencia el estado 3 de la sección anterior se creó el siguiente código que realiza el 
    procedimiento del simplex paso a paso y devuelve el código \LaTeX.
"""

def Tabla2LaTeX(A, Ampl):
    m = len(A)      # Calcula el numero de filas de la matriz
    n = len(A[0])   # Calcula el numero de columnas de la matriz
    
    # Comienza a construir el codigo LaTeX
    latex_code = "\\begin{tabular}{|" + "c" * (n-1) + "|c|}\\hline\n"

    # Itera sobre las filas de la matriz
    for i, fila in enumerate(A):
        # Itera sobre los elementos de cada fila
        for elemento in fila:
            # Agrega el elemento a la tabla LaTeX
            latex_code += str(elemento) + " & "

        # Elimina el ultimo " & " de la fila y agrega una nueva linea
        latex_code = latex_code[:-2] + " \\\\\n"

        # Agrega una linea horizontal antes de la penultima fila
        if Ampl and i == m - 3:
            latex_code += "\\hline\n"
        if not Ampl and i == m - 2:
            latex_code += "\\hline\n"

    # Agrega la linea horizontal final y el cierre de la tabla LaTeX
    latex_code += "\\hline\n\\end{tabular}"

    return latex_code

"""
    Seguidamente, se definió la función LatexSimplexPasoAPaso, la cual tiene el objetivo de ir explicando 
    paso a paso el proceso de resolución del programa utilizando el método simplex. Lo primero que realiza 
    la función es calcular el número de filas y columnas de la matriz en formato simplex y se crea una variable 
    llamada Ejecutar que tendrá como valor True y se ejecutará hasta que se le de la instrucción contraria.
"""

def LatexSimplexPasoAPaso(Matriz, EsAmpliado):
    NFilas, NColumnas = len(Matriz), len(Matriz[0])
    Matrices = []
    Matrices.append(copy.deepcopy(Matriz))
    Ejecutar = True

    #Primera iteracion 
    print('Se comienza a resolver usando el metodo simplex. \\\ ')

    
    while(Ejecutar):
        #Si todos los coeficientes de la funcion objetivo son no negativos, se finaliza automaticamente
        if min(Matriz[NFilas-1][0:NColumnas-1])>=0:
            print('Como los coeficientes de la funcion objetivo son no negativos, se llega al fin del programa.')
            Ejecutar = False

        if Ejecutar:
            #Encontrar columna pivote, recorre la funcion objetivo y devuelve el indice del menor elemento
            columna_pivote = 0
            for i in range(0, NColumnas-1):
                if (Matriz[NFilas-1][i] < Matriz[NFilas-1][columna_pivote]):
                    columna_pivote = i
            print("\\textbf{Proceso de pivoteo}")
            print("\\begin{itemize}")
            print('\item La columna pivote es', columna_pivote+1, 'dado que', Matriz[NFilas-1][columna_pivote], ' es el menor coeficiente negativo de la funcion objetivo.')
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
                print('\item La fila pivote es', fila_pivote+1, 'dado que', str(Matriz[fila_pivote][NColumnas-1])+'/'+ str(Matriz[fila_pivote][columna_pivote]) ,'es el menor cociente no negativo.')
                
            else:
                Ejecutar = False
                T = []
                
        if Ejecutar:
            print('\item Ahora se aplica el proceso de pivoteo con el elemento pivote en la posicion ['+str(fila_pivote+1)+', '+str(columna_pivote+1)+ "].")
            
            ElementoPivote = Matriz[fila_pivote][columna_pivote]

            print('\item El elemento pivote corresponde a', ElementoPivote)
            print("\end{itemize}")
            #Primer paso pivote 
            Matriz = Escalamiento(Matriz, 1/ElementoPivote, fila_pivote+1)
            print('Se multiplica la fila ', fila_pivote+1, 'por', 1/ElementoPivote, " y se convierte en 0 los demas valores de la columna pivote en 0: ")
            
            #Segundo paso pivoteo
            for i in range(0, NFilas):
                if i != fila_pivote:
                    Valor_k = -Matriz[i][columna_pivote]
                    Matriz = Pivoteo(Matriz, i+1, Valor_k, fila_pivote+1)
            print("\\begin{center}")
            print(Tabla2LaTeX(Matriz, EsAmpliado))
            print("\end{center}")
    return Matriz

"""
    Luego, tenemos otra función llamada obtenerVector la cual recibirá el vector de restricciones y 
    a partir de este se obtendrá el vector de soluciones del programa. Primero, se genera un for para buscar 
    en que posición se tiene un 1 y a la vez se tienen ceros en las demás entradas del vector.
"""

def obtenerVector(T):
    NFilas, NColumnas = len(T), len(T[0])
    VectorSolucion = [0]*(NColumnas-1)
    for i in range(NFilas-1):
        for j in range(NColumnas-1):
            if T[i][j] == 1 and T[NFilas-1][j]==0:
                VectorSolucion[j] = T[i][NColumnas-1]
    return VectorSolucion


"""
    La siguiente función se llama Coeficiente2Funcion, la cual tiene la funcionalidad de tomar el vector de
    coeficientes y el vector de restricciones y convertirlos en un criterio de función con las variables 
    correspondientes. El código es el siguiente:
"""

def Coeficiente2Funcion(c, verCeros):
    #Esta funcion crea el string c_1x_1+c_2x_2...
    f=""
    numvariable=0 # Contador de variables
    for coeficiente in c:
        if isinstance(coeficiente, str):
            return f
        else:
            numvariable+=1
            # Verifica si quiere que se vean los 0x_i
            if verCeros:
                # Si el coeficiente es negativo o es la primera variable 
                # no hace falta agregar el +
                if coeficiente<0 or numvariable==1:
                    if coeficiente==-1: #Hacer que el -1 no se vea
                        f+=f"-x_{numvariable}"
                    elif coeficiente==1: #Hacer que el 1 no se vea
                        f+=f"x_{numvariable}"
                    else:
                        f+=str(coeficiente)+f"x_{numvariable}"
                    
                #Si el coeficiente es 0 no se agrega a la funcion
                else:
                    if coeficiente==1: #Hacer que el 1 no se vea
                        f+=f"+x_{numvariable}"
                    else:
                        f+="+"+str(coeficiente)+f"x_{numvariable}"
            else:
                if coeficiente<0 or numvariable==1:
                    if coeficiente==-1: #Hacer que el -1 no se vea
                        f+=f"-x_{numvariable}"
                    elif coeficiente==1: #Hacer que el 1 no se vea
                        f+=f"x_{numvariable}"
                    else:
                        f+=str(coeficiente)+f"x_{numvariable}"
                elif coeficiente>0:
                    if coeficiente==1: #Hacer que el 1 no se vea
                        f+=f"+x_{numvariable}"
                    else:
                        f+="+"+str(coeficiente)+f"x_{numvariable}"
    return f

"""
    La última función auxiliar se llama minimizarSujetoA, la cual crea el encabezado del programa lineal donde se 
    tiene el minimizar la función sujeto a las restricciones en código LaTeX. A partir de la función Coeficiente2Funcion 
    se crea la función objetivo y cada uno de los criterios de las restricciones, luego de eso se crea el código LaTeX 
    correspondiente a la forma usual de un programa lineal. El código se muestra a continuación:
"""

def minimizarSujetoA(c,T,z0, canonica, soloT):
    #Hace el print de minizar z sujeto a T
    
    #Verifica si se tiene z0
    if z0==0:
        z="$z="+Coeficiente2Funcion(c, canonica)+"$"
    else:
        z="$z="+Coeficiente2Funcion(c, canonica)+str(z0)+"$"
        
    
    #Inicia el vector de restricciones:
    r="$$\left\{ \n \\begin{array}{rcl}\n"
    for restriccion in T:
        if not canonica:
            if "<=" in restriccion:
                igualdad="\leq"
            if ">=" in restriccion:
                igualdad="\geq"
            if "=" in restriccion:
                igualdad="="
        else:
            igualdad="="
        b=str(restriccion[-1]) # Toma el ultimo valor de la restriccion
        r+=Coeficiente2Funcion(restriccion, canonica)+" & "+igualdad+" & "+b+"\\\ "+"\n"
    r+="\end{array} \n\\right.$$"
    
    #Print del problema inicial
    if soloT: #Si solo se quiere ver el vector de restricciones
        print(f"{r}")
    else:
        print("\\begin{center}")
        print(f"Minimizar {z} \\\ \nSujeto a las restricciones:")
        print("\end{center}")
        print(f"{r}")

"""
    Por último, se tiene la función Simplex2LaTeX, que recibe el vector de coeficientes, el vector de restricciones 
    y la constante perteneciente a la función objetivo en el caso que la tenga. 
"""

def Simplex2Latex(c,T,z0):
    
    print("Resolucion del siguiente programa lineal:")
    minimizarSujetoA(c,T,z0, False, False)
    
    # Texto explicativo de variables de holgura y superfluas
    txt1=""
    cont=0
    for restriccion in T:
        if "<=" in restriccion:
            cont+=1
            txt1+=f"La restriccion {cont} es de $\leq$, se agrega la variable de holgura $x_{cont+len(c)}$. "
        if ">=" in restriccion:
            cont+=1
            txt1+=f"La restriccion {cont} es de $\geq$, se agrega la variable superflua $x_{cont+len(c)}$. "
    print(txt1)
    
    Tabla, TieneArtificiales, Artificiales = TablaSimplexAmpliada(c, T,z0)
    
    print("Al agregar las variables de holgura y superfluas a la restriccion se obtiene:")
    minimizarSujetoA(c,T,z0, True, True)

    #Verificar si es un ejercicio con artificiales o no
    if TieneArtificiales:
        print("Note que todavia no se tienen todas las columnas del vector identidad, se deben agregar variables artificiales \\\ ")
        print("Al agregar las variables artificiales se crea la siguiente tabla simplex apliada:")
        print("\\begin{center} \n" +Tabla2LaTeX(Tabla, True)+"\n\end{center}")
        
        VectorArtificiales =[]
        for _ in Artificiales:
            VectorArtificiales.append(int(_))
        VectorArtificiales.sort(reverse=True)
        #Simplex para sistemas aumentados
        LatexSimplexPasoAPaso(Tabla, True)
        if Tabla:
            #Commpara que cada 
            SolucionProgramaAmplicado = obtenerVector(Tabla)
            Validacion = True
            for IndiceArtificial in VectorArtificiales:
                if SolucionProgramaAmplicado[(IndiceArtificial)-1] != 0:
                    Validacion = False
            if Validacion:
                print('Note que ampliado converge y como las variables artificiales son cero la penalizacion es nula. \\')
                #Proceso de poda, corregir
                print('Se elimina la ultima fila de la tabla y las columnas de las variables artificiales')
                del(Tabla[-1])
                
                for i in range(len(Tabla)):
                    for IndiceArtificial in VectorArtificiales:
                        del(Tabla[i][IndiceArtificial-1])
                print("\\begin{center}")
                print(Tabla2LaTeX(Tabla, False))
                print("\end{center}")
                print("Ahora se vuelve a realizar el metodo simplex con esta nueva tabla.")
            else:
                print('Note que el programa lineal ampliado converge pero todavia tiene variables artificiales, por lo que no tiene solucion')
                Tabla = []
        else:
            print('El programa no tiene solucion')
          
    print("Se crea la tabla simplex incial:")
    print("\\begin{center} \n" +Tabla2LaTeX(Tabla, False)+"\n\end{center}")
    Tabla = LatexSimplexPasoAPaso(Tabla,False)
    if Tabla:
        print('La solucion del programa lineal es:')
        print(obtenerVector(Tabla))
    else:
        print('Programa lineal sin solucion')
    return Tabla

