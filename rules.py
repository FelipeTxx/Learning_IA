from types import SimpleNamespace
import math
import time
from collections import Counter
estado = []
tempo_validador = 60
tempo = 2
primeiro_quadro = True
pontos_emPe = 0
pontos_sentado = 0
pontos_deitado = 0
inicio = time.monotonic()

def analisar_postura(nariz, quadril_esquerdo, quadril_direito, joelho_esquerdo, joelho_direito):
    global estado, tempo_validador, primeiro_quadro, pontos_sentado, pontos_emPe, pontos_deitado, inicio
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

    pontos_deitado = 90 - int(anguloG)
    dist = abs(centro_quadril.y - centro_joelho.y)  
    pontos_sentado = max(0, (0.4 - dist) * 100)
    pontos_emPe = (-45+int(anguloG)) - pontos_sentado
    
    if pontos_deitado > pontos_emPe and pontos_deitado > pontos_sentado:
        estado.append("Deitado")
    elif pontos_emPe > pontos_deitado and pontos_emPe > pontos_sentado:
        estado.append("Em pe")
    elif pontos_sentado > pontos_deitado and pontos_sentado > pontos_emPe:
        estado.append("Sentado")
    mais_comum = Counter(estado).most_common(1)[0][0]
    print(mais_comum)
    return str(mais_comum)