from HandRules import calcular_mao
from TimerF import timerFunction
from types import SimpleNamespace
from collections import Counter

tempo = 0.5
mao_est = 2
braco_em_uso = 0
tempoEstavel = []
ft = 0

retorno = SimpleNamespace(
    maoFechou = True,
    maoAbriu = False,
    posicao_correta_braco = False
)

def HandMonitor_Right(lado_mao, estado_mao, ombro_esquerdo, ombro_direito, cotovelo_esquerdo, cotovelo_direito, pulso_direito, pulso_esquerdo):
    global tempo, mao_est, braco_em_uso, ft
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
        if ft == 0: retorno.posicao_correta_braco = True;ft+=1  # noqa: E701, E702
        if not retorno.posicao_correta_braco:
            retorno.posicao_correta_braco = True
            print("Posição CORRETA")
        print(mao, "   -   ",mao_est)
        if mao_est == 1 and mao == 0:
            print("Mão Fechou!!!")
            retorno.maoFechou = True
            retorno.maoAbriu = False
        elif mao_est == 0 and mao == 1:
            print("MaoAbriu!!")
            retorno.maoFechou = False
            retorno.maoAbriu = True

        mao_est = mao
    else:
        mao_est = 1
        mao = 1
        
        
        if retorno.posicao_correta_braco:
            print("Posiçao errada")
            retorno.posicao_correta_braco = False
            
    return retorno
        
    

   
        
        

            
            

