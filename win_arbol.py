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

        self.alto = 750
        self.ancho = 900
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
        self.options = ['inorder', 'preorder', 'postorder', 'amplitud']
        self.draw_menu = False
        self.rectas_options = []
        self.eleccion = None
        self.reccorrido = ''

    #Metodo que dibuja el combobox en pantalla
    def combo_draw(self):
        pygame.draw.rect(self.win, self.color_menu, self.rect_combo, 0)
        self.img = pygame.image.load("Imagenes\descarga.png")
        self.rect_2 = pygame.Rect(550, 5, 100, 25) 
        self.rect_2.left += 100
        self.win.blit(self.img, self.rect_2)

    #metodo que después de haberse extendido el combobox, lo dibuja de nuevo
    #y de haberse escogido algunas de las opciones del combobox, la coloca arriba
    def borrar_informacion_combobox(self, desplegado):
        self.combo_draw()

        if self.eleccion != None: 
            msg = self.base_font_2.render(self.eleccion, 1, (0, 0, 0))
            self.win.blit(msg, self.rect_combo)

    #Se crea un metodo que inserta cada valor de ingresado como equivalencia
    #a los nodos en una lista con la estructura de un arbol binario
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

    #Metodo que retorna una lista con los valores de los nodos en preorder 
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
    
    #Metodo que retorna una lista con los valores de los nodos en preorder 
    def amplitud(self):
        contenedor_1 = [self.root]
        contenedor_2 = [self.root.value]
        while len(contenedor_1) != 0:
            node = contenedor_1[0]
            if node.left_branch != None:
                contenedor_1.append(node.left_branch)
                contenedor_2.append(node.left_branch.value)
            if node.rigth_branch != None:
                contenedor_1.append(node.rigth_branch)
                contenedor_2.append(node.rigth_branch.value)
            contenedor_1.pop(0)
        
        self.imprimir_recorrido(contenedor_2)
        return print(contenedor_2)

    #Metodo que muestra en pantalla el recorrido (en forma de lista) que se haya elegido
    #la lista ya traída de los metodos de preorder, inorder o postorder entra como parametro
    def imprimir_recorrido(self, contenedor):
        self.reccorrido = ''
        for i in range(len(contenedor)):
            self.reccorrido += str(contenedor[i])
            if i != len(contenedor) -1:
                self.reccorrido += ','

        text_surface = self.base_font.render(self.reccorrido, True, (0,255,255))
        self.win.blit(text_surface, (210,50))

    #Metodo que retorna una lista con los valores de los nodos en inorder
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

    #Metodo que retorna una lista con los valores de los nodos en postorder 
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

    #Se crea una función que imprima el titulo del primer input: El número de nodos a dibujar
    def input_title(self):
        text_surface = self.base_font.render(self.base, True, (0,255,255))
        self.win.blit(text_surface, (30,10))

    #función que imprima el titulo del input de los valores de los nodos
    def input_value_and_father(self):
        text_surface = self.base_font.render(self.value, True, (0,255,255))
        self.win.blit(text_surface, (30,50))

    #Función que acciona todo el proceso del arbol
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

                #se verifica que el numero de valores ingresado sea equivalente al numero de nodos
                while cont < self.numeros:
                    self.input_value_and_father()
                    pygame.draw.rect(self.win, (255,255,255), input_rect_1, 2)

                    i = self.input_value(input_rect_1)

                    if  i == "Hola": 
                        cont = self.numeros

                    cont += 1

                #Se llama un metodo que separa el string con los valores de los nodos y los ingresa a un vector
                self.separar_cadena()
                #Se llama al metodo que establecerá la posición de los nodos y los dibujará
                self.breadth_first_search()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos() 

                    #Se verifica que la ubicación del mouse esté sobre la recta del combobox
                    if mouse_pos[0] >= self.rect_2.left and mouse_pos[0] <= self.rect_2.left+25:
                        #Se lleva una cuenta de los clicks para verificar el despliegue del menú
                        if cont_1 == 0 or cont_1%2 == 0:
                            self.draw_menu = True
                        else:
                            self.win.fill((0,0,0))
                            self.borrar_info(input_rect_1)
                            self.draw_menu = False
                        cont_1+= 1

                    else:
                        #Se verifica que el menú del 'combobox' esté desplegado
                        if self.draw_menu == True:

                            i = 0
                            #Se recorren las opciones posibles
                            while i <= len(self.rectas_options)-1:
                                actual = self.rectas_options[i]

                                #Se verifica que la posición del mouse esté sobre la recta de la opción actual
                                if mouse_pos[1] <= actual.top+20 and mouse_pos[1] >= actual.top and mouse_pos[0] <= actual.left+90 and mouse_pos[0] >= actual.left:
                                    self.win.fill((0,0,0))
                                    self.eleccion = self.options[i]
                                    self.elegir_recorrido()
                                    self.borrar_info(input_rect_1)
                                    self.draw_menu = False
                                i+=1

                #Se verifica que se quieran desplegar las opciones del combobox
                if self.draw_menu:
                    for i, text in enumerate(self.options):
                        rect = self.rect_combo.copy()

                        #Se va aumentando el valor de y de la recta a medida que se pasa a la opción siguiente
                        rect.y += (i+1) * self.rect_combo.height
                        #Se agrega la posición de cada opción posibre a un vector
                        self.rectas_options.insert(i, rect)
                        #y se verifica el tamaño de la lista para en caso de haber más de las 
                        #necesarias, eliminar el excedente 
                        if len(self.rectas_options) > i+1:
                            self.rectas_options.pop(i+1)

                        pygame.draw.rect(self.win, self.color_menu, rect, 0)
                        msg = self.base_font_2.render(text, 1, self.color_option)
                        self.win.blit(msg, rect)
                else:
                    self.borrar_info(input_rect_1)

            pygame.display.flip()

    #Se crea un metodo que valide la eleccion del recorrido que se desee realizar
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
        elif self.eleccion == 'amplitud':
            if self.value != 'Amplitud':
                self.amplitud()
                self.value = 'Amplitud'

    #Se crea un metodo que valide que el dato ingresado corresponda a un valor entero
    def validar_int(self, numero):
        try:
            conversion = int(numero)
            return conversion
        except:
            return False

    #Metodo que reciba la información del input del número de nodos
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

        if self.user_text != '' and self.user_text != None:
            self.numeros = int(self.user_text)
            print(self.numeros)
        else:
            self.numeros = None

    #Metodo que separa los valores de los nodos ingresados, 
    #dividiendo el string utilizando el separador ','
    def separar_cadena(self):
        separado = self.value_input.split(',')

        for i in range(0, len(separado)-1):
            self.insert(int(separado[i]))

    def verifica_valor_existente(self, input_rect_1):
        separado = self.value_input.split(',')
        final = len(separado)-1
        print(separado[final-1], final-1)
        cont = separado.count(separado[final-1])

        print(len(self.value_input)-2)
        if cont > 1:
            self.value_input = self.value_input[:-1]
            while self.value_input[len(self.value_input)-1] != ',':
                self.value_input = self.value_input[:-1]

            self.win.fill((0,0,0))
            self.borrar_info(input_rect_1)
            self.cont_arbol = self.cont_arbol - (cont - 1)

    #Metodo que reciba la información del input del valor del nodo a ingresar
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
                        self.verifica_valor_existente(input_rect_1)
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

    #Metodo que estable la ubicacion de los nodos, y llama a la función que los dibuja
    def breadth_first_search(self):
        contenedor_1 = [self.root]
        contenedor_2 = [self.root.value]
        xinicial = 450
        yinicial = 130
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

    #Metodo que dibuja cada uno de los valores de los nodos en el arbol
    def draw_nodes(self, xinicial, yinicial, x, y, valor):
        if yinicial > 130:
            pygame.draw.line(self.win, (255,255,255), (x,y+10), (xinicial-5,yinicial+5), 4)

        #(100,0,105) color linea, (100,10,255) color circulo
        pygame.draw.circle(self.win, (255,255,255), (xinicial,yinicial), 20, 20)

        text_surface = self.base_font.render(str(valor), True, (0,0,0))

        if valor >= 10:
            xinicial = xinicial-6

        self.win.blit(text_surface, (xinicial-5,yinicial-10))
        
        pygame.display.flip()

    #Metodo que resetea la pantalla y luego dibuja las cuadriculas del input de value y nodes,
    # y llama a la función que dibuja al 'combobox'
    def borrar_info(self, input_rect_1):
        self.input_title()
        self.input_value_and_father()
        pygame.draw.rect(self.win, (255,255,255), self.input_rect, 2)
        pygame.draw.rect(self.win, (255,255,255), input_rect_1, 2)
        text_surface = self.base_font.render(self.user_text, True, (0,255,255))
        self.win.blit(text_surface, (350,10))
        self.borrar_informacion_combobox(False)




