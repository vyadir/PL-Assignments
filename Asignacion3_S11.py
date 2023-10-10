# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 21:45:05 2023

@author: Andy Torres Alfaro


Descripción de la tarea:
        Toma una  matriz que representa una tabla simplex (utilizada para expresar la función objetivo y el sistema de
        restricciones de tipo igualdad) y generar el correspondiente código LaTeX con su representación visual. 
        Esta función en Python debería ser capaz de traducir la información contenida en la matriz del método simplex 
        a un formato LaTeX adecuado, considerando elementos como la función objetivo separandolas de las restricciones. 
        Llamen a esta función Tabla2LaTeX deben documentarla.

"""

def Tabla2LaTeX(A):
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
        if i == m - 2:
            latex_code += "\\hline\n"
    # Agrega la línea horizontal final y el cierre de la tabla LaTeX
    latex_code += "\\hline\n\\end{tabular}"
    return latex_code

# Ejemplo de una matriz MxN
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
# Imprime el código LaTeX resultante
print(codigo_latex)