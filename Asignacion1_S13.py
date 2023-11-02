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

