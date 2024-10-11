import sys
#import greedy
#import p_dinamica

def set_coins(archivo_txt):
    with open(archivo_txt, "r") as archivo:
        lineas = archivo.readlines()

    header = True
    for linea in lineas:
        if header:
            header = False
            continue
        monedas = linea.strip().split(';')
    
    archivo.close()

    for i in range(len(monedas)):
        monedas[i] = int(monedas[i])

    return monedas

"""
    Esto estaba para la parte de obtener los pasos a realizar pero ma da paja testearlo

    def set_results(archivo_txt):
    resultados = []

    with open(archivo_txt, "r") as archivo:
        lineas = archivo.readlines()
        for linea in lineas:
            if linea[0] != 'G':
                continue
            ganancia = linea.strip().split(':')
            ganancia = int(ganancia[1])
            resultados.append(ganancia[1])

    archivo.close()

    return resultados
"""

"""
if __name__ == '__main__':
    archivo_txt = sys.argv[1]
    monedas = set_coins(archivo_txt)
    contador_Sophia= p_dinamica.main(monedas)
    print(contador_Sophia)

"""