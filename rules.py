from types import SimpleNamespace
import math
estado = ["Iniciando!"]
tempo_validador = 60
tempo = 15
primeiro_quadro = True



def analisar_postura(nariz, quadril_esquerdo, quadril_direito, joelho_esquerdo, joelho_direito):
    global estado, tempo_validador, primeiro_quadro 
    if len(estado) >= 30:
        estado.pop(0)
    centro_quadril = SimpleNamespace(
        y = (quadril_esquerdo.y + quadril_direito.y)/2,
        x = (quadril_esquerdo.x + quadril_direito.x)/2
    ) 
    centro_joelho = SimpleNamespace(
         y = (joelho_esquerdo.y + joelho_direito.y)/2,
         x = (joelho_esquerdo.x + joelho_direito.x)/2
    ) 
    #diferença de x entre nariz e quadril
    dx_narizQuadril = abs(nariz.x - centro_quadril.x)
    dy_narizQuadril = abs(nariz.y - centro_quadril.y)
    #diferença de quadril e joelho
    dx_quadrilJoelho = abs(centro_quadril.x - centro_joelho.x)
    dy_quadrilJoelho = abs(centro_quadril.y - centro_joelho.y)
    #angulo entre nariz e quadril
    anguloG = math.degrees(math.atan2(dy_narizQuadril, dx_narizQuadril))
    #angulo entre joelho e quadril
    anguloJQ = math.degrees(math.atan2(dy_quadrilJoelho, dx_quadrilJoelho))

    #print(anguloJQ)

    #Verificar se esta deitado baseando-se no angulo geral do corpo
    if anguloG <= 50:       
        if primeiro_quadro:
            tempo_validador = tempo 
            primeiro_quadro = False       
        tempo_validador-=1
        if tempo_validador <= 0:
            if estado[-1] != "deitado":
                print(estado[-1])
            estado.append("deitado")
            tempo_validador = tempo 
            primeiro_quadro = True           
            return estado
    #Verificar se esta em pé baseando-se no anguloG
    
    if anguloG > 70 and not(abs(centro_quadril.y-centro_joelho.y) <= 0.23):
        if primeiro_quadro:
            tempo_validador = tempo 
            primeiro_quadro = False     
        tempo_validador-=1  
        if tempo_validador <= 0:
            tempo_validador-=1
            if estado[-1] != "de_pe":
                print(estado[-1])
            estado.append("de_pe")
            tempo_validador = tempo 
            primeiro_quadro = True        
            return estado
    #Verificar se esta sentado a partir do angulo do joelho e quadril central e tambem pela proximidade do jeelho central com o quadril central
    if anguloJQ < 45 or abs(centro_quadril.y-centro_joelho.y) <= 0.23:
            if primeiro_quadro:
                tempo_validador = tempo 
                primeiro_quadro = False     
            tempo_validador-=1  
            if tempo_validador <= 0:
                if estado[-1] != "sentado":
                    print(estado[-1])
                estado.append("sentado")
                tempo_validador = tempo 
                primeiro_quadro = True
                return estado
    return estado

