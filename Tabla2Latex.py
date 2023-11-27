"""
    Se requiere crear una función que tome una matriz de tamaño M x N y regrese el código LaTeX correspondiente.
    Recibe una matriz y retorna un string con el codigo latex.
"""

def Tabla2LaTeX(A):
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
        if i == m - 2:
            latex_code += "\\hline\n"

    # Agrega la linea horizontal final y el cierre de la tabla LaTeX
    latex_code += "\\hline\n\\end{tabular}"

    return latex_code



A = [[1,2,31,4,1,3,1,1],
     [1,2,31,4,1,3,1,2],
     [1,2,31,4,1,3,1,3],
     [1,2,31,4,1,3,1,4],
     [1,2,31,4,1,3,1,5],
     [1,2,31,4,1,3,1,6],
     [1,2,31,4,1,3,1,7],
     [1,2,31,4,1,3,1,"z"]]

# Convierte la matriz en una tabla LaTeX 
codigo_latex = Tabla2LaTeX(A)

# Imprime el codigo LaTeX resultante
print(codigo_latex)


"""
    Salida:
                        \begin{tabular}{|ccccccc|c|}\hline
                        1 & 2 & 31 & 4 & 1 & 3 & 1 & 1  \\
                        1 & 2 & 31 & 4 & 1 & 3 & 1 & 2  \\
                        1 & 2 & 31 & 4 & 1 & 3 & 1 & 3  \\
                        1 & 2 & 31 & 4 & 1 & 3 & 1 & 4  \\
                        1 & 2 & 31 & 4 & 1 & 3 & 1 & 5  \\
                        1 & 2 & 31 & 4 & 1 & 3 & 1 & 6  \\
                        1 & 2 & 31 & 4 & 1 & 3 & 1 & 7  \\
                        \hline
                        1 & 2 & 31 & 4 & 1 & 3 & 1 & z  \\
                        \hline
                        \end{tabular}

"""