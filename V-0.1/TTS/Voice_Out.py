import asyncio
import threading
import edge_tts
import tempfile
import os
import hashlib
import pygame

# pt-BR-FranciscaNeural -> portugues Brasil, voz feminina
# pt-BR-AntonioNeural   -> portugues Brasil, voz masculina

fala_lock = threading.Lock()
falando = False
PASTA_CACHE = os.path.join(os.path.dirname(__file__), "cache")


def obter_arquivo_cache(texto, voz):
    os.makedirs(PASTA_CACHE, exist_ok=True)
    chave = f"{voz}|{texto}".encode("utf-8")
    nome_arquivo = hashlib.md5(chave).hexdigest() + ".mp3"
    return os.path.join(PASTA_CACHE, nome_arquivo)


async def falar(texto: str, voz: str = "en-US-GuyNeural"):
    arquivo = obter_arquivo_cache(texto, voz)

    if not os.path.exists(arquivo):
        communicate = edge_tts.Communicate(texto, voz)
        await communicate.save(arquivo)

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(arquivo)
        pygame.mixer.music.play()

        # Aguarda o fim do audio sem bloquear o loop principal do projeto.
        while pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        if pygame.mixer.get_init():
            pygame.mixer.quit()


def tocar_fala_em_background(texto, voz):
    global falando

    with fala_lock:
        if falando:
            return

        falando = True
        try:
            asyncio.run(falar(texto, voz))
        finally:
            falando = False


def def_fala(voz_fala, texto):
    if voz_fala == "ptHomem":
        voz_fala = "pt-BR-AntonioNeural"
    elif voz_fala == "ptMulher":
        voz_fala = "pt-BR-FranciscaNeural"
    elif voz_fala == "enHomem":
        voz_fala = "en-US-GuyNeural"

    threading.Thread(
        target=tocar_fala_em_background,
        args=(texto, voz_fala),
        daemon=True
    ).start()
