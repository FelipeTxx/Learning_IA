from HandRules import calcular_mao
from TimerF import timerFunction
from types import SimpleNamespace
from collections import Counter

tempo = 0.5
mao_est = 0
braco_em_uso = 0
tempoEstavel = []

retorno = SimpleNamespace(
    maoFechou = True,
    maoAbriu = False,
    posicao_correta_braco = False
)

def HandMonitor(lado_mao, estado_mao, ombro_esquerdo, ombro_direito, cotovelo_esquerdo, cotovelo_direito, pulso_direito, pulso_esquerdo):
    global tempo, mao_est, braco_em_uso
    mao = estado_mao
    #print(ombro_direito.x, ": ombro direito     !       ", pulso_direito.x, ": cotoVelo direito")

    #Definiçao braco direito
    dfX_ombD_PlsD = abs(ombro_direito.x - pulso_direito.x)
    dfY_ombD_PlsD = abs(ombro_direito.y - pulso_direito.y)
    
    dfX_ctvD_ombD = abs(cotovelo_direito.x - ombro_direito.x)
    dfY_ctvD_ombD = abs(cotovelo_direito.y - ombro_direito.y)


    #Definiçao braco esquerdo
    dfX_ombD_PlsE = abs(ombro_esquerdo.x - pulso_esquerdo.x)
    dfY_ombD_PlsE = abs(ombro_esquerdo.y - pulso_esquerdo.y)
    
    dfX_ctvD_ombE = abs(cotovelo_esquerdo.x - ombro_esquerdo.x)
    dfY_ctvD_ombE = abs(cotovelo_esquerdo.y - ombro_esquerdo.y)

    
   
    
    
    if dfX_ombD_PlsD < 0.1  and dfY_ombD_PlsD < 0.1 and dfX_ctvD_ombD < 0.1 and dfY_ctvD_ombD < 0.1:
        retorno.posicao_correta_braco = True

        if mao == 1:   
            mao_est = 1
        if mao_est == 1 and mao == 0:
            mao_est = 0
            print("MaoFechou")
            tempoEstavel.append(1)
            
            return retorno
        
        if mao == 0:   
            mao_est = 0
        if mao_est == 0 and mao == 1:
            mao_est = 1
            print("MoaAbriu!!")
            tempoEstavel.append(2)
            
            return retorno
        else:
            tempoEstavel.append(0)
    else:
        retorno.posicao_correta_braco = False
    if len(tempoEstavel) > 40:
        mais_comum = Counter(tempoEstavel).most_common(1)[0][0]
    else:
        mais_comum = 0
   
    if mais_comum == 1:
        retorno.maoFechou = True
    elif mais_comum == 2:
        retorno.maoAbriu = True
        retorno.maoFechou = False
    else:
        retorno.maoAbriu = False
    if len(tempoEstavel) >= 2:
        del tempoEstavel[0]
            
    return retorno
        
    

   
        
        

            
            

