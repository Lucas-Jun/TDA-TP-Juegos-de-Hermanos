import sys
import set_files

def quitar_rama(l, r, m):
        if m[l] > m[r]:
            return l+1, r
        return l, r-1

def solucion_dinamica(monedas):
    n = len(monedas)
    M = [[0 for j in range(n)] for i in range(n)]

    for largo in range(1, n+1): 
        for left_index in range(0, n-largo+1):
            right_index = left_index + largo-1 

            if largo > 2: 
                Amateo_l, Amateo_r = quitar_rama(left_index+1, right_index, monedas)         
                Bmateo_l, Bmateo_r = quitar_rama(left_index, right_index-1, monedas)
                
                M[left_index][right_index]= max(monedas[left_index] + M[Amateo_l][Amateo_r], monedas[right_index] + M[Bmateo_l][Bmateo_r])
                continue

            M[left_index][right_index] = max(monedas[left_index], monedas[right_index])

    return M[0][n-1]
 
if __name__ == '__main__':
    archivo_txt = sys.argv[1]
    monedas = set_files.set_coins(archivo_txt)
    solucion_dinamica(monedas)