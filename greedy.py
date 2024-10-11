def obtener_moneda_mas_grande(a, b, l, r):
        if a > b:
            return a , l+1 , r
        return b, l , r-1

def obtener_moneda_mas_chica(a, b, l, r):
    if a < b:
        return a , l+1 , r
    return b, l , r-1

def main(monedas):
    contador_Sophia = 0
    contador_Mateo = 0
    l = 0
    r = len(monedas)-1
    turno_sophi = True
    while (l<=r):
        if turno_sophi:    
            m, l, r = obtener_moneda_mas_grande(monedas[l], monedas[r], l, r)
            contador_Sophia += m
            turno_sophi = False
            continue
        m, l, r = obtener_moneda_mas_chica(monedas[l], monedas[r], l, r)
        contador_Mateo += m
        turno_sophi = True

    return contador_Sophia, contador_Mateo

if __name__ == '__main__':
    main()
