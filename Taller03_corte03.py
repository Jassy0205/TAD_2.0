import pygame
import sys

class arbol():

    class Node:
        def __init__(self, value):
            self.value = value
            self.left_branch = None
            self.rigth_branch = None

    def __init__(self):
        pygame.init()

        self.alto = 850
        self.ancho = 910
        self.terminar_arbol = False
        self.terminar_1 = False
        self.terminar_combo = False

        self.user_text = ''
        self.value_input = ''

        self.base = 'Cantidad de nodos del arbol: '
        self.value = 'Valor del nodo: '
        self.input_rect = pygame.Rect(346, 5, 160, 30)

        self.numeros = 0
        self.nodes = []
        self.parents = []
        self.ubicacion = []

        self.base_font = pygame.font.Font(None, 32)
        self.base_font_2 = pygame.font.Font(None, 23)

        self.win = pygame.display.set_mode((self.ancho, self.alto))
        self.win.fill((0,0,0))

        self.root = None
        self.length = None

        self.color_menu = (255, 255, 255)
        self.color_option = (0, 0, 0)
        self.rect_combo = pygame.Rect(550, 5, 100, 25) 
        self.options = ['inorder', 'preorder', 'postorder']
        self.draw_menu = False
        self.rectas_options = []
        self.eleccion = None
        self.reccorrido = ''

    def combo_draw(self):
        pygame.draw.rect(self.win, self.color_menu, self.rect_combo, 0)
        self.img = pygame.image.load("Imagenes\descarga.png")
        self.rect_2 = pygame.Rect(550, 5, 100, 25) 
        self.rect_2.left += 100
        self.win.blit(self.img, self.rect_2)

    def borrar_informacion_combobox(self, desplegado):
        self.combo_draw()

        if desplegado == True: 
            for i, text in enumerate(self.options):
                rect = self.rect_combo.copy()

                rect.y += (i+1) * self.rect_combo.height
                self.rectas_options.insert(i, rect)
                if len(self.rectas_options) > i+1:
                    self.rectas_options.pop(i+1)

                pygame.draw.rect(self.win, self.color_menu, rect, 0)
                msg = self.base_font_2.render(text, 1, self.color_option)
                self.win.blit(msg, rect)

        if self.eleccion != None: 
            msg = self.base_font_2.render(self.eleccion, 1, (0, 0, 0))
            self.win.blit(msg, self.rect_combo)

    def insert(self, value):
        new_node = self.Node(value)

        if self.root == None:
            self.root = new_node
        else:
            def tree_route(value, node):
                if value == node.value:
                    return "El elemento ya existe"

                elif value < node.value:
                    if node.left_branch == None:
                        node.left_branch = new_node
                        return True
                    else:
                        return tree_route(value, node.left_branch)

                elif value > node.value:
                    if node.rigth_branch == None:
                        node.rigth_branch = new_node
                        return True
                    else:
                        return tree_route(value, node.rigth_branch)
                        
            tree_route(value, self.root)

    def preorder(self):
        contenedor = []
        def tree_route(node):
            contenedor.append(node.value)
            if node.left_branch != None:
                tree_route(node.left_branch)
            if node.rigth_branch != None:
                tree_route(node.rigth_branch)
        tree_route(self.root)

        self.imprimir_recorrido(contenedor)
        return print('preorder', contenedor)

    def imprimir_recorrido(self, contenedor):
        self.reccorrido = ''
        for i in range(len(contenedor)):
            self.reccorrido += str(contenedor[i])
            if i != len(contenedor) -1:
                self.reccorrido += ','

        text_surface = self.base_font.render(self.reccorrido, True, (0,255,255))
        self.win.blit(text_surface, (210,50))

    def inorder(self):
        contenedor = []
        def tree_route(node):
            if node.left_branch != None:
                tree_route(node.left_branch)
            contenedor.append(node.value)
            if node.rigth_branch != None:
                tree_route(node.rigth_branch)
        tree_route(self.root)

        self.imprimir_recorrido(contenedor)
        return print('inorder', contenedor)

    def postorder(self):
        contenedor = []
        def tree_route(node):
            if node.left_branch != None:
                tree_route(node.left_branch)
            if node.rigth_branch != None:
                tree_route(node.rigth_branch)
            contenedor.append(node.value)
        tree_route(self.root)

        self.imprimir_recorrido(contenedor)
        return print('postorder', contenedor) 

    def input_title(self):
        text_surface = self.base_font.render(self.base, True, (255,255,50))
        self.win.blit(text_surface, (30,10))

    def input_value_and_father(self):
        text_surface = self.base_font.render(self.value, True, (255,255,50))
        self.win.blit(text_surface, (30,50))

    def input_information(self):
        self.input_title()
        self.input_nodes()
        input_rect_1 = pygame.Rect(200, 45, 310, 30)
        cont = 0
        self.combo_draw()
        cont_1 = 0

        while not self.terminar_arbol:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:  self.terminar_arbol = True

                while cont < self.numeros:
                    self.input_value_and_father()
                    pygame.draw.rect(self.win, (255,255,255), input_rect_1, 2)

                    i = self.input_value(input_rect_1)

                    if  i == "Hola": 
                        cont = self.numeros

                    cont += 1

                self.separar_cadena()
                self.breadth_first_search()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos() 
                    if mouse_pos[0] >= self.rect_2.left and mouse_pos[0] <= self.rect_2.left+25:
                        if cont_1 == 0 or cont_1%2 == 0:
                            self.draw_menu = True
                        else:
                            self.win.fill((0,0,0))
                            self.borrar_info(input_rect_1)
                            self.draw_menu = False
                        cont_1+= 1

                    else:
                        if self.draw_menu == True:
                            i = 0
                            while i <= len(self.rectas_options)-1:
                                actual = self.rectas_options[i]
                                if mouse_pos[1] <= actual.top+20 and mouse_pos[1] >= actual.top and mouse_pos[0] <= actual.left+90 and mouse_pos[0] >= actual.left:
                                    self.win.fill((0,0,0))
                                    self.eleccion = self.options[i]
                                    self.elegir_recorrido()
                                    self.borrar_info(input_rect_1)
                                    self.draw_menu = False
                                i+=1

                if self.draw_menu:
                    for i, text in enumerate(self.options):
                        rect = self.rect_combo.copy()

                        rect.y += (i+1) * self.rect_combo.height
                        self.rectas_options.insert(i, rect)
                        if len(self.rectas_options) > i+1:
                            self.rectas_options.pop(i+1)

                        pygame.draw.rect(self.win, self.color_menu, rect, 0)
                        msg = self.base_font_2.render(text, 1, self.color_option)
                        self.win.blit(msg, rect)
                else:
                    self.borrar_info(input_rect_1)

            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

    def elegir_recorrido(self):
        if self.eleccion == 'inorder':
            if self.value != 'Inorder':
                self.inorder()
                self.value = 'Inorder'
        elif self.eleccion == 'preorder':
            if self.value != 'Preorder':
                self.preorder()
                self.value = 'Preorder'
        elif self.eleccion == 'postorder':
            if self.value != 'Postorder':
                self.postorder()
                self.value = 'Postorder'

    def validar_int(self, numero):
        try:
            conversion = int(numero)
            return conversion
        except:
            return False

    def input_nodes(self):
        r = 0

        while not self.terminar_1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    self.terminar_arbol = True
                    self.terminar_1 = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: 
                        self.user_text = self.user_text[:-1]
                        self.win.fill((0,0,0))
                        self.input_title()
                    elif event.key == pygame.K_SPACE:
                        self.terminar_1 = True
                    else:
                        r = self.validar_int(event.unicode)
                        print(r)

                        if r != False: 
                            self.user_text += event.unicode

            pygame.draw.rect(self.win, (255,255,255), self.input_rect, 2)
            text_surface = self.base_font.render(self.user_text, True, (0,255,255))
            self.win.blit(text_surface, (350,10))
            pygame.display.flip()

        self.numeros = int(self.user_text)
        print(self.numeros)

    def separar_cadena(self):
        separado = self.value_input.split(',')

        for i in range(0, len(separado)-1):
            self.insert(int(separado[i]))

    def input_value(self, input_rect_1):
        terminar_value = False

        while not terminar_value:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    terminar_value = True
                    return "Hola"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_COMMA:
                        self.value_input += event.unicode
                        terminar_value = True
                    elif event.key == pygame.K_BACKSPACE: 
                        self.value_input = self.value_input[:-1]
                        self.win.fill((0,0,0))
                        self.borrar_info(input_rect_1)
                    else:
                        numero = self.validar_int(event.unicode)
                        print(numero)
                        if numero != False: 
                            print(event.unicode)
                            self.value_input += event.unicode

            text_surface_1 = self.base_font.render(self.value_input, True, (0,255,255))
            self.win.blit(text_surface_1, (210,50))
            pygame.display.flip()

    def breadth_first_search(self):
        contenedor_1 = [self.root]
        contenedor_2 = [self.root.value]
        xinicial = 450
        yinicial = 100
        x = xinicial
        y = yinicial
        resta = 170
        self.draw_nodes(xinicial, yinicial, 0, 0, self.root.value)
        cont = 0

        while len(contenedor_1) != 0:
            node = contenedor_1[0]

            if cont != 0: 
                actual =  contenedor_1[0]
                xinicial = actual[2]
                yinicial = actual[1]
                y = actual[1]+100
                node = actual[0]
            else: 
                y = y + 100
                node = contenedor_1[0]

            if node.left_branch != None:
                x = xinicial - resta
                contenedor_1.append((node.left_branch, y, x))
                contenedor_2.append(node.left_branch.value)
                a = x
                self.draw_nodes(x, y, xinicial, yinicial, node.left_branch.value)
                x = xinicial
                xinicial = a
            else: 
                x = xinicial

            if node.rigth_branch != None:
                r = x
                x = x + resta
                contenedor_1.append((node.rigth_branch, y, x))
                contenedor_2.append(node.rigth_branch.value)
                self.draw_nodes(x, y, r, yinicial, node.rigth_branch.value)

            cont += 1
            contenedor_1.pop(0)

            if resta > 50:
                resta -= 15

        return print(contenedor_2)

    def draw_nodes(self, xinicial, yinicial, x, y, valor):
        if yinicial > 100:
            pygame.draw.line(self.win, (100,0,105), (x,y+10), (xinicial-5,yinicial+5), 4)

        pygame.draw.circle(self.win, (100,10,255), (xinicial,yinicial), 20, 5)

        text_surface = self.base_font.render(str(valor), True, (0,255,255))
        self.win.blit(text_surface, (xinicial-5,yinicial-10))
        
        pygame.display.flip()

    def borrar_info(self, input_rect_1):
        self.input_title()
        self.input_value_and_father()
        pygame.draw.rect(self.win, (255,255,255), self.input_rect, 2)
        pygame.draw.rect(self.win, (255,255,255), input_rect_1, 2)
        text_surface = self.base_font.render(self.user_text, True, (0,255,255))
        self.win.blit(text_surface, (350,10))
        self.borrar_informacion_combobox(False)




