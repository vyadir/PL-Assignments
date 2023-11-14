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

# Ejemplo de una matriz MxN
A = [[0.0, 0.0, 2.4285714285714284, 1.0, 0.42857142857142855, 17.0],
[1.0, 0.0, 1.1428571428571428, 0.0, 0.14285714285714285, 8.0],
[0.0, 1.0, 0.14285714285714285, 0.0, 0.14285714285714285, 4.0],
[0.0, 0.0, 2.4285714285714284, 0.0, 0.42857142857142855, 20.0]]

# Convierte la matriz en una tabla LaTeX 
codigo_latex = Tabla2LaTeX(A, False)

# Imprime el código LaTeX resultante
print(codigo_latex)