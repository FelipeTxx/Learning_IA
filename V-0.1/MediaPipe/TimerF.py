import time
tempoInicial = 0
def timerFunction(tempo):
    global tempoInicial
    if tempoInicial == 0:
        tempoInicial = time.perf_counter()
    tempoPassado = time.perf_counter() - tempoInicial
    if tempoPassado >= tempo:
        return 1
    else: return 0
    
