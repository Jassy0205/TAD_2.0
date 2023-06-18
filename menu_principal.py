import pygame
import sys
import random
import unicodedata

from grafos import grafo

class barajas():
    #Se crea la clase nodo
    class _Nodo:
        #Se hace el metodo incializador de la clase nodo
        def __init__(self, valor):
            self.valor = valor
            self.nodo_siguiente = None

    #Se crea la clase nodo del arbol
    class Node:
        #Se hace el metodo incializador de la clase nodo
        def __init__(self, value):
            self.value = value
            self.left_branch = None
            self.rigth_branch = None

    #Se hace el metodo incializador de la clase barajas
    def __init__(self):
        pygame.init()

        self.n_cartas = 0

        self.cabeza = None
        self.cola = None
        self.tamaño = 0

        self.alto = 750
        self.ancho = 900
        self.terminar = False
        self.terminar_1 = False
        self.terminar_arbol = False
        self.terminar_combo = False
        self.terminar_grafo = False

        #variable creada para guardar la información de la posición
        #en la que estaba la imagen que se está moviendo
        self.posicion_inicial = None

        #Se establecen las inscripciones que tendrán los input para el arbol
        self.base = 'Cantidad de nodos del arbol: '
        self.value = 'Valor del nodo: '
        self.input_rect =  pygame.Rect(346, 5, 160, 30)

        #Se crean las variables que serán utilizadas para el arbol
        self.user_text = ''
        self.value_input = ''
        self.numeros = 0
        self.base_font_2 = pygame.font.Font(None, 23)
        self.base_font_3 = pygame.font.Font(None, 28)
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
        self.cont_arbol = 0

        #Se establecen la inscripción que tendrán los botones
        self.base1 = 'Pilas'
        self.base2 = 'Árboles'
        self.base3 = 'Grafos'

        #Se crean tres rectangulos para los botones
        self.input_rect1 = pygame.Rect(60, 10, 100, 30)
        self.input_rect2 = pygame.Rect(190, 10, 100, 30)
        self.input_rect3 = pygame.Rect(320, 10, 100, 30)

        #Función para cargar todas las imagenes para el juego
        self.carga_imagenes()

        #Se crean las variables que serán utilizadas para la pila
        self.array = []
        self.array_tam_image = []
        self.mov_mouse_1() 
        self.terminar_pila = False

        #Se crean las variables con la ubicación de cada una de las rectas que corresponden a las diferentes pilas
        self.rect1 = pygame.Rect(20, 200, 95, 166)
        self.rect2 = pygame.Rect(130, 200, 95, 166)
        self.rect3 = pygame.Rect(240, 200, 95, 166)
        self.rect4 = pygame.Rect(350, 200, 95, 166)
        self.rect5 = pygame.Rect(460, 200, 95, 166)
        self.rect6 = pygame.Rect(570, 200, 95, 166)
        self.rect7 = pygame.Rect(680, 200, 95, 166)
        self.r1 = pygame.Rect(350, 10, 95, 166)

        #Se crea el vector que guardará las copias que han sido creadas en el metodo posterior
        self.vector_copy_imagenes = []

        #Se crean unas copias de estas posiciones iniciales de las pilas
        self.crear_copias()

        #Se crean los vectores de cada pila que guardarán las cartas que haya en cada una de ellas
        self.pila1 = []
        self.pila2 = []
        self.pila3 = []
        self.pila3 = []
        self.pila4 = []
        self.pila5 = []
        self.pila6 = []
        self.pila7 = []
        self.pila8 = []

        #Se crea la variable que guarda la posición de la carta que será girada
        self.voltear = None

        #variable que indica la pila en la que estaba la carta a la que se le está dando movimiento
        self.mov_pila1 = False
        self.mov_pila2 = False
        self.mov_pila3 = False
        self.mov_pila4 = False
        self.mov_pila5 = False
        self.mov_pila6 = False
        self.mov_pila7 = False
        self.mov_pila8 = False

        #Se crean unos contadores para llevar una noción del numero de cartas disponibles en cada pila
        self.cont_pila1 = 3
        self.cont_pila2 = 3
        self.cont_pila3 = 3
        self.cont_pila4 = 3
        self.cont_pila5 = 3
        self.cont_pila6 = 3
        self.cont_pila7 = 3
        self.cont_pila8 = 0
        
        #variable utilizada para guardar la información de la imagen extraida de las pilas inferiores
        self.tam_image_2 = None
        self.imagen_mov = None

        #variables para grafos
        self.combo_1 = 'Origen:'
        self.draw_menu_1 = False
        self.rect_combo_1 = pygame.Rect(30, 100, 100, 25) 
        self.eleccion_1 = None
        self.rectas_options_1 = []

        self.combo_2 = 'Destino:'
        self.draw_menu_2 = False
        self.rect_combo_2 = pygame.Rect(190, 100, 100, 25) 
        self.eleccion_2 = None
        self.rectas_options_2 = []

        self.img_mapa = pygame.image.load("Imagenes\MapaColombia.jpg")
        self.tam_mapa_rect =  None

        self.combo_3 = 'Arista:'
        self.input_rect_origen = pygame.Rect(115, 817, 126, 25) 
        self.user_text_origen = ""
        self.input_rect_destino = pygame.Rect(372, 817, 126, 25) 
        self.user_text_destino = ""
        self.input_rect_arista = pygame.Rect(610, 817, 70, 25) 
        self.user_text_arista = ""

        self.text_dijktra = 'Dijktra'
        self.rect_dijk = pygame.Rect(30, 60, 125, 25) 
        self.algorithm_dijktra = False
        self.recorrido_corto = None

        self.text_rutas = 'rutas'
        self.rect_rutas = pygame.Rect(190, 60, 125, 25) 
        self.mostrar_rutas = False

        self.combo_4 = "Selected"
        self.rect_select_arista = pygame.Rect(750, 707, 115, 25) 

        self.ciudades = ['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena',
                            'Cúcuta', 'Leticia', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Riohacha',
                            'Santa Marta', 'Valledupar', 'Villavicencio']
        self.relaciones = []
        self.rectas_ciudades = []
        self.dictionary_relations = None
        self.grafos = []
        self.otros = []

        self.negro = (0,0,0)
        self.blanco = (255,255,255)
        self.rojo = (100,30,22)

        #Se le da el tipo de letra y el tamaño de la letra que será utilizada para los botones
        self.base_font = pygame.font.Font(None, 32)

        #Se dibuja la ventana con las especificaciones de ancho y alto establecidas 
        # y se le da el color negro 
        self.win = pygame.display.set_mode((self.ancho, self.alto))
        self.win.fill((0,0,0))

    #Se hace un metodo que carga las imagenes necesarias para desarrollar la pila
    # y las ingresa a un vector 
    def carga_imagenes(self):
        #Se instancian a cada una de las imagenes
        self.imgA = pygame.image.load("a.jpg")
        self.img2 = pygame.image.load("2mod.jpg")
        self.img3 = pygame.image.load("3.jpg")
        self.img4 = pygame.image.load("4mod.jpg")
        self.img5 = pygame.image.load("5mod.jpg")
        self.img6 = pygame.image.load("6mod.jpg")
        self.img7 = pygame.image.load("7mod.jpg")
        self.img8 = pygame.image.load("8mod.jpg")
        self.img9 = pygame.image.load("9mod.jpg")
        self.img10 = pygame.image.load("10mod.jpg")
        self.imgj = pygame.image.load("jmod.jpg")
        self.imgq = pygame.image.load("qmod.jpg")
        self.imgk = pygame.image.load("kmod.jpg")
        self.imgAtras = pygame.image.load("atrasmod.jpg")

        self.Aca = pygame.image.load("Aca.png")
        self.I4ca = pygame.image.load("4ca.png")
        self.I5ca = pygame.image.load("5ca.png")
        self.Ijca = pygame.image.load("Jca.png")
        self.IQca = pygame.image.load("Qca.png")

        self.Ic2 = pygame.image.load("2c.png")
        self.Ic6 = pygame.image.load("6c.png")
        self.Ic7 = pygame.image.load("7c.png")
        self.Ic8 = pygame.image.load("8c.png")
        self.Ic10 = pygame.image.load("10c.png")
        self.IcQ = pygame.image.load("Qc.png")
        self.Ick = pygame.image.load("Kc.png")

        self.imagenes = [self.I4ca, self.IcQ, self.Ic6, self.Ic2, self.Ic7, self.Ic10, self.IQca, self.Ick, self.Ijca, self.I5ca, self.Aca, self.Ic8, self.img9, self.img3]

    #Se crean los cuatro botones que serán utilizados
    def crear_botones(self):
        pygame.draw.rect(self.win, (255,255,255), self.input_rect1)
        pygame.draw.rect(self.win, (255,255,255), self.input_rect2)
        pygame.draw.rect(self.win, (255,255,255), self.input_rect3)

        text_surface = self.base_font.render(self.base1, True, (0,0,0))
        self.win.blit(text_surface, (self.input_rect1.x + (self.input_rect1.width - text_surface.get_width()) / 2, (self.input_rect1.y + (self.input_rect1.height - text_surface.get_height())/2)))

        text_surface = self.base_font.render(self.base2, True, (0,0,0))
        self.win.blit(text_surface, (self.input_rect2.x + (self.input_rect2.width - text_surface.get_width()) / 2, (self.input_rect2.y + (self.input_rect2.height - text_surface.get_height())/2)))

        text_surface = self.base_font.render(self.base3, True, (0,0,0))
        self.win.blit(text_surface, (self.input_rect3.x + (self.input_rect3.width - text_surface.get_width()) / 2, (self.input_rect3.y + (self.input_rect3.height - text_surface.get_height())/2)))

    #Se crea un metodo que muestre todas las cartas apiladas
    def cartas_apiladas(self, jugando):
        left = 600
        top = 10

        for i in range(0, jugando):
            tam_image = self.imgAtras.get_rect()
            tam_image.left = left         
            tam_image.top = top
            left += 3

            self.win.blit(self.imgAtras, tam_image)

    #Metodo para agregar nodos a la pila
    def enqueue(self, valor):
        # Agrega un elemento al final de la queue
        nuevo_nodo = self._Nodo(valor)
        if self.cabeza == None and self.cola == None:
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.nodo_siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.tamaño += 1

    #Metodo que convierte la pila en un array 
    def mostrar_cola1(self, n_cartas):
        # Muestra los elementos de la queue
        array = []
        nodo_actual = self.cabeza
        cont = 0

        while nodo_actual != None and cont < n_cartas:
            array.append(nodo_actual.valor)
            nodo_actual = nodo_actual.nodo_siguiente
            cont+=1

        return array

    #Se crea un metodo que cree los botones, y realice las funciones según el botón que sea seleccionado
    def jugar_cartas(self, numero_cartas):
        self.n_cartas = numero_cartas
        self.crear_botones()
        self.cartas_apiladas(self.n_cartas)
        cont = 0
        cont_cartas = 0
        mov = False

        while not self.terminar:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.terminar = True
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 

                    if self.input_rect1.collidepoint(pygame.mouse.get_pos()):
                        self.terminar_pila = False
                        self.win.fill((25,111,61))
                        self.tam_image = self.apiladas(13)
                        cont_cartas = self.control_pila_mouse(cont_cartas)
                        self.win.fill((0,0,0))
                        self.crear_botones()
                        self.cartas_apiladas(numero_cartas)

                    elif self.input_rect2.collidepoint(pygame.mouse.get_pos()):
                        self.terminar_arbol = False
                        self.win.fill((0,0,0))
                        self.input_information()
                        self.win.fill((0,0,0))
                        self.crear_botones()
                        self.cartas_apiladas(numero_cartas)

                    elif self.input_rect3.collidepoint(pygame.mouse.get_pos()):
                        self.terminar_grafo = False
                        self.win.fill((0,0,0))

                        screen = grafo(self.win, self.ancho, self.alto)
                        screen.inicio_juego()

                        
                        self.win.fill((0,0,0))
                        self.crear_botones()
                        self.cartas_apiladas(numero_cartas)

            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

    #-------------------------------- Arbol -------------------------------

    #Metodo que dibuja el combobox en pantalla
    def combo_draw(self):
        pygame.draw.rect(self.win, self.color_menu, self.rect_combo, 0)
        self.img = pygame.image.load("descarga.png")
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
        text_surface = self.base_font.render(self.base, True, (255,255,50))
        self.win.blit(text_surface, (30,10))

    #función que imprima el titulo del input de los valores de los nodos
    def input_value_and_father(self):
        text_surface = self.base_font.render(self.value, True, (255,255,50))
        self.win.blit(text_surface, (30,50))

    #Función que acciona todo el proceso del arbol
    def input_information(self):
        self.input_title()
        self.input_nodes()
        input_rect_1 = pygame.Rect(200, 45, 310, 30)
        self.combo_draw()
        cont_1 = 0

        while not self.terminar_arbol:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:  self.terminar_arbol = True

                #se verifica que el numero de valores ingresado sea equivalente al numero de nodos
                while self.cont_arbol < self.numeros:
                    self.input_value_and_father()
                    pygame.draw.rect(self.win, (255,255,255), input_rect_1, 2)

                    i = self.input_value(input_rect_1)

                    if  i == "Hola": 
                        self.cont_arbol = self.numeros

                    self.cont_arbol += 1

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

        self.numeros = int(self.user_text)
        print(self.numeros)

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

                        if numero != False: 
                            self.value_input += event.unicode

            text_surface_1 = self.base_font.render(self.value_input, True, (0,255,255))
            self.win.blit(text_surface_1, (210,50))
            pygame.display.flip()

    #Metodo que estable la ubicacion de los nodos, y llama a la función que los dibuja
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

        return contenedor_2

    #Metodo que dibuja cada uno de los valores de los nodos en el arbol
    def draw_nodes(self, xinicial, yinicial, x, y, valor):
        if yinicial > 100:
            pygame.draw.line(self.win, (100,0,105), (x,y+10), (xinicial-5,yinicial+5), 4)

        pygame.draw.circle(self.win, (100,10,255), (xinicial,yinicial), 20, 5)

        text_surface = self.base_font.render(str(valor), True, (0,255,255))
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

    #----------------------------- Pila --------------------------------

    #Se desarrolla un metodo que controle los movimientos del mouse y el teclado una vez que se ha presionado el botón 'pila'
    def control_pila_mouse(self, cont_cartas):
        #Se crean las variables locales que serán utilizadas al dibujar las cartas
        activar = False
        cont = 0
        mov = False
        i = -1
        otros = False
        hola = False
        abajo = False
        carta_pila_superior = None


        #Se inicia in ciclo que abre una interfaz para organizar las cartas de la pila
        #ciclo que termina al darle en la x de la interfaz grafica
        while not self.terminar_pila: 
            if len(self.vector_copy_imagenes) == 0: 
                self.crear_imagenes_pilas()

            for event in pygame.event.get():
                if event.type == pygame.QUIT : self.terminar_pila = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                    
                    hola = self.carta_actual_collision_2()
                    if hola == True: 
                        activar = True
                        hola = False

                    #Se lleva un control de clicks para definir en que momento hacer que acción
                    elif cont == 0 and self.tam_image.collidepoint(pygame.mouse.get_pos()):
                        #self.apiladas(13)
                        activar = True
                        carta = self.imgAtras
                    else: 
                        if cont%2 == 0: 
                            i = self.carta_actual_collision(mov)
                            #Se pregunta si la carta que se desea mover está en la pila o ya salió de ella
                            if i != -1: 
                                activar = True
                                mov = False
                                carta = self.array[i]
                                otros = True
                                print('aja4')
                            else:
                                activar = False
                                mov = False
                                otros = False
                                print('aja3')
                                if abajo: 
                                    mouse_pos = pygame.mouse.get_pos()
                                    self.ingreso_nueva_pila(mouse_pos, self.imagen_mov)
                                    abajo = False
                                else:
                                    print(carta_pila_superior)
                                    mouse_pos = pygame.mouse.get_pos()
                                    self.ingreso_nueva_pila(mouse_pos, carta_pila_superior)
                        else: 
                            #Se llega a esta parte cuando ya se quiere dejar la carta en un lugar 
                            #especifico de la pantalla
                            if self.tam_image.collidepoint(pygame.mouse.get_pos()):
                                self.tam_image = self.imgAtras.get_rect()
                                carta = self.imgAtras
                                activar = True
                                mov = False
                                print('aja')
                    cont += 1

            #Se extrae la posición del mouse
            mouse_pos = pygame.mouse.get_pos()
            if activar == True: 
                #Se posiciona la carta que sigue en la pila, una vez que se ha seleccionado la misma
                if mov == False and self.tam_image.collidepoint(pygame.mouse.get_pos()): 
                    self.win.fill((25,111,61))
                    if not otros:
                        cont_cartas += 1
                        self.tam_image = self.apiladas(13)
                        carta = self.definir_carta(cont_cartas-1)

                        if carta != None:
                            self.win.blit(carta, self.tam_image)

                    mov = True
                elif self.carta_actual_collision_2() and mov == False and self.tam_image_2.collidepoint(pygame.mouse.get_pos()): 
                    print("whatsaap")
                    mov = True
                    abajo = True
                    #self.posicion_inicial = self.imagen_mov.get_rect()
                    self.quitar_carta_mov_pila()
                #Se resetea la pantalla y se le da movimiento con el mouse a la imagen seleccionada
                elif mov == True: 
                    #Se pregunta si es una carta recién sacada de la pila o si ya estaba
                    #haciendo uso de la variable 'otros'
                    if not otros and not abajo:
                        carta_pila_superior = self.mov_true(cont_cartas, mouse_pos)
                        self.tam_image = self.apiladas(13)
                    elif abajo: 
                        self.apiladas(13)
                        self.mov_true_3(cont_cartas, mouse_pos)
                #Se deja la carta en la ulitima posición que tomó mientras se movía
                else:
                    #Se pregunta si es una carta recién sacada de la pila o si ya estaba
                    #haciendo uso de la variable 'otros'
                    if not otros:
                        self.tam_image = self.apiladas(13)
                    else: 
                        self.tam_image = self.imgAtras.get_rect()
                        carta = self.imgAtras
                        self.apiladas(13)
                        print('aja2')
                        otros = False

            self.apiladas(13)
            pygame.display.flip()

        return cont_cartas

    #con este metodo se verifica la posicion del mouse en la pantalla para establecer la pila donde se ingresaría la carta
    def ingreso_nueva_pila(self, mouse_pos, imagen):

        #Se establecen algunos rangos tomando la posición en x (mouse_pos[0]) del mouse y la posicion en y
        #para establecer el rango entre los limites de la pila con un margen de error de aproximadamente 2%
        if mouse_pos[0] >= self.rect1.left-10 and mouse_pos[0] < self.rect1.left+70 and mouse_pos[1] >= self.rect1.top-10:
            #Se verifica si la pila está vacía o no
            if self.cont_pila1 == 0: 
                self.cont_pila1 += 1
                self.pila1.insert(0, imagen)
            #Se verifica que la carta corresponda a la carta siguiente a la que ya está en la pila
            elif self.verificar_continuidad_orden(self.pila1, self.cont_pila1, imagen):
                self.cont_pila1 += 1
                self.pila1.insert(self.cont_pila1 -1, imagen)
            else: 
                print(imagen, self.pila1[self.cont_pila1-1], self.cont_pila1-1)

        elif mouse_pos[0] >= self.rect2.left-10 and mouse_pos[0] < self.rect2.left+70 and mouse_pos[1] >= self.rect2.top-10:
            if self.cont_pila2 == 0: 
                self.cont_pila2 += 1
                self.pila2.insert(0, imagen)
            elif self.verificar_continuidad_orden(self.pila2, self.cont_pila2, imagen):
                self.cont_pila2 += 1
                self.pila2.insert(self.cont_pila2 -1, imagen)
            else: 
                print(imagen, self.pila2[self.cont_pila2-1], self.cont_pila2-1)

        elif mouse_pos[0] >= self.rect3.left-10 and mouse_pos[0] < self.rect3.left+70 and mouse_pos[1] >= self.rect3.top-10 :
            if self.cont_pila3 == 0: 
                self.cont_pila3 += 1
                self.pila3.insert(0, imagen)
            elif self.verificar_continuidad_orden(self.pila3, self.cont_pila3, imagen):
                self.cont_pila3 += 1
                self.pila3.insert(self.cont_pila3 -1, imagen)
            else: 
                print(imagen, self.pila3[self.cont_pila3-1], self.cont_pila3-1)
                print("Te encontre")

        elif mouse_pos[0] >= self.rect4.left-10 and mouse_pos[0] < self.rect4.left+70 and mouse_pos[1] >= self.rect4.top-10 :
            self.cont_pila4 += 1
            self.pila4.insert(self.cont_pila4 -1, imagen)
        elif mouse_pos[0] >= self.rect5.left-10 and mouse_pos[0] < self.rect5.left+70 and mouse_pos[1] >= self.rect5.top-10 :
            self.cont_pila5 += 1
            self.pila5.insert(self.cont_pila5 -1, imagen)
        elif mouse_pos[0] >= self.rect6.left-10 and mouse_pos[0] < self.rect6.left+70 and mouse_pos[1] >= self.rect6.top-10 :
            self.cont_pila6 += 1
            self.pila6.insert(self.cont_pila6 -1, imagen)
        elif mouse_pos[0] >= self.rect7.left-10 and mouse_pos[0] < self.rect7.left+70 and mouse_pos[1] >= self.rect7.top-10:
            self.cont_pila7 += 1
            self.pila7.insert(self.cont_pila7 -1, imagen)
        elif mouse_pos[0] >= self.r1.left-10 and mouse_pos[0] < self.r1.left+70 and mouse_pos[1] >= self.r1.top-10 and mouse_pos[1] < self.r1.top+170:
            self.cont_pila8 += 1
            self.pila8.insert(self.cont_pila8 -1, imagen)

    #Se verifica que la carta que se desea ingresar corresponda a la carta que le sigue a la que ya está en la pila
    def verificar_continuidad_orden(self, pila, posicion, imagen):

        listo = False

        if pila[posicion-1] == self.imgA or pila[posicion-1] == self.Aca: 
            if imagen == self.imgk or imagen == self.Ick: 
                listo = True
            else:
                listo = False
        elif pila[posicion-1] == self.imgk or pila[posicion-1] == self.Ick: 
            if imagen == self.imgq or imagen == self.IQca or imagen == self.IcQ: 
                listo = True
            else:
                listo = False
        elif  pila[posicion-1] == self.imgq or  pila[posicion-1] == self.IQca or  pila[posicion-1] == self.IcQ: 
            if imagen == self.imgj or imagen == self.Ijca:
                listo = True
            else:
                listo = False
        elif  pila[posicion-1] == self.imgj or pila[posicion-1] == self.Ijca: 
            if imagen == self.img10 or imagen == self.Ic10:
                listo = True
            else:
                listo = False
        elif  pila[posicion-1] == self.img10 or pila[posicion-1] == self.Ic10: 
            if imagen == self.img9:
                listo = True
            else:
                listo = False
        elif  pila[posicion-1] == self.img9: 
            if imagen == self.img8 or imagen == self.Ic8:
                listo = True
            else:
                listo = False
        elif  pila[posicion-1] == self.img8 or pila[posicion-1] == self.Ic8: 
            if imagen == self.img7 or imagen == self.Ic7:
                listo = True
            else:
                listo = False
        elif  pila[posicion-1] == self.img7 or pila[posicion-1] == self.Ic7: 
            if imagen == self.img6 or imagen == self.Ic6:
                listo = True
            else:
                listo = False
        elif  pila[posicion-1] == self.img6 or pila[posicion-1] == self.Ic6: 
            if imagen == self.img5 or imagen == self.I5ca:
                listo = True
            else:
                listo = False
        elif  pila[posicion-1] == self.img5 or pila[posicion-1] == self.I5ca: 
            if imagen == self.img4 or imagen == self.I4ca:
                listo = True
            else:
                listo = False
        elif  pila[posicion-1] == self.img4 or pila[posicion-1] == self.I4ca: 
            if imagen == self.img3:
                listo = True
            else:
                listo = False
        elif  pila[posicion-1] == self.img3: 
            if imagen == self.img2 or imagen == self.Ic2:
                listo = True

                #Se verifica el numero de cartas que ya han sigdo registradas en la pila
                #esto para saber si ya ha sido llenada
                if posicion+1 >= 13:
                    #En caso de obtener una respuesta afirmativa, se llama a la siguiente función para imprimir 
                    #el mensaje que señale que ya la pila se ha llenado
                    self.llenado_pila()

            else:
                listo = False

        return listo

    #Se muestra un mensaje que indica que ya al menos una pila ha sido completada
    def llenado_pila(self):
        text = '---------- End -------------'
        base_font = pygame.font.Font(None, 50)
        text_surface = base_font.render(text, True, (255,0,0))
        self.win.blit(text_surface, (350,self.alto-100))
        pygame.display.flip()

    #Se ingresa la imagen en la ultima posición de la pila
    def confirmar_ingreso_pila(self, imagen):
        if self.voltear.left == self.copy_rect2.left and self.pila2[self.cont_pila2-1] == self.imgAtras:
            self.pila2[self.cont_pila2-1] = imagen
        elif self.voltear.left == self.copy_rect3.left and self.pila3[self.cont_pila3-1] == self.imgAtras:
            self.pila3[self.cont_pila3-1] = imagen
        elif self.voltear.left == self.copy_rect4.left and self.pila4[self.cont_pila4-1] == self.imgAtras:
            self.pila4[self.cont_pila4-1] = imagen
        elif self.voltear.left == self.copy_rect5.left and self.pila5[self.cont_pila5-1] == self.imgAtras:
            self.pila5[self.cont_pila5-1] = imagen
        elif self.voltear.left == self.copy_rect6.left and self.pila6[self.cont_pila6-1] == self.imgAtras:
            self.pila6[self.cont_pila6-1] = imagen
        elif self.voltear.left == self.copy_rect7.left and self.pila7[self.cont_pila7-1] == self.imgAtras:
            self.pila7[self.cont_pila7-1] = imagen
        elif self.voltear.left == self.copy_rect1.left and self.pila1[self.cont_pila1-1] == self.imgAtras:
            self.pila1[self.cont_pila1-1] = imagen
        elif self.voltear.left == self.copy_rect8.left and self.cont_pila8 > 0:
            self.pila8[self.cont_pila8-1] = imagen

    #Con este metodo se 'crea' la pila
    def mov_mouse_1(self):
        self.array = [self.imgA, self.imgk, self.imgq, self.imgj, self.img10, self.img9, self.img8, self.img7, self.img6, self.img5, self.img4, self.img3, self.img2]
        self.array_tam_image = [self.imgA.get_rect(), self.imgk.get_rect(), self.imgq.get_rect(), self.imgj.get_rect(), 
                            self.img10. get_rect(), self.img9.get_rect(), self.img8.get_rect(), self.img7.get_rect(), 
                            self.img6.get_rect(), self.img5.get_rect(), self.img4.get_rect(), self.img3.get_rect(), self.img2.get_rect()]
        self.tam_image = self.imgAtras.get_rect()
        print('listo')

    #Se define la carta que sigue en la extracción de las mismas del monto
    def definir_carta(self, cont):
        carta = None

        if cont < 13 and cont >= 0:
            carta = self.array[cont]
        return carta 

    #Metodo creado para que las imagenes una vez que son sacadas del monto
    #se muevan junto al mouse, mientras se re-dibuja la pantalla 
    def mov_true(self, cont_cartas, mouse_pos):
        self.win.fill((25,111,61))
        carta = self.definir_carta(cont_cartas-1)
        
        #se le da la posición del mouse a la imagen 
        tam_image_1 = carta.get_rect()
        tam_image_1.left = mouse_pos[0]
        tam_image_1.top = mouse_pos[1]
        
        #se modifica la posición de esa carta en el vector 
        #que guarda las posiciones de cada carta
        self.array_tam_image[cont_cartas-1] = tam_image_1
        self.win.blit(carta, tam_image_1)

        return carta

    #Metodo creado para que la imagen que sea seleccionada de las 7 pilas de abajo
    #pueda moverse con el mouse, mientras se re-dibuja la pantalla 
    def mov_true_3(self, cont_cartas, mouse_pos):
        self.win.fill((25,111,61))

        tam_image_1 = self.imagen_mov.get_rect()
        tam_image_1.left = mouse_pos[0]
        tam_image_1.top = mouse_pos[1]
        
        self.win.blit(self.imagen_mov, tam_image_1)

    #Se le resta una unidad a la variable que cuenta la cantidad de cartas que hay en cada pila
    #esto cada vez que se retire una carta de la pila
    def quitar_carta_mov_pila(self): 
        if self.mov_pila1 == True: 
            self.cont_pila1 -= 1
        elif self.mov_pila2 == True: 
            self.cont_pila2 -= 1
        elif self.mov_pila3 == True: 
            self.cont_pila3 -= 1
        elif self.mov_pila4 == True: 
            self.cont_pila4 -= 1
        elif self.mov_pila5 == True: 
            self.cont_pila5 -= 1
        elif self.mov_pila6 == True: 
            self.cont_pila6 -= 1
        elif self.mov_pila7 == True: 
            self.cont_pila7 -= 1
        elif self.mov_pila8 == True: 
            self.cont_pila8 -= 1

        self.confirmar_identidad_mov_carta()
        self.crear_imagenes_pilas()

    #Se le da a la variable self.iamgen_mov la equivalencia de la carta que se esté moviendo en el momento
    #De las pilas de abajo
    def confirmar_identidad_mov_carta(self):
        if self.mov_pila1 == True: 
            self.imagen_mov = self.pila1[self.cont_pila1]
        elif self.mov_pila2 == True: 
            self.imagen_mov = self.pila2[self.cont_pila2]
        elif self.mov_pila3 == True: 
            self.imagen_mov = self.pila3[self.cont_pila3]
        elif self.mov_pila4 == True: 
            self.imagen_mov = self.pila4[self.cont_pila4]
        elif self.mov_pila5 == True: 
            self.imagen_mov = self.pila5[self.cont_pila5]
        elif self.mov_pila6 == True: 
            self.imagen_mov = self.pila6[self.cont_pila6]
        elif self.mov_pila7 == True: 
            self.imagen_mov = self.pila7[self.cont_pila7]
        elif self.mov_pila8 == True: 
            self.imagen_mov = self.pila8[self.cont_pila8]

    #Se dibuja el monto de cartas en una esquina de la pantalla, pero solo para la interfaz de pila
    #también se ilustran los rectangulos de la parte superior de la pantalla
    def apiladas(self, numero):
        left = 20
        top = 10
        tam_image_1 = None
        grey = (213,219,219)

        r2 = pygame.Rect(470 , 10, 95, 166)
        r3 = pygame.Rect(570, 10, 95, 166)
        r4 = pygame.Rect(680, 10, 95, 166)

        pygame.draw.rect(self.win, grey, self.r1, 4, 5)
        pygame.draw.rect(self.win, grey, r2, 4, 5)
        pygame.draw.rect(self.win, grey, r3, 4, 5)
        pygame.draw.rect(self.win, grey, r4, 4, 5)
        self.apiladas_abajo_juego()
        self.crear_copias()

        for i in range(0, numero+1):
            tam_image_1 = self.imgAtras.get_rect()
            tam_image_1.left = left         
            tam_image_1.top = top

            self.win.blit(self.imgAtras, tam_image_1)

        return tam_image_1

    #Con este metodo se llaman todos los metodos que organizan a las diferentes pilas
    def apiladas_abajo_juego(self):
        #Se crea la variable que contendrá la posición de la última carta disponible en cada pila
        self.cartas_abajo_apiladas = []

        self.organizar_pila_1()
        self.organizar_pila_2()
        self.organizar_pila_3()
        self.organizar_pila_4()
        self.organizar_pila_5()
        self.organizar_pila_6()
        self.organizar_pila_7()
        self.organizar_pila_8()

    #Dibuja las cartas que estan en la pil 1 a en el rango que se estable con la variable self.cont_pila1
    #variable que aumenta o disminuye cada que se saque o inserte una carta a la pila
    def organizar_pila_1(self):
        top = self.copy_rect1.top

        #Se verifica que la variable sea positiva y que en la pila todavia hayan cartas
        if self.cont_pila1 > 0:
            #Se recorre la lista que tiene las cartas de la pila, desde 0 hasta el número que la variable nos diga
            for i in range(0, self.cont_pila1): 
                tam_image_1 = self.copy_rect1
                tam_image_1.top = top
                top += 30
                
                #Se pregunta si estamos en la ultima posicion de la lista para agregar la ubicacion 
                #en una lista que después nos permitirá conocer la ubicación de la carta a la que se 
                #le puede dar movimiento con el mouse
                if i == self.cont_pila1-1:
                    self.cartas_abajo_apiladas.append(self.copy_rect1)

                #Se pregunta si la lista ya ha sido llenada
                if len(self.pila1) > i:
                    #en caso de que así sea, se pregunta cual es la carta que está 
                    #y se procede a dibujarla
                    if self.pila1[i] != self.imgAtras:
                        self.win.blit(self.pila1[i], tam_image_1)
                    #en el caso contrario se muestra una imagen que muestra la parte trasera de las cartas
                    else:
                        self.win.blit(self.imgAtras, tam_image_1)
                #en caso de que le lista no haya sido llenada, se le agrega la imagen que muestra la parte trasera de las cartas
                else:
                    self.pila1.append(self.imgAtras)
                    self.win.blit(self.imgAtras, tam_image_1)

            #Se hace una pequeña verificación para eliminar de la pila las cartas que ya han sido sacadas 
            #esto preguntando si el tamaño de la pila es igual al de la variable global que nos lleva una cuenta 
            #de las cartas con las que disponemos en la pila
            i = self.cont_pila1
            while len(self.pila1) > i: 
                self.pila1.pop(i)
                i += 1

    #Dibuja las cartas que estan en la pila 2 en el rango que se estable con la variable self.cont_pila2
    #variable que aumenta o disminuye cada que se saque o inserte una carta a la pila
    def organizar_pila_2(self):
        top = self.copy_rect2.top

        if self.cont_pila2 > 0:
            for i in range(0, self.cont_pila2): 
                tam_image_1 = self.copy_rect2
                tam_image_1.top = top
                top += 30
                
                if i == self.cont_pila2-1:
                    self.cartas_abajo_apiladas.append(self.copy_rect2)

                if len(self.pila2) > i:
                    if self.pila2[i] != self.imgAtras:
                        self.win.blit(self.pila2[i], tam_image_1)
                    else:
                        self.win.blit(self.imgAtras, tam_image_1)
                else:
                    self.pila2.append(self.imgAtras)
                    self.win.blit(self.imgAtras, tam_image_1)

    #Dibuja las cartas que estan en la pila 3 en el rango que se estable con la variable self.cont_pila3
    def organizar_pila_3(self):
        top = self.copy_rect3.top

        if self.cont_pila3 > 0:
            for i in range(0, self.cont_pila3): 
                tam_image_1 = self.copy_rect3
                tam_image_1.top = top
                top += 30
                
                if i == self.cont_pila3-1:
                    self.cartas_abajo_apiladas.append(self.copy_rect3)

                if len(self.pila3) > i:
                    if self.pila3[i] != self.imgAtras:
                        self.win.blit(self.pila3[i], tam_image_1)
                    else:
                        self.win.blit(self.imgAtras, tam_image_1)
                else:
                    self.pila3.append(self.imgAtras)
                    self.win.blit(self.imgAtras, tam_image_1)

    #Dibuja las cartas que estan en la pila 4 en el rango que se establece con la variable self.cont_pila4
    def organizar_pila_4(self):
        top = self.copy_rect4.top

        if self.cont_pila4 > 0:
            for i in range(0, self.cont_pila4): 
                tam_image_1 = self.copy_rect4
                tam_image_1.top = top
                top += 30
                
                if i == self.cont_pila4-1:
                    self.cartas_abajo_apiladas.append(self.copy_rect4)

                if len(self.pila4) > i:
                    if self.pila4[i] != self.imgAtras:
                        self.win.blit(self.pila4[i], tam_image_1)
                    else:
                        self.win.blit(self.imgAtras, tam_image_1)
                else:
                    self.pila4.append(self.imgAtras)
                    self.win.blit(self.imgAtras, tam_image_1)

    #Dibuja las cartas que estan en la pila 5 en el rango que se establece con la variable self.cont_pila5
    def organizar_pila_5(self):
        top = self.copy_rect5.top

        if self.cont_pila5 > 0:
            for i in range(0, self.cont_pila5): 
                tam_image_1 = self.copy_rect5
                tam_image_1.top = top
                top += 30
                
                if i == self.cont_pila5-1:
                    self.cartas_abajo_apiladas.append(self.copy_rect5)

                if len(self.pila5) > i:
                    if self.pila5[i] != self.imgAtras:
                        self.win.blit(self.pila5[i], tam_image_1)
                    else:
                        self.win.blit(self.imgAtras, tam_image_1)
                else:
                    self.pila5.append(self.imgAtras)
                    self.win.blit(self.imgAtras, tam_image_1)

    #Dibuja las cartas que estan en la pila 6 en el rango que se establece con la variable self.cont_pila6
    def organizar_pila_6(self):
        top = self.copy_rect6.top

        if self.cont_pila6 > 0:
            for i in range(0, self.cont_pila6): 
                tam_image_1 = self.copy_rect6
                tam_image_1.top = top
                top += 30
                
                if i == self.cont_pila6-1:
                    self.cartas_abajo_apiladas.append(self.copy_rect6)

                if len(self.pila6) > i:
                    if self.pila6[i] != self.imgAtras:
                        self.win.blit(self.pila6[i], tam_image_1)
                    else:
                        self.win.blit(self.imgAtras, tam_image_1)
                else:
                    self.pila6.append(self.imgAtras)
                    self.win.blit(self.imgAtras, tam_image_1)

    #Dibuja las cartas que estan en la pila 7 en el rango que se establece con la variable self.cont_pila7
    def organizar_pila_7(self):
        top = self.copy_rect7.top

        if self.cont_pila7 > 0:
            for i in range(0, self.cont_pila7): 
                tam_image_1 = self.copy_rect7
                tam_image_1.top = top
                top += 30
                
                if i == self.cont_pila7-1:
                    self.cartas_abajo_apiladas.append(self.copy_rect7)

                if len(self.pila7) > i:
                    if self.pila7[i] != self.imgAtras:
                        self.win.blit(self.pila7[i], tam_image_1)
                    else:
                        self.win.blit(self.imgAtras, tam_image_1)
                else:
                    self.pila7.append(self.imgAtras)
                    self.win.blit(self.imgAtras, tam_image_1)

    #Dibuja las cartas que estan en la pila 8 en el rango que se establece con la variable self.cont_pila8
    def organizar_pila_8(self):
        top = self.copy_rect8.top

        if self.cont_pila8 > 0:
            for i in range(0, self.cont_pila8): 
                tam_image_1 = self.copy_rect8
                tam_image_1.top = top
                
                if i == self.cont_pila8-1:
                    self.cartas_abajo_apiladas.append(self.copy_rect8)

                self.win.blit(self.pila8[i], tam_image_1)

    #Se crean las copias iniciales de las rectas principales de cada pila
    #para partir de ahí con el dibjo de cada imagen perteneciente a la pila
    def crear_copias(self):
        self.copy_rect1 = pygame.Rect(20, 200, 95, 166)
        self.copy_rect2 = pygame.Rect(130, 200, 95, 166)
        self.copy_rect3 = pygame.Rect(240, 200, 95, 166)
        self.copy_rect4 = pygame.Rect(350, 200, 95, 166)
        self.copy_rect5 = pygame.Rect(460, 200, 95, 166)
        self.copy_rect6 = pygame.Rect(570, 200, 95, 166)
        self.copy_rect7 = pygame.Rect(680, 200, 95, 166)
        self.copy_rect8 = pygame.Rect(350, 10, 95, 166)

        self.vector_copy = [self.copy_rect1, self.copy_rect2, self.copy_rect3, self.copy_rect4, self.copy_rect5, self.copy_rect6, self.copy_rect7, self.copy_rect8]

    #Se crean las imagenes aleatorias mostradas al final de la pila 
    def crear_imagenes_pilas(self):
        #Se crean las copias de las rectas principales de cada pila
        self.crear_copias()
        x = len(self.vector_copy)-1

        for i in range(0, x): 
            actual = self.vector_copy[i]
            #Se elige un numero que esté en el rango del tamaño de la lista
            #que contiene a las imagenes
            numero = random.randrange(0, len(self.imagenes)-1)
            imag = self.imagenes[numero]
            self.vector_copy_imagenes.append(imag)
            self.voltear = actual
            self.confirmar_ingreso_pila(imag)

    #retorna la pisición (en la pila) en donde está la carta que ha sido seleccionada
    def carta_actual_collision(self, mov):
        listo = False
        i = 0

        #Se verifica que la carta que se desee mover no esté en el monto
        if mov is False:
            #se recorre la pila hasta que se encuentre o 'i' pase su tamaño
            while not listo and  i < len(self.array):
                tam_imagen = self.array_tam_image[i]
                if tam_imagen.collidepoint(pygame.mouse.get_pos()):
                    self.tam_image = self.array_tam_image[i]
                    listo = True
                i += 1

        return i-1

    #Se verifica la colision del mouse con una de las cartas de las 7 pilas de la parte baja
    def carta_actual_collision_2(self):
        listo = False
        i = 0

        #se recorre la lista que tiene un registro de las ultima carta que se encuentra en cada pila
        while not listo and  i < len(self.cartas_abajo_apiladas):
            tam_imagen = self.cartas_abajo_apiladas[i]

            #se verifica que la carta que la carta actual haya sido clickponeada 
            #y de ser el caso se identifica la pila en la que se encuentra la carta
            #para llamar a una función que diga que todas las demas pilas no son
            if tam_imagen.collidepoint(pygame.mouse.get_pos()):

                if tam_imagen.left == self.rect1.left:
                    self.mov_pila1 = True
                    self.imagen_mov_pila1()
                elif tam_imagen.left == self.rect2.left:
                    self.mov_pila2 = True
                    self.imagen_mov_pila2()
                elif tam_imagen.left == self.rect3.left:
                    self.mov_pila3 = True
                    self.imagen_mov_pila3()
                elif tam_imagen.left == self.rect4.left and tam_imagen.top >= self.rect4.top-15:
                    self.mov_pila4 = True
                    self.imagen_mov_pila4()
                elif tam_imagen.left == self.rect5.left and tam_imagen.top >= self.rect5.top-15:
                    self.mov_pila5 = True
                    self.imagen_mov_pila5()
                elif tam_imagen.left == self.rect6.left:
                    self.mov_pila6 = True
                    self.imagen_mov_pila6()
                elif tam_imagen.left == self.rect7.left:
                    self.mov_pila7 = True
                    self.imagen_mov_pila7()
                elif tam_imagen.left > self.r1.left-20 and tam_imagen.left < self.r1.left+110:
                    self.mov_pila8 = True
                    self.imagen_mov_pila8()

                #Se estable la ubicación de la carta tocada, ingresando esta en la variable global
                self.tam_image_2 = self.cartas_abajo_apiladas[i]
                #Se le notifica al ciclo que ya ha sido encontrada la carta para que se suspenda y deje de buscar
                listo = True
            i += 1

        return listo

    def imagen_mov_pila1(self):
        self.mov_pila2 = False
        self.mov_pila3 = False
        self.mov_pila4 = False
        self.mov_pila5 = False
        self.mov_pila6 = False
        self.mov_pila7 = False
        self.mov_pila8 = False
    
    def imagen_mov_pila2(self):
        self.mov_pila1 = False
        self.mov_pila3 = False
        self.mov_pila4 = False
        self.mov_pila5 = False
        self.mov_pila6 = False
        self.mov_pila7 = False
        self.mov_pila8 = False

    def imagen_mov_pila3(self):
        self.mov_pila1 = False
        self.mov_pila2 = False
        self.mov_pila4 = False
        self.mov_pila5 = False
        self.mov_pila6 = False
        self.mov_pila7 = False
        self.mov_pila8 = False

    def imagen_mov_pila4(self):
        self.mov_pila1 = False
        self.mov_pila2 = False
        self.mov_pila3 = False
        self.mov_pila5 = False
        self.mov_pila6 = False
        self.mov_pila7 = False
        self.mov_pila8 = False

    def imagen_mov_pila5(self):
        self.mov_pila1 = False
        self.mov_pila2 = False
        self.mov_pila4 = False
        self.mov_pila3 = False
        self.mov_pila6 = False
        self.mov_pila7 = False
        self.mov_pila8 = False

    def imagen_mov_pila6(self):
        self.mov_pila1 = False
        self.mov_pila2 = False
        self.mov_pila4 = False
        self.mov_pila3 = False
        self.mov_pila5 = False
        self.mov_pila7 = False
        self.mov_pila8 = False

    def imagen_mov_pila7(self):
        self.mov_pila1 = False
        self.mov_pila2 = False
        self.mov_pila4 = False
        self.mov_pila3 = False
        self.mov_pila5 = False
        self.mov_pila6 = False
        self.mov_pila8 = False

    def imagen_mov_pila8(self):
        self.mov_pila1 = False
        self.mov_pila2 = False
        self.mov_pila4 = False
        self.mov_pila3 = False
        self.mov_pila5 = False
        self.mov_pila6 = False
        self.mov_pila7 = False