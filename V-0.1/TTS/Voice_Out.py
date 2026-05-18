import asyncio
import edge_tts
import tempfile
import os
import pygame
#pt-BR-FranciscaNeural   -> português Brasil, voz feminina
#pt-BR-AntonioNeural     -> português Brasil, voz masculina

async def falar(texto: str, voz: str = "en-US-GuyNeural"):
    # Salva em arquivo temporário
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        arquivo = f.name

    communicate = edge_tts.Communicate(texto, voz)
    await communicate.save(arquivo)

    # Reproduz com pygame
    pygame.mixer.init()
    pygame.mixer.music.load(arquivo)
    pygame.mixer.music.play()

    # Aguarda terminar
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    os.remove(arquivo)
def def_fala(voz_fala, texto):
    if voz_fala == "ptHomem": voz_fala = "pt-BR-AntonioNeural"
    elif voz_fala == "ptMulher": voz_fala = "pt-BR-FranciscaNeural"
    elif voz_fala == "enHomem": voz_fala = "en-US-GuyNeural"
    asyncio.run(falar(texto, voz_fala))
