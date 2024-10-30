import set_files
import sys

PRIMERA_S = "Primera moneda para Sophie; "
ULTIMA_S = "Ultima moneda para Sophie; "
PRIMERA_M = "Primera moneda para Mateo; "
ULTIMA_M = "Ultima moneda para Mateo; "

def obtener_moneda_mas_grande(a, b, l, r):
        if a > b:
            return a , l+1 , r, PRIMERA_S
        return b, l , r-1, ULTIMA_S

def obtener_moneda_mas_chica(a, b, l, r):
    if a < b:
        return a , l+1 , r, PRIMERA_M
    return b, l , r-1, ULTIMA_M

def solucion_greedy(monedas):
    contador_Sophia = 0
    contador_Mateo = 0
    orden_de_monedas = []
    l = 0
    r = len(monedas)-1
    turno_sophi = True
    while (l<=r):
        if turno_sophi:    
            m, l, r, lado = obtener_moneda_mas_grande(monedas[l], monedas[r], l, r)
            contador_Sophia += m
            orden_de_monedas.append(lado)
            turno_sophi = False
            continue
        m, l, r , lado = obtener_moneda_mas_chica(monedas[l], monedas[r], l, r)
        contador_Mateo += m
        orden_de_monedas.append(lado)
        turno_sophi = True

    return contador_Sophia, contador_Mateo, orden_de_monedas

if __name__ == '__main__':
    archivo_txt = sys.argv[1]
    monedas = set_files.set_coins(archivo_txt)
    cont_s, cont_m, orden = solucion_greedy(monedas)
    set_files.set_results(cont_s, cont_m, orden, "out_greedy.txt")