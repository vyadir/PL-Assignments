# Simplex2Latex
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
def Tabla2LaTeX(A, Ampl):
    m = len(A)      # Calcula el número de filas de la matriz
    n = len(A[0])   # Calcula el número de columnas de la matriz
    
    # Comienza a construir el código LaTeX
    latex_code = "\\begin{tabular}{|" + "c" * (n-1) + "|c|}\\hline\n"

    # Itera sobre las filas de la matriz
    for i, fila in enumerate(A):
        # Itera sobre los elementos de cada fila
        for elemento in fila:
            # Agrega el elemento a la tabla LaTeX
            latex_code += str(elemento) + " & "

        # Elimina el último " & " de la fila y agrega una nueva línea
        latex_code = latex_code[:-2] + " \\\\\n"

        # Agrega una línea horizontal antes de la penúltima fila
        if Ampl and i == m - 3:
            latex_code += "\\hline\n"
        if not Ampl and i == m - 2:
            latex_code += "\\hline\n"

    # Agrega la línea horizontal final y el cierre de la tabla LaTeX
    latex_code += "\\hline\n\\end{tabular}"

    return latex_code

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

def LatexSimplexPasoAPaso(Matriz, EsAmpliado):
    NFilas, NColumnas = len(Matriz), len(Matriz[0])
    Matrices = []
    Matrices.append(copy.deepcopy(Matriz))
    Ejecutar = True

    #Primera iteracion 
    print('Se comienza a resolver usando el método simplex. \\\ ')

    
    while(Ejecutar):
        #Si todos los coeficientes de la funcion objetivo son no negativos, se finaliza automaticamente
        if min(Matriz[NFilas-1][0:NColumnas-1])>=0:
            print('Como los coeficientes de la función objetivo son no negativos, se llega al fin del programa.')
            Ejecutar = False

        if Ejecutar:
            #Encontrar columna pivote, recorre la funcion objetivo y devuelve el indice del menor elemento
            columna_pivote = 0
            for i in range(0, NColumnas-1):
                if (Matriz[NFilas-1][i] < Matriz[NFilas-1][columna_pivote]):
                    columna_pivote = i
            print("\\textbf{Proceso de pivoteo}")
            print("\\begin{itemize}")
            print('\item La columna pivote es', columna_pivote+1, 'dado que', Matriz[NFilas-1][columna_pivote], ' es el menor coeficiente negativo de la función objetivo.')
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
                print('\item La fila pivote es', fila_pivote+1, 'dado que', str(Matriz[fila_pivote][NColumnas-1])+'/'+ str(Matriz[fila_pivote][columna_pivote]) ,'es el menor cociente no negativo.')
                
            else:
                Ejecutar = False
                T = []
                
        if Ejecutar:
            print('\item Ahora se aplica el proceso de pivoteo con el elemento pivote en la posición ['+str(fila_pivote+1)+', '+str(columna_pivote+1)+ "].")
            
            ElementoPivote = Matriz[fila_pivote][columna_pivote]

            print('\item El elemento pivote corresponde a', ElementoPivote)
            print("\end{itemize}")
            #Primer paso pivote 
            Matriz = Escalamiento(Matriz, 1/ElementoPivote, fila_pivote+1)
            print('Se multiplica la fila ', fila_pivote+1, 'por', 1/ElementoPivote, " y se convierte en 0 los demás valores de la columna pivote en 0: ")
            
            #Segundo paso pivoteo
            for i in range(0, NFilas):
                if i != fila_pivote:
                    Valor_k = -Matriz[i][columna_pivote]
                    Matriz = Pivoteo(Matriz, i+1, Valor_k, fila_pivote+1)
            print("\\begin{center}")
            print(Tabla2LaTeX(Matriz, EsAmpliado))
            print("\end{center}")
    return Matriz

def obtenerVector(T):
    NFilas, NColumnas = len(T), len(T[0])
    VectorSolucion = [0]*(NColumnas-1)
    for i in range(NFilas-1):
        for j in range(NColumnas-1):
            if T[i][j] == 1 and T[NFilas-1][j]==0:
                VectorSolucion[j] = T[i][NColumnas-1]
    return VectorSolucion

def Coeficiente2Funcion(c, verCeros):
    #Esta función crea el string c_1x_1+c_2x_2...
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
                # no hace falta añadir el +
                if coeficiente<0 or numvariable==1:
                    if coeficiente==-1: #Hacer que el -1 no se vea
                        f+=f"-x_{numvariable}"
                    elif coeficiente==1: #Hacer que el 1 no se vea
                        f+=f"x_{numvariable}"
                    else:
                        f+=str(coeficiente)+f"x_{numvariable}"
                    
                #Si el coeficiente es 0 no se añade a la función
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
        b=str(restriccion[-1]) # Toma el último valor de la restricción
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

def Simplex2Latex(c,T,z0):
    
    print("Resolución del siguiente programa lineal:")
    minimizarSujetoA(c,T,z0, False, False)
    
    # Texto explicativo de variables de holgura y superfluas
    txt1=""
    cont=0
    for restriccion in T:
        if "<=" in restriccion:
            cont+=1
            txt1+=f"La restricción {cont} es de $\leq$, se añade la variable de holgura $x_{cont+len(c)}$. "
        if ">=" in restriccion:
            cont+=1
            txt1+=f"La restricción {cont} es de $\geq$, se añade la variable superflua $x_{cont+len(c)}$. "
    print(txt1)
    
    Tabla, TieneArtificiales, Artificiales = TablaSimplexAmpliada(c, T,z0)
    
    print("Al añadir las variables de holgura y superfluas a la restricción se obtiene:")
    minimizarSujetoA(c,T,z0, True, True)

    #Verificar si es un ejercicio con artificiales o no
    if TieneArtificiales:
        print("Note que todavía no se tienen todas las columnas del vector identidad, se deben añadir variables artificiales \\\ ")
        print("Al añadir las variables artificiales se crea la siguiente tabla simplex apliada:")
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
                print('Note que ampliado converge y cómo las variables artificiales son cero la penalización es nula. \\')
                #Proceso de poda, corregir
                print('Se elimina la última fila de la tabla y las columnas de las variables artificiales')
                del(Tabla[-1])
                
                for i in range(len(Tabla)):
                    for IndiceArtificial in VectorArtificiales:
                        del(Tabla[i][IndiceArtificial-1])
                print("\\begin{center}")
                print(Tabla2LaTeX(Tabla, False))
                print("\end{center}")
                print("Ahora se vuelve a realizar el método simplex con esta nueva tabla.")
            else:
                print('Note que el programa lineal ampliado converge pero todavía tiene variables artificiales, por lo que no tiene solución')
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

c = [135,180,452,235]
T = [[1,1,7,7, '>=', 4],
     [2,7,3,-7,'>=', 6],
     [3,7,-6,1, '>=', 5],
     [6,7,2,-3, '>=', 7]]
z0=0


Simplex2Latex(c,T,z0)

