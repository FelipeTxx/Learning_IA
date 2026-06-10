postura_anterior = None

def verificar_postura(postura):
    global postura_anterior
    if postura != postura_anterior:
        postura_anterior = postura
        if postura != None:
            print(postura, " // post")