import pygame
pygame.init()

velx = 1
vely = 1
terminar = False
x = 50
y = 100
activar = False
cont = 0
mov = False
cont_cartas = 0

win = pygame.display.set_mode((760,640))

imgA = pygame.image.load("a.jpg")
img2 = pygame.image.load("2mod.jpg")
img3 = pygame.image.load("3.jpg")
img4 = pygame.image.load("4mod.jpg")
img5 = pygame.image.load("5mod.jpg")
img6 = pygame.image.load("6mod.jpg")
img7 = pygame.image.load("7mod.jpg")
img8 = pygame.image.load("8mod.jpg")
img9 = pygame.image.load("9mod.jpg")
img10 = pygame.image.load("10mod.jpg")
imgj = pygame.image.load("jmod.jpg")
imgq = pygame.image.load("qmod.jpg")
imgk = pygame.image.load("kmod.jpg")
imgAtras = pygame.image.load("atrasmod.jpg")

img = pygame.image.load("logo.png")

array = [imgA, imgk, imgq, imgj, img10, img9, img8, img7, img6, img5, img4, img3, img2]
array_tam_image = [imgA.get_rect(), imgk.get_rect(), imgq.get_rect(), imgj.get_rect(), 
                    img10. get_rect(), img9.get_rect(), img8.get_rect(), img7.get_rect(), 
                    img6.get_rect(), img5.get_rect(), img4.get_rect(), img3.get_rect(), img2.get_rect()]
tam_image = imgAtras.get_rect()

def verificar_cartas_dibujadas(cont):
    if cont <= 13:
        for i in range(0, cont):
            tam_image = array_tam_image[i]
            win.blit(array[i], tam_image)

def definir_carta(cont):
    carta = None

    if cont < 13 and cont >= 0:
        carta = array[cont]
    return carta 

def apiladas(numero):
    left = 500
    top = 10
    tam_image_1 = None

    for i in range(0, numero+1):
        tam_image_1 = imgAtras.get_rect()
        tam_image_1.left = left         
        tam_image_1.top = top
        left += 3

        win.blit(imgAtras, tam_image_1)

    pygame.display.flip()
    return tam_image_1

def mov_true():
    win.fill((0,0,0))
    verificar_cartas_dibujadas(cont_cartas-1)
    carta = definir_carta(cont_cartas-1)

    tam_image_1 = carta.get_rect()
    tam_image_1.left = mouse_pos[0]
    tam_image_1.top = mouse_pos[1]
    
    array_tam_image[cont_cartas-1] = tam_image_1
    win.blit(carta, tam_image_1)

tam_image = apiladas(13)
while not terminar: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT : terminar = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            if cont == 0 and tam_image.collidepoint(pygame.mouse.get_pos()):
                activar = True
            else: 
                if cont%2 == 0: 
                    activar = False
                else: 
                    if tam_image.collidepoint(pygame.mouse.get_pos()):
                        activar = True
                        mov = False
            cont += 1

    mouse_pos = pygame.mouse.get_pos()
    if activar == True: 
        if mov == False and tam_image.collidepoint(pygame.mouse.get_pos()): 
            win.fill((0,0,0))
            cont_cartas += 1
            tam_image = apiladas(13-cont_cartas)
            verificar_cartas_dibujadas(cont_cartas)
            carta = definir_carta(cont_cartas-1)
            win.blit(carta, tam_image)
            mov = True
        elif mov == True: 
            mov_true()
            tam_image = apiladas(13-cont_cartas)
        else:
            tam_image = apiladas(13-cont_cartas)
    else: 
        tam_image = apiladas(13-cont_cartas)
        verificar_cartas_dibujadas(cont_cartas)

    pygame.display.flip()

pygame.quit

