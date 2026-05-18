from collections import Counter
from types import SimpleNamespace
maiorV_JoelhoQuadril = []

def calcMediaJoelhoQuadril(centro_joelho, centro_quadril):
    global maiorV_JoelhoQuadril
    mv_JQ_agora = centro_joelho.y-centro_quadril.y
    maiorV_JoelhoQuadril.append(mv_JQ_agora)
    mediaDeTamanho = sum(maiorV_JoelhoQuadril)/len(maiorV_JoelhoQuadril)
    medias = SimpleNamespace(
        media = (mediaDeTamanho),
        agora = mv_JQ_agora
    )
    return medias
    
        
    

