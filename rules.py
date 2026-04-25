estado = ["Iniciando!"]
tempo_validador = 60
primeiro_quadro = True
def analisar_postura(nariz, quadril_esquerdo, quadril_direito, joelho_esquerdo, joelho_direito):
    global estado, tempo_validador, primeiro_quadro 
    #Verificar se esta deitado baseando-se no quadril direito
    if nariz.y >= quadril_direito.y-0.2 and nariz.y <= quadril_direito.y+0.2 and not(nariz.x >= quadril_direito.x-0.2 and nariz.x <= quadril_direito.x+0.2):       
        if primeiro_quadro:
            tempo_validador = 60 
            primeiro_quadro = False       
        tempo_validador-=1
        if tempo_validador <= 0:
            estado.append("deitado")
            print(estado[-1])            
            tempo_validador = 60 
            primeiro_quadro = True           
            return "deitado"
            
    
    '''#Verificar se esta deitado baseando-se no quadril esquerdo
    elif nariz.y >= quadril_esquerdo.y-0.2 and nariz.y <= quadril_esquerdo.y+0.2 and not(nariz.x >= quadril_esquerdo.x-0.2 and nariz.x <= quadril_esquerdo.x+0.2) and estado[-1] != "deitado":
        estado.append("deitado")
        print(estado[-1])
        return "deitado"'''
    #Verificar se esta em pé baseando-se no quadril direito
    if nariz.x >= quadril_direito.x-0.1 and nariz.x <= quadril_direito.x+0.1 and not(quadril_direito.y >= joelho_direito.y - 0.14 and quadril_direito.y <= joelho_direito.y + 0.14):
        if primeiro_quadro:
            tempo_validador = 60 
            primeiro_quadro = False     
        tempo_validador-=1  
        if tempo_validador <= 0:
            tempo_validador-=1
            estado.append("de_pe")
            print(estado[-1])
            tempo_validador = 60 
            primeiro_quadro = True        
            return "de_pe"
    #Verificar se esta em pé baseando-se no quadril esquerdo
    '''elif nariz.x >= quadril_esquerdo.x-0.1 and nariz.x <= quadril_esquerdo.x+0.1 and estado[-1] != "de_pe" and not(quadril_esquerdo.y >= joelho_esquerdo.y - 0.14 and quadril_esquerdo.y <= joelho_esquerdo.y + 0.14):
        estado.append("de_pe")
        print(estado[-1])
        return "de_pe"
    #Verificar se esta sentado a partido do joelho direito
    elif quadril_direito.y >= joelho_direito.y - 0.12 and quadril_direito.y <= joelho_direito.y + 0.12 and not(nariz.y >= quadril_direito.y-0.2 and nariz.y <= quadril_direito.y+0.2 and not(nariz.x >= quadril_direito.x-0.2 and nariz.x <= quadril_direito.x+0.2)) and estado[-1] != "sentado":
            estado.append("sentado")
            print(estado[-1])
            return "sentado"
    #Verificar se esta sentado a partido do joelho esquerdo
    elif quadril_esquerdo.y >= joelho_esquerdo.y - 0.12 and quadril_esquerdo.y <= joelho_esquerdo.y + 0.12 and not(nariz.y >= quadril_esquerdo.y-0.2 and nariz.y <= quadril_esquerdo.y+0.2 and not(nariz.x >= quadril_esquerdo.x-0.2 and nariz.x <= quadril_esquerdo.x+0.2)) and estado[-1] != "sentado":
            estado.append("sentado")
            print(estado[-1])
            return "sentado"'''
    #print(estado[-1], "ESTADO")
