'''from ast import Try
from tercero import juego'''

'''import pygame
pygame.init()

alto = 750
ancho = 900
win = pygame.display.set_mode((ancho,alto))'''

#from taller01_corte03 import listas
from menu_principal import barajas
#from win_arbol import arbol
#from taller04_corte03 import grafo

#screen = juego()
#screen_2 = listas()
screen_3 = barajas()
#screen_4 = arbol()

'''screen = grafo(win, ancho, alto)
screen.inicio_juego()'''

#prueba.draw()

#screen.crear_circulos()
#screen_2.input_screen()
screen_3.jugar_cartas(13)
#screen_4.input_information()

