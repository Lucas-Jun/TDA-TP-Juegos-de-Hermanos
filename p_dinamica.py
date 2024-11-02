import sys
import set_files

PRIMERA_S = "Sophia debe agarrar la primera; "
ULTIMA_S = "Sophia debe agarrar la ultima; "
PRIMERA_M = " Mateo agarra la primera; "
ULTIMA_M = "Mateo agarra la ultima; "

def quitar_rama(l, r, m: list):
        if m[l] >= m[r]:
            return l+1, r, PRIMERA_M, m[l]
        return l, r-1, ULTIMA_M, m[r]

def solucion_dinamica(monedas: list):
    n = len(monedas)
    M = [[0 for j in range(n)] for i in range(n)]

    for largo in range(1, n+1): 
        for left_index in range(0, n-largo+1):
            right_index = left_index + largo-1 

            if largo > 2: 
                Amateo_l, Amateo_r, _, _ = quitar_rama(left_index+1, right_index, monedas)         
                Bmateo_l, Bmateo_r, _, _  = quitar_rama(left_index, right_index-1, monedas)
                
                M[left_index][right_index]= max(monedas[left_index] + M[Amateo_l][Amateo_r], monedas[right_index] + M[Bmateo_l][Bmateo_r])

            else: 
                M[left_index][right_index] = max(monedas[left_index], monedas[right_index])

    return M, M[0][n-1]

def obtener_moneda_mas_grande(a, b, l, r, prim, ult):
        if a > b:
            return a, l+1 , r, prim
        return b, l , r-1, ult

def obtener_orden(M: list, l, r, monedas: list, orden: list, cont_mateo):

    if (r-l > 2): 
        Amateo_l, Amateo_r, ladoA, ganancia_A = quitar_rama(l+1, r, monedas)         
        Bmateo_l, Bmateo_r, ladoB, ganancia_B = quitar_rama(l, r-1, monedas)
        max_l = monedas[l] + M[Amateo_l][Amateo_r]
        max_r = monedas[r] + M[Bmateo_l][Bmateo_r]

        if (max_l >= max_r):
            orden.append(PRIMERA_S)
            orden.append(ladoA)
            return obtener_orden(M, Amateo_l, Amateo_r, monedas, orden, cont_mateo + ganancia_A)
        else:
            orden.append(ULTIMA_S)
            orden.append(ladoB)
            return obtener_orden(M, Bmateo_l, Bmateo_r, monedas, orden, cont_mateo + ganancia_B)

    elif (l <= r):
        if (l-r)%2 == 0:
            ganancia, l, r, lado = obtener_moneda_mas_grande(monedas[l], monedas[r], l, r, PRIMERA_M, ULTIMA_M)
            orden.append(lado)
            return ganancia + cont_mateo
        else: 
            _, l, r, lado = obtener_moneda_mas_grande(monedas[l], monedas[r], l, r, PRIMERA_S, ULTIMA_S)
            orden.append(lado)
            return obtener_orden(M, l, r, monedas, orden, cont_mateo)
    
    return cont_mateo
        
        

if __name__ == '__main__':
    archivo_txt = sys.argv[1]
    monedas = set_files.set_coins(archivo_txt)
    M, ganancia_s = solucion_dinamica(monedas)
    orden = [] 
    ganancia_m = obtener_orden(M, 0, len(monedas)-1, monedas, orden, 0)

    set_files.set_results(ganancia_s, ganancia_m, orden, "out_p_dinamica.txt")
