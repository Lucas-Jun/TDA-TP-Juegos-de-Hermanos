def obtener_moneda(a, b, l, r, turno):
    if turno:
        if a > b:
            l+=1
            return a , l , r
        r-=1
        return b, l , r
    if a < b:
        l+=1
        return a , l , r
    r-=1
    return b, l , r

def main(monedas):
    contador_Sophia = 0
    contador_Mateo = 0
    l = 0
    r = len(monedas)-1
    turno_sophi = True
    while (l<=r):
        if turno_sophi:    
            m, l, r = obtener_moneda(monedas[l], monedas[r], l, r, turno_sophi)
            contador_Sophia += m
            turno_sophi = False
            continue
        m, l, r = obtener_moneda(monedas[l], monedas[r], l, r, turno_sophi)
        contador_Mateo += m
        turno_sophi = True

    return contador_Sophia, contador_Mateo

if __name__ == '__main__':
    main()
