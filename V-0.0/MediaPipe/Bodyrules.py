from types import SimpleNamespace
import math
import time
from collections import Counter
from MediaDistanciaJoelhoQuadril import calcMediaJoelhoQuadril
estado = []
tempo_validador = 60
tempo = 2
primeiro_quadro = True
PtEmPe=0
Psentado=0
PDeitado=0

porcent_JQ=0
media_JQ = 0

scoreEmPe=0
scoreSentado=0
scoreDeitado=0
first = 0

inicio = time.monotonic()

def analisar_postura(nariz, quadril_esquerdo, quadril_direito, joelho_esquerdo, joelho_direito, pe_esquerdo, pe_direito):
    global estado, tempo_validador, primeiro_quadro, Psentado, PtEmPe, PDeitado, inicio, scoreEmPe,scoreSentado, scoreDeitado, maiorV_JoelhoQuadril, first, media_JQ, porcent_JQ

    

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
    centro_pe = SimpleNamespace(
        y = (pe_esquerdo.y + pe_direito.y)/2,
        x = (pe_esquerdo.x + pe_direito.x)/2
    )
    
    #diferença de x entre nariz e quadril
    dx_narizQuadril = abs(nariz.x - centro_quadril.x)
    dy_narizQuadril = abs(nariz.y - centro_quadril.y)
    #diferença de quadril e joelho
    dx_quadrilJoelho = abs(centro_quadril.x - centro_joelho.x)
    dy_quadrilJoelho = abs(centro_quadril.y - centro_joelho.y)
     #diferença de pe e joelho
    dx_peQuadril = abs(centro_pe.x - centro_quadril.x)
    dy_peQuadril = abs(centro_pe.y - centro_quadril.y)
    #angulo entre nariz e quadril
    anguloG = math.degrees(math.atan2(dy_narizQuadril, dx_narizQuadril))
    #angulo entre joelho e quadril
    anguloJQ = math.degrees(math.atan2(dy_quadrilJoelho, dx_quadrilJoelho))
    #angulo entre joelho e pe
    anguloPQ = math.degrees(math.atan2(dy_peQuadril, dx_peQuadril))


    PDeitado = 65 - int(anguloG)
    PtEmPe = anguloG
    
    
    
    if PDeitado > PtEmPe:
        estado.append("Deitado")
  
    
    elif porcent_JQ >= 2:
        estado.append("Sentado")
        media_JQ_min = calcMediaJoelhoQuadril(centro_joelho, centro_quadril)
        porcent_JQ = ((media_JQ_min.media - media_JQ_min.agora) / media_JQ_min.agora)*100
        #print(porcent_JQ)
    elif porcent_JQ < 2 and PtEmPe > PDeitado:
        media_JQ = calcMediaJoelhoQuadril(centro_joelho, centro_quadril)
        porcent_JQ = ((media_JQ.media - media_JQ.agora) / media_JQ.agora)*100
       # print(porcent_JQ) 
    if PtEmPe > PDeitado and porcent_JQ< 3:
        estado.append("Em pe")
   
        
   
    
    mais_comum = Counter(estado).most_common(1)[0][0]
    

    if mais_comum == "Em pe": scoreEmPe+=1; scoreSentado-=1; scoreDeitado-=1
    elif mais_comum == "Sentado": scoreSentado+=1; scoreDeitado-=1; scoreEmPe-=1
    elif mais_comum == "Deitado": scoreDeitado+=1; scoreEmPe-=1; scoreSentado-=1
    
    scoreEmPe = max(0, min(30, scoreEmPe))
    scoreSentado = max(0, min(30, scoreSentado))
    scoreDeitado = max(0, min(30, scoreDeitado))

    if scoreEmPe>scoreSentado and scoreEmPe>scoreDeitado: return "Em pe"
    elif scoreSentado>scoreEmPe and scoreSentado>scoreDeitado: return "Sentado"
    elif scoreDeitado>scoreEmPe and scoreDeitado>scoreSentado: return "Deitado"

    