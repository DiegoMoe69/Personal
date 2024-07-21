def codificar(mensaje: str):
    mensaje = mensaje.encode('utf-8')
    largo = len(mensaje)
    mensaje_codificado = largo.to_bytes(4)
    posicion = 0
    n_bloque = 0
    continuar = True
    while continuar:
        if posicion + 25 < largo:
            mensaje_codificado += (n_bloque).to_bytes(3)
            mensaje_codificado += mensaje[posicion:posicion + 25]
            posicion += 25
            n_bloque += 1

        elif posicion + 25 == largo:
            mensaje_codificado += (n_bloque).to_bytes(3)
            mensaje_codificado += mensaje[posicion:posicion + 25]
            return mensaje_codificado
        
        else:
            mensaje_codificado += (n_bloque).to_bytes(3)
            resto = posicion + 25 - largo
            mensaje_codificado += mensaje[posicion:] + b'\x00' * resto
            return mensaje_codificado

def decodificacion(mensaje_codificado: bytes):
    largo_total = len(mensaje_codificado)
    cantidad_bloques = int((largo_total - 4) / 28)
    largo = int.from_bytes(mensaje_codificado[:4])
    dicc_bloques = {}
    posicion = 4
    while posicion < largo_total:
        n_bloque = int.from_bytes(mensaje_codificado[posicion:posicion + 3])
        bloque = mensaje_codificado[posicion + 3:posicion + 28]
        dicc_bloques[n_bloque] = bloque
        posicion += 28
    mensaje_decodificado = b''
    for bloque in range(cantidad_bloques):
        mensaje_decodificado += dicc_bloques[bloque]
    mensaje_decodificado = mensaje_decodificado[:largo]
    return mensaje_decodificado.decode('utf-8')