import win32gui
import win32process
import psutil
import time

janela = win32gui.GetForegroundWindow()
nome_janela = win32gui.GetWindowText(janela)

while True:
    janela = win32gui.GetForegroundWindow()
    nome_janela = win32gui.GetWindowText(janela)
    print(nome_janela )
    time.sleep(1)