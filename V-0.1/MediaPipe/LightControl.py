import tinytuya
from types import SimpleNamespace
import time
import math
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from TTS.Voice_Out import def_fala
cooldown = 0
intervalo = False

# lamp.turn_on()
# print("Ligada!")
# time.sleep(2)

# lamp.set_colour(255, 0, 0)
# print("Vermelho!")
# time.sleep(2)

# lamp.set_colour(0, 255, 0)
# print("Verde!")
# time.sleep(2)

# lamp.set_colour(0, 0, 255)
# print("Azul!")
lamp = tinytuya.BulbDevice(
    dev_id='eb6cf639a85ba6907by7ss',
    address='192.168.0.118',
    local_key='CGBlNgA==+v~1Lqc',
    version=3.5
    )

lamp.set_socketPersistent(True)
status = lamp.status()
ligada = status['dps']['20']
def LightControl(get_hand):
    global status, ligada,cooldown,intervalo
    

    
    if get_hand.maoFechou and ligada and not intervalo:
        lamp.turn_off()
        status = lamp.status()
        ligada = False
        print("Desligou!")
        def_fala("ptMulher", "A luz do quarto Desligou!")
        intervalo = True 
        

    
        
        
    elif get_hand.maoAbriu and not ligada and not intervalo:
        lamp.turn_on()
        status = lamp.status()
        ligada = True
        print("Ligou!")
        def_fala("ptHomem", "A luz do quarto ligou!")
        intervalo = True
    
    if intervalo == True:
        cooldown+=1
        if cooldown >= 30:
            print("excedeu")
            intervalo = False
            cooldown = 0
def normalizar(valor, min_val, max_val):
    return (valor - min_val) / (max_val - min_val)
def brightControl(estado_mao, get_hand):
    global cooldown, intervalo

    indicadorAberto = estado_mao.indicador      
    indicadorTip = estado_mao.indicador_tip
    pulso = estado_mao.pulso

    centro_indicadorPulso = SimpleNamespace(
        x=(indicadorTip.x + pulso.x)/2,
        y=(indicadorTip.y + pulso.y)/2
    )

    dx = indicadorTip.x - centro_indicadorPulso.x
    dy = indicadorTip.y - centro_indicadorPulso.y

    angulo = math.atan2(dy, dx)
    
    norm = abs(normalizar(angulo, 0.01,2.70))

    if indicadorAberto and not estado_mao.polegar and not estado_mao.medio and not estado_mao.anelar and not estado_mao.mindinho and get_hand.posicao_correta_braco and not intervalo:
        intervalo = True
        if norm*1000 <= 1000:
            lamp.set_brightness(norm*1000)
       

    if intervalo:
        cooldown += 1
        if cooldown >= 15:
            cooldown = 0
            intervalo = False



