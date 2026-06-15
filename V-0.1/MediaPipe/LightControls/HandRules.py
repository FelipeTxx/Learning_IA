import math
from types import SimpleNamespace
#from collections import Counter

media_AF=[]

def calcular_mao(pulso,polegar_cmc,polegar_mcp,polegar_ip,polegar_tip,indicador_mcp,indicador_pip,indicador_dip,indicador_tip,medio_mcp,medio_pip,medio_dip,medio_tip,anelar_mcp,anelar_pip,anelar_dip,anelar_tip,mindinho_mcp,mindinho_pip,mindinho_dip,mindinho_tip):
    def dist(ax,ay,bx,by): return math.sqrt((ax-bx)**2+(ay-by)**2)

    aberto_indicador=dist(indicador_tip.x,indicador_tip.y,pulso.x,pulso.y)>dist(indicador_mcp.x,indicador_mcp.y,pulso.x,pulso.y)
    aberto_medio=dist(medio_tip.x,medio_tip.y,pulso.x,pulso.y)>dist(medio_mcp.x,medio_mcp.y,pulso.x,pulso.y)
    aberto_anelar=dist(anelar_tip.x,anelar_tip.y,pulso.x,pulso.y)>dist(anelar_mcp.x,anelar_mcp.y,pulso.x,pulso.y)
    aberto_mindinho=dist(mindinho_tip.x,mindinho_tip.y,pulso.x,pulso.y)>dist(mindinho_mcp.x,mindinho_mcp.y,pulso.x,pulso.y)
    aberto_polegar=dist(polegar_tip.x,polegar_tip.y,indicador_mcp.x,indicador_mcp.y)>dist(polegar_mcp.x,polegar_mcp.y,indicador_mcp.x,indicador_mcp.y)

    mao_aberta=aberto_indicador and aberto_medio and aberto_anelar and aberto_mindinho
    dedos=[aberto_polegar,aberto_indicador,aberto_medio,aberto_anelar,aberto_mindinho]
    qtd=sum(dedos)

    handData=SimpleNamespace(
        aberta=1 if mao_aberta else 0,
        fechada=1 if qtd==0 else 0,
        dedos_levantados=qtd,
        polegar=aberto_polegar,
        indicador=aberto_indicador,
        medio=aberto_medio,
        anelar=aberto_anelar,
        mindinho=aberto_mindinho,
        pulso=pulso,
        polegar_cmc=polegar_cmc,polegar_mcp=polegar_mcp,polegar_ip=polegar_ip,polegar_tip=polegar_tip,
        indicador_mcp=indicador_mcp,indicador_pip=indicador_pip,indicador_dip=indicador_dip,indicador_tip=indicador_tip,
        medio_mcp=medio_mcp,medio_pip=medio_pip,medio_dip=medio_dip,medio_tip=medio_tip,
        anelar_mcp=anelar_mcp,anelar_pip=anelar_pip,anelar_dip=anelar_dip,anelar_tip=anelar_tip,
        mindinho_mcp=mindinho_mcp,mindinho_pip=mindinho_pip,mindinho_dip=mindinho_dip,mindinho_tip=mindinho_tip
    )

    return handData