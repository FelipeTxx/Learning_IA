import tinytuya
from types import SimpleNamespace
import time
import math
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#from TTS.Voice_Out import def_fala
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
    'eb6cf639a85ba6907by7ss',
    '192.168.0.109',
    'CGBlNgA==+v~1Lqc'
)


lamp.set_version(3.5)

lamp.set_socketPersistent(True)
status = None
ligada = False
tempo_liberado = 0


def lightControler(get_hand):
    global tempo_liberado, ligada

    agora = time.time()

    if agora < tempo_liberado:
        return

    if get_hand.maoFechou and ligada:
        lamp.turn_off()
        ligada = False
        tempo_liberado = agora + 2  
        return ligada

    if get_hand.maoAbriu and not ligada:
        lamp.turn_on()
        ligada = True
        tempo_liberado = agora + 2
        return ligada
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



