import pygame
import sys
import random
import unicodedata

class grafo():
    def __init__(self, win, ancho, alto):
        pygame.init()

        self.ancho = ancho
        self.alto = alto
        self.terminar_grafo= False

        self.tam_mapa_ancho = 474
        self.tam_mapa_alto = 655

        self.user_text = ''
        self.value_input = ''

        self.base = 'Cantidad de nodos del arbol: '
        self.value = 'Valor del nodo: '
        self.input_rect = pygame.Rect(346, 5, 160, 30)

        self.img_mapa = pygame.image.load("Imagenes\MapaColombia.jpg")
        self.tam_mapa_rect =  None
        self.base_font = pygame.font.Font(None, 32)
        self.base_font_2 = pygame.font.Font(None, 23)
        self.base_font_3 = pygame.font.Font(None, 26)

        self.win = win
        self.win.fill((0,0,0))

        self.root = None
        self.length = None

        self.text_dijktra = 'Dijktra'
        self.rect_dijk = pygame.Rect(30, 60, 125, 25) 
        self.algorithm_dijktra = False
        self.recorrido_corto = None

        self.text_rutas = 'rutas'
        self.rect_rutas = pygame.Rect(190, 60, 125, 25) 
        self.mostrar_rutas = False

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

        self.combo_3 = 'Arista:'
        self.input_rect_origen = pygame.Rect(115, self.alto-40, 115, 25) 
        self.user_text_origen = ""
        self.input_rect_destino = pygame.Rect(372, self.alto-40, 115, 25) 
        self.user_text_destino = ""
        self.input_rect_arista = pygame.Rect(607, self.alto-40, 70, 25) 
        self.user_text_arista = ""

        self.combo_4 = "Selected"
        self.rect_select_arista = pygame.Rect(760, self.alto-40, 115, 25) 

        self.color_menu = (255, 255, 255)
        self.color_option = (0, 0, 0)

        self.ciudades = ['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena',
                            'Cúcuta', 'Leticia', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Riohacha',
                            'Santa Marta', 'Valledupar', 'Villavicencio']
        self.relaciones = []
        self.dictionary_relations = None
        self.rectas_ciudades = []
        self.grafos = []
        self.otros = []

        self.negro = (0,0,0)
        self.blanco = (255,255,255)
        self.rojo = (100,30,22)

    #Se crean los rectangulos donde se ingresarán las equivalencias de la ciudad de origen y la de destino
    #al igual que el nuevo valor correspondiente a la arista que conecta a las dos ciudades
    def crear_cajas_texto(self):
        text_surface = self.base_font.render(self.combo_1, True, (255, 255, 255))
        self.win.blit(text_surface, (30, 817))
        pygame.draw.rect(self.win, (255,255,255), self.input_rect_origen, 2)

        text_surface = self.base_font.render(self.combo_2, True, (255, 255, 255))
        self.win.blit(text_surface, (281, 817))
        pygame.draw.rect(self.win, (255,255,255), self.input_rect_destino, 2)

        text_surface = self.base_font.render(self.combo_3, True, (255, 255, 255))
        self.win.blit(text_surface, (525, 817))
        pygame.draw.rect(self.win, (255,255,255), self.input_rect_arista, 2)

    #Metodo que crea los botones necesarios: el de seleccionar para cambio del valor de la arista entre dos vertices
    #el que permite ilustrar la ruta más corta con dijktra y el que muestra todas las rutas
    def crear_botones_grafo(self):
        pygame.draw.rect(self.win, (255,255,255), self.rect_dijk)
        pygame.draw.rect(self.win, (255,255,255), self.rect_rutas)
        pygame.draw.rect(self.win, (255,255,255), self.rect_select_arista)

        text_surface = self.base_font.render(self.text_dijktra, True, (0,0,0))
        self.win.blit(text_surface, (self.rect_dijk.x + (self.rect_dijk.width - text_surface.get_width()) / 2, (self.rect_dijk.y + (self.rect_dijk.height - text_surface.get_height())/2)))

        text_surface = self.base_font.render(self.text_rutas, True, (0,0,0))
        self.win.blit(text_surface, (self.rect_rutas.x + (self.rect_rutas.width - text_surface.get_width()) / 2, (self.rect_rutas.y + (self.rect_rutas.height - text_surface.get_height())/2)))

        self.crear_cajas_texto()
        text_surface = self.base_font.render(self.combo_4, True, (0,0,0))
        self.win.blit(text_surface, (self.rect_select_arista.x + (self.rect_select_arista.width - text_surface.get_width()) / 2, (self.rect_select_arista.y + (self.rect_select_arista.height - text_surface.get_height())/2)))

    #Se recorren las posibles rutas de destino de una ciudad a otra
    #sin importar las escalas que se deban hacer
    def recorre(self):
        origen = self.ciudades.index(self.eleccion_1)
        destino = self.ciudades.index(self.eleccion_2)

        ciudades_origen = self.relaciones[origen].copy()
        prev = []

        def busqueda(vector, prev):
            grafos = []
            estaba = False

            for i in range(len(vector)):
                actual = vector[i]
                if actual != self.eleccion_1:
                    if actual == self.eleccion_2:
                        grafos.append(actual)
                    else:
                        for i in range(len(prev)):
                            if actual == prev[i]:
                                estaba = True
                        
                        if estaba == False and len(prev) != 18:
                            index = self.ciudades.index(actual)
                            prev.insert(0, actual)
                            grafos.append(actual)
                            grafos.append(busqueda(self.relaciones[index], prev))
            return grafos
        
        while ciudades_origen:
            self.grafos.append(busqueda(ciudades_origen, prev))
            ciudades_origen.pop(0)
            prev = []

        self.dibujar_recorridos()

    #Se dibujan todas las rutas posibles, ya obtenidas con el metodo anterior
    def dibujar_recorridos(self): 
        index = self.ciudades.index(self.eleccion_1)
        rect_inicial = self.rectas_ciudades[index]
        cont = 0

        for i in range(len(self.grafos)):
            #print(type(self.grafos[0]))
            vector = self.grafos[i]

            for j in range(len(vector)):
                if cont == 0 and type(vector[j]) is str:
                    index_2 = self.ciudades.index(vector[j])
                    rect = self.rectas_ciudades[index_2]

                    pygame.draw.line(self.win, (255, 25, 255), (rect_inicial.left,rect_inicial.top), (rect.left,rect.top), 4)
                    
                    if type(vector[j+1]) != str and vector[j+1] != self.recorrido_corto:
                        actual_2 = vector[j+1]
                        for i in range(len(actual_2)):
                            if type(actual_2[i]) is str:
                                index_3 = self.ciudades.index(actual_2[i])
                                rect_2 = self.rectas_ciudades[index_3]

                                pygame.draw.line(self.win, (20,143, 119), (rect.left,rect.top), (rect_2.left,rect_2.top), 4)
                            else: 
                                index_4 = self.ciudades.index(self.eleccion_2)
                                rect_3 = self.rectas_ciudades[index_4]

                                pygame.draw.line(self.win, (20,143, 119), (rect_2.left,rect_2.top), (rect_3.left,rect_3.top), 4)

                    cont+=1
                elif type(vector[j]) is str:
                    index_2 = self.ciudades.index(vector[j])
                    rect = self.rectas_ciudades[index_2]

                    pygame.draw.line(self.win, (255, 25, 255), (rect_inicial.left,rect_inicial.top), (rect.left,rect.top), 4)
                    
                    if j != len(vector)-1:
                        if type(vector[j+1]) != str and vector[j+1] != self.recorrido_corto:
                            actual_2 = vector[j+1]
                            for i in range(len(actual_2)):
                                if type(actual_2[i]) is str:
                                    index_3 = self.ciudades.index(actual_2[i])
                                    rect_2 = self.rectas_ciudades[index_3]

                                    pygame.draw.line(self.win, (46,134, 193), (rect.left,rect.top), (rect_2.left,rect_2.top), 4)
                                else: 
                                    index_4 = self.ciudades.index(self.eleccion_2)
                                    rect_3 = self.rectas_ciudades[index_4]

                                    pygame.draw.line(self.win, (46,134, 193), (rect_2.left,rect_2.top), (rect_3.left,rect_3.top), 4)
                pygame.display.flip()

    #Metodo que dibuja la imagen del mapa
    def mapa_fondo(self):
        if self.tam_mapa_rect == None:
            tam_image = self.img_mapa.get_rect()
            tam_image.left += 360
            tam_image.top += 35
            self.tam_mapa_rect = tam_image

        self.win.blit(self.img_mapa, self.tam_mapa_rect)

    #Se dibuja el rectangulo del combobox de las ciudades origen, y una imagen
    #que se utilizaría para desplegar las opciones del combobox
    def combo_origen(self):
        pygame.draw.rect(self.win, self.color_menu, self.rect_combo_1, 0)
        self.img_1 = pygame.image.load("Imagenes\descarga.png")
        self.rect_mov1 = pygame.Rect(30, 100, 100, 25) 
        self.rect_mov1.left += 100
        self.win.blit(self.img_1, self.rect_mov1)

    #Se dibuja el rectangulo del combobox de las ciudades destino, y una imagen
    #que se utilizaría para desplegar las opciones del combobox
    def combo_destino(self):
        pygame.draw.rect(self.win, self.color_menu, self.rect_combo_2, 0)
        self.img_2 = pygame.image.load("Imagenes\descarga.png")
        self.rect_mov2 = pygame.Rect(190, 100, 100, 25) 
        self.rect_mov2.left += 100
        self.win.blit(self.img_2, self.rect_mov2)

    #Metodo que permite dar inicio a la dinamica
    def inicio_juego(self):
        cont_1 = 0
        cont_2 = 0
        cont_3 = 0
        cont_4 = 0

        self.mapa_fondo()
        self.dibujar_nodos_mapa()
        self.combo_origen()
        self.combo_destino()
        self.relaciones_ciudades()
        self.crear_botones_grafo()

        while not self.terminar_grafo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  self.terminar_grafo = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos() 
                    if mouse_pos[0] >= self.rect_mov2.left and mouse_pos[0] <= self.rect_mov2.left+25 and mouse_pos[1] >= self.rect_mov2.top and mouse_pos[1] <= self.rect_mov2.top+20:
                        if cont_1 == 0 or cont_1%2 == 0:
                            self.draw_menu_2 = True
                        else:
                            self.win.fill((0,0,0))
                            self.borrar_info_grafo()
                            self.draw_menu_2 = False
                        cont_1+= 1
                    elif mouse_pos[0] >= self.rect_mov1.left and mouse_pos[0] <= self.rect_mov1.left+25 and mouse_pos[1] >= self.rect_mov1.top and mouse_pos[1] <= self.rect_mov1.top+20:
                        if cont_2 == 0 or cont_2%2 == 0:
                            self.draw_menu_1 = True
                        else:
                            self.win.fill((0,0,0))
                            self.borrar_info_grafo()
                            self.draw_menu_1 = False
                        cont_2+= 1
                    elif mouse_pos[0] >= self.rect_dijk.left and mouse_pos[0] <= self.rect_dijk.left+100 and mouse_pos[1] >= self.rect_dijk.top and mouse_pos[1] <= self.rect_dijk.top+20:
                        if cont_3 == 0 or cont_3%2 == 0:
                            self.algorithm_dijktra = True
                        else:
                            self.win.fill((0,0,0))
                            self.algorithm_dijktra = False
                            self.borrar_info_grafo()
                            cont_3 += 1
                        print('dij', self.algorithm_dijktra, cont_3)
                    elif mouse_pos[0] >= self.rect_rutas.left and mouse_pos[0] <= self.rect_rutas.left+100 and mouse_pos[1] >= self.rect_rutas.top and mouse_pos[1] <= self.rect_rutas.top+20:
                        if cont_4 == 0 or cont_4%2 == 0:
                            self.mostrar_rutas = True
                        else:
                            self.win.fill((0,0,0))
                            self.mostrar_rutas = False
                            self.borrar_info_grafo()
                        print('ru', self.mostrar_rutas)
                        cont_4 += 1
                    elif mouse_pos[0] >= self.input_rect_origen.left and mouse_pos[0] <= self.input_rect_origen.left+100 and mouse_pos[1] >= self.input_rect_origen.top and mouse_pos[1] <= self.input_rect_origen.top+20:
                        self.ingreso_ciudad_origen()
                    elif mouse_pos[0] >= self.input_rect_destino.left and mouse_pos[0] <= self.input_rect_destino.left+100 and mouse_pos[1] >= self.input_rect_destino.top and mouse_pos[1] <= self.input_rect_destino.top+20:
                        self.ingreso_ciudad_destino()
                    elif mouse_pos[0] >= self.input_rect_arista.left and mouse_pos[0] <= self.input_rect_arista.left+100 and mouse_pos[1] >= self.input_rect_arista.top and mouse_pos[1] <= self.input_rect_arista.top+20:
                        self.ingreso_distancia_arista()
                    elif mouse_pos[0] >= self.rect_select_arista.left and mouse_pos[0] <= self.rect_select_arista.left+100 and mouse_pos[1] >= self.rect_select_arista.top and mouse_pos[1] <= self.rect_select_arista.top+20:
                        self.cambio_aristas()

                    self.eleccion_combobox(mouse_pos)

                if self.algorithm_dijktra == True and self.eleccion_1 != None and self.eleccion_2 != None:
                    if cont_3 == 0 or cont_3%2 == 0:
                        recorrido = self.dijkstra(self.dictionary_relations, self.eleccion_1)
                        self.definir_recorrido_corto(recorrido)
                        cont_3 += 1
                
                if self.eleccion_1 != None and self.eleccion_2 != None and self.mostrar_rutas == True:
                    self.grafos = []
                    self.recorre()

                self.mostrar_combobox()
                self.mostrar_rutas_pant()

            pygame.display.flip()

    #Se verifica que el botón "selected" haya sido clickponeado, eso para permitir
    #el cambio del valor de la arista entre las ciudades que han sido elegidas
    def cambio_aristas(self):
        if self.user_text_origen != "" and self.user_text_destino != "" and self.user_text_arista != "": 
            origen_in = unicodedata.normalize('NFKD', self.user_text_origen).encode('ASCII', 'ignore').strip().lower()
            destino_in = unicodedata.normalize('NFKD', self.user_text_destino).encode('ASCII', 'ignore').strip().lower()

            if origen_in == b'santamarta':
                origen_in = b'santa marta'
            elif origen_in == b'sanandres':
                origen_in = b'san andres'

            if destino_in == b'santamarta':
                destino_in = b'santa marta'
            elif destino_in == b'sanandres':
                destino_in = b'san andres'
            
            for clave in self.dictionary_relations: 
                if unicodedata.normalize('NFKD', clave).encode('ASCII', 'ignore').strip().lower() == origen_in:
                    print(unicodedata.normalize('NFKD', self.user_text_origen).encode('ASCII', 'ignore').strip().lower())
                    for clave_2 in self.dictionary_relations[clave]:
                        if unicodedata.normalize('NFKD', clave_2).encode('ASCII', 'ignore').strip().lower() == destino_in:
                            print(self.dictionary_relations[clave][clave_2])
                            self.dictionary_relations[clave][clave_2] = int(self.user_text_arista)
                            print(unicodedata.normalize('NFKD', self.user_text_destino).encode('ASCII', 'ignore').strip().lower(), self.dictionary_relations[clave_2])

    #Método que permite el ingreso de la equivalencia (utilizando el teclado)
    #de la ciudad origen a la que se le cambiará el valor de la arista
    def ingreso_ciudad_origen(self):
        terminar = False

        while terminar == False: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  terminar = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: 
                        self.user_text_origen = self.user_text_origen[:-1]
                        self.win.fill((0,0,0))
                        self.borrar_info_grafo()
                    elif event.key == pygame.K_SPACE:
                        terminar = True
                    else:
                        self.user_text_origen += event.unicode

            text_surface = self.base_font_3.render(self.user_text_origen, True, (0,255,255))
            self.win.blit(text_surface, (120, self.alto-35))
            pygame.display.flip()

    #Método que permite el ingreso de la equivalencia (utilizando el teclado)
    #de la ciudad destino a la que se le cambiará el valor de la arista
    def ingreso_ciudad_destino(self):
        terminar = False

        while terminar == False: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  terminar = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: 
                        self.user_text_destino = self.user_text_destino[:-1]
                        self.win.fill((0,0,0))
                        self.borrar_info_grafo()
                    elif event.key == pygame.K_SPACE:
                        terminar = True
                    else:
                        self.user_text_destino += event.unicode

            text_surface = self.base_font_3.render(self.user_text_destino, True, (0,255,255))
            self.win.blit(text_surface, (377,self.alto-35))
            pygame.display.flip()

    #Método que permite el ingreso de la equivalencia
    #(utilizando el teclado) de la arista que se cambia
    def ingreso_distancia_arista(self):
        terminar = False

        while terminar == False: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  terminar = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: 
                        self.user_text_arista = self.user_text_arista[:-1]
                        self.win.fill((0,0,0))
                        self.borrar_info_grafo()
                    elif event.key == pygame.K_SPACE:
                        terminar = True
                    else:
                        r = self.validar_int(event.unicode)
                        print(r)

                        if r != False: 
                            self.user_text_arista += event.unicode

            text_surface = self.base_font_3.render(self.user_text_arista, True, (0,255,255))
            self.win.blit(text_surface, (612, self.alto-35))
            pygame.display.flip()

    #Se valida que el valor de la arista sea numerico
    def validar_int(self, numero):
        try:
            conversion = int(numero)
            return conversion
        except:
            return False

    #Se define la ruta más corta previamente encontrada (con dijktra)
    def definir_recorrido_corto(self, recorrido):
        for actual in recorrido: 
            f = len(actual)-1

            if actual[f] == self.eleccion_2:
                self.recorrido_corto = actual
                cont = self.recorrido_corto.count(self.eleccion_1)

                while cont > 1: 
                    self.recorrido_corto.pop(0)
                    cont -= 1
        
        self.visualizar_recorrido_corto()

    #Método para dibujar las aristas del recorrido más corto hayado
    def visualizar_recorrido_corto (self):
        i = 0
        rect_recorrido_corto = pygame.Rect(150, 10, 100, 25) 

        if self.recorrido_corto != None:
            while i < len(self.recorrido_corto)-1:
                actual = self.recorrido_corto[i]
                index = self.ciudades.index(actual)
                rect = self.rectas_ciudades[index]

                i+=1
                actual_1 = self.recorrido_corto[i]
                index_1 = self.ciudades.index(actual_1)
                rect_1 = self.rectas_ciudades[index_1]

                pygame.draw.line(self.win, (0, 0, 0), (rect.left,rect.top), (rect_1.left,rect_1.top), 8)

            text_surface = self.base_font_2.render(str(self.recorrido_corto), True, (255,255,255))
        else:
            text_surface = self.base_font_2.render(self.eleccion_1, True, (255,255,255))

        self.win.blit(text_surface, (rect_recorrido_corto.x + (rect_recorrido_corto.width - text_surface.get_width()) / 2, (rect_recorrido_corto.y + (rect_recorrido_corto.height - text_surface.get_height())/2)))

    #Se muestran todas las opciones de los combobox (origen y destino) 
    #en caso de seleccionar la apción de despliegue
    def mostrar_combobox(self):
        if self.draw_menu_1:
            for i, text in enumerate(self.ciudades):
                rect = self.rect_combo_1.copy()

                rect.y += (i+1) * self.rect_combo_1.height
                self.rectas_options_1.insert(i, rect)
                if len(self.rectas_options_1) > i+1:
                    self.rectas_options_1.pop(i+1)

                pygame.draw.rect(self.win, self.color_menu, rect, 0)
                msg = self.base_font_2.render(text, 1, self.color_option)
                self.win.blit(msg, rect)
        elif self.draw_menu_2:
            for i, text in enumerate(self.ciudades):
                rect = self.rect_combo_2.copy()

                rect.y += (i+1) * self.rect_combo_2.height
                self.rectas_options_2.insert(i, rect)
                if len(self.rectas_options_2) > i+1:
                    self.rectas_options_2.pop(i+1)

                pygame.draw.rect(self.win, self.color_menu, rect, 0)
                msg = self.base_font_2.render(text, 1, self.color_option)
                self.win.blit(msg, rect)

    #metodo que dibuja los vertices que conforman cada una de 
    #las rutas posibles entre dos ciudades
    def mostrar_rutas_pant(self):
        if self.eleccion_1 != None and self.eleccion_2 != None and self.mostrar_rutas == True:
            self.dibujar_recorridos()

    #Se determina la ciudad elegida entre las opciones de los combobox
    def eleccion_combobox(self, mouse_pos):
        if self.draw_menu_1 == True:
            i = 0
            while i <= len(self.rectas_options_1)-1:
                actual = self.rectas_options_1[i]
                if mouse_pos[1] <= actual.top+20 and mouse_pos[1] >= actual.top and mouse_pos[0] <= actual.left+90 and mouse_pos[0] >= actual.left:
                    self.win.fill((0,0,0))
                    self.eleccion_1 = self.ciudades[i]
                    print(self.eleccion_1)
                    self.borrar_info_grafo()
                    self.draw_menu_1 = False
                i+=1
        if self.draw_menu_2 == True:
            i = 0
            while i <= len(self.rectas_options_2)-1:
                actual = self.rectas_options_2[i]
                if mouse_pos[1] <= actual.top+20 and mouse_pos[1] >= actual.top and mouse_pos[0] <= actual.left+90 and mouse_pos[0] >= actual.left:
                    self.win.fill((0,0,0))
                    self.eleccion_2 = self.ciudades[i]
                    print(self.eleccion_2)
                    self.borrar_info_grafo()
                    self.draw_menu_2 = False
                i+=1

        if self.algorithm_dijktra == True:
            self.algorithm_dijktra = False
            self.win.fill((0,0,0))
            self.borrar_info_grafo()
            self.algorithm_dijktra = True
            recorrido = self.dijkstra(self.dictionary_relations, self.eleccion_1)
            self.definir_recorrido_corto(recorrido)

    #Método dijkstra que halla el recorrido más corto desde
    #la ciudad origen hasta cada una de las ciudades posibles
    def dijkstra(self, Grafo, salida):
        dist, prev = {}, {}
        result = []
        recorrido = []

        for vertice in Grafo:
            dist[vertice] = float("inf")
            prev[vertice] = None
        dist[salida] = 0

        vertice_visited = [vertice for vertice in Grafo]

        while vertice_visited:
            u = min(vertice_visited, key=dist.get)
            vertice_visited.remove(u)
            result.append(u)

            for vecino in Grafo[u]:
                vector = []
                if vecino in vertice_visited and dist[vecino] > dist[u] + Grafo[u][vecino]:
                    real = None
                    index = -1
                    for vertice in recorrido: 
                        actual_vector = vertice
                        i = len(actual_vector)
                        for valores in actual_vector:
                            if valores == u and actual_vector[i-1] == valores:
                                real = actual_vector
                            elif valores == vecino:
                                index = recorrido.index(actual_vector)
                    if index != -1:
                        recorrido.pop(index)
                        index = -1
                    
                    if u != salida:
                        if real != None: 
                            vector = [salida]
                            vector.extend(real)
                            vector.append(vecino)
                        else: 
                            vector = [salida, u, vecino]
                    else:
                        vector = [salida, vecino]

                    recorrido.append(vector)
                    dist[vecino] = dist[u] + Grafo[u][vecino]
                    prev[vecino] = u

        return recorrido

    #Metodo que redibuja los combobox, botones, imagen del mapa, vertices,
    #cuadros de texto (con los mensajes correspondientes), y aristas
    def borrar_info_grafo(self):
        self.mapa_fondo()
        self.dibujar_nodos_mapa()
        self.combo_origen()
        self.combo_destino()
        self.mostrar_rutas_pant()
        self.crear_botones_grafo()
        if self.algorithm_dijktra == True: 
            self.visualizar_recorrido_corto()

        if self.eleccion_1 != None: 
            msg = self.base_font_2.render(self.eleccion_1, 1, (0, 0, 0))
            rect = self.rect_combo_1.copy()
            rect.top += 7
            self.win.blit(msg, rect)
        if self.eleccion_2 != None: 
            msg = self.base_font_2.render(self.eleccion_2, 1, (0, 0, 0))
            rect = self.rect_combo_2.copy()
            rect.top += 7
            self.win.blit(msg, rect)

    #Se registran los destinos posibles para cada ciudad antes guardada
    def relaciones_ciudades(self):
        self.relaciones.append(['Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Leticia', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Medellin', 'Monteria', 'Neiva', 'Pasto', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Leticia', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Barranquilla', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Leticia', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Cali', 'Cartagena', 'Cúcuta', 'Leticia', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cartagena', 'Cúcuta', 'Leticia', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cúcuta', 'Leticia', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Leticia', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Medellin', 'Monteria', 'Pereira', 'Santa Marta'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Leticia', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Leticia', 'Medellin', 'Neiva', 'Pereira', 'Pasto', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Medellin', 'Monteria', 'Pereira', 'Pasto', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Leticia', 'Medellin', 'Monteria', 'Neiva', 'Pasto', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Leticia', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Santa Marta', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Leticia', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Valledupar', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Santa Marta', 'Villavicencio'])
        self.relaciones.append(['San Andrés', 'Armenia', 'Barranquilla', 'Bucaramanga', 'Bogotá', 'Cali', 'Cartagena', 'Cúcuta', 'Leticia', 'Medellin', 'Monteria', 'Neiva', 'Pereira', 'Pasto', 'Santa Marta', 'Valledupar'])
        self.valores_recorridos()

    #Método que dibuja vertices en las diferentes ciudades,
    #cada uno en la ubicación exacta de estos a lo largo del mapa
    def dibujar_nodos_mapa(self):
        tam_image_1 = self.tam_mapa_rect.copy()

        tam_image_1.top += (self.tam_mapa_alto*0.04)
        tam_image_1.right += (self.tam_mapa_ancho*0.0809)

        self.rectas_ciudades.insert(0, tam_image_1)
        if len(self.rectas_ciudades) > 1:
            self.rectas_ciudades.pop(1)
        pygame.draw.circle(self.win, self.rojo, (tam_image_1.left, tam_image_1.top), 4, 5)
        
        tam_image_2 = tam_image_1.copy()
        tam_image_2.left += (self.tam_mapa_ancho*0.20)
        tam_image_2.top += (self.tam_mapa_alto*0.44)
        self.rectas_ciudades.insert(1, tam_image_2)
        if len(self.rectas_ciudades) > 2:
            self.rectas_ciudades.pop(2)
        pygame.draw.circle(self.win, self.rojo, (tam_image_2.left, tam_image_2.top), 4, 5)

        tam_image_3 = tam_image_1.copy()
        tam_image_3.left += (self.tam_mapa_ancho*0.27)
        tam_image_3.top += (self.tam_mapa_alto*0.0602)
        self.rectas_ciudades.insert(2, tam_image_3)
        if len(self.rectas_ciudades) > 3:
            self.rectas_ciudades.pop(3)
        pygame.draw.circle(self.win, self.rojo, (tam_image_3.left, tam_image_3.top), 4, 5)

        tam_image_4 = tam_image_1.copy()
        tam_image_4.left += (self.tam_mapa_ancho*0.407)
        tam_image_4.top += (self.tam_mapa_alto*0.288)
        self.rectas_ciudades.insert(3, tam_image_4)
        if len(self.rectas_ciudades) > 4:
            self.rectas_ciudades.pop(4)
        pygame.draw.circle(self.win, self.rojo, (tam_image_4.left, tam_image_4.top), 4, 5)

        tam_image_5 = tam_image_1.copy()
        tam_image_5.left += (self.tam_mapa_ancho*0.328)
        tam_image_5.top += (self.tam_mapa_alto*0.43)
        self.rectas_ciudades.insert(4, tam_image_5)
        if len(self.rectas_ciudades) > 5:
            self.rectas_ciudades.pop(5)
        pygame.draw.circle(self.win, self.rojo, (tam_image_5.left, tam_image_5.top), 4, 5)

        tam_image_6 = tam_image_1.copy()
        tam_image_6.left += (self.tam_mapa_ancho*0.13)
        tam_image_6.top += (self.tam_mapa_alto*0.5)
        self.rectas_ciudades.insert(5, tam_image_6)
        if len(self.rectas_ciudades) > 6:
            self.rectas_ciudades.pop(6)
        pygame.draw.circle(self.win, self.rojo, (tam_image_6.left, tam_image_6.top), 4, 5)

        tam_image_7 = tam_image_1.copy()
        tam_image_7.left += (self.tam_mapa_ancho*0.2161)
        tam_image_7.top += (self.tam_mapa_alto*0.09)
        self.rectas_ciudades.insert(6, tam_image_7)
        if len(self.rectas_ciudades) > 7:
            self.rectas_ciudades.pop(7)
        pygame.draw.circle(self.win, self.rojo, (tam_image_7.left, tam_image_7.top), 4, 5)

        tam_image_8 = tam_image_1.copy()
        tam_image_8.left += (self.tam_mapa_ancho*0.456)
        tam_image_8.top += (self.tam_mapa_alto*0.239)
        self.rectas_ciudades.insert(7, tam_image_8)
        if len(self.rectas_ciudades) > 8:
            self.rectas_ciudades.pop(8)
        pygame.draw.circle(self.win, self.rojo, (tam_image_8.left, tam_image_8.top), 4, 5)

        tam_image_9 = tam_image_1.copy()
        tam_image_9.left += (self.tam_mapa_ancho*0.658)
        tam_image_9.top += (self.tam_mapa_alto*0.9448)
        self.rectas_ciudades.insert(8, tam_image_9)
        if len(self.rectas_ciudades) > 9:
            self.rectas_ciudades.pop(9)
        pygame.draw.circle(self.win, self.rojo, (tam_image_9.left, tam_image_9.top), 4, 5)

        tam_image_10 = tam_image_1.copy()
        tam_image_10.left += (self.tam_mapa_ancho*0.207)
        tam_image_10.top += (self.tam_mapa_alto*0.338)
        self.rectas_ciudades.insert(9, tam_image_10)
        if len(self.rectas_ciudades) > 10:
            self.rectas_ciudades.pop(10)
        pygame.draw.circle(self.win, self.rojo, (tam_image_10.left, tam_image_10.top), 4, 5)

        tam_image_11 = tam_image_1.copy()
        tam_image_11.left += (self.tam_mapa_ancho*0.18)
        tam_image_11.top += (self.tam_mapa_alto*0.19)
        self.rectas_ciudades.insert(10, tam_image_11)
        if len(self.rectas_ciudades) > 11:
            self.rectas_ciudades.pop(11)
        pygame.draw.circle(self.win, self.rojo, (tam_image_11.left, tam_image_11.top), 4, 5)

        tam_image_12 = tam_image_1.copy()
        tam_image_12.left += (self.tam_mapa_ancho*0.237)
        tam_image_12.top += (self.tam_mapa_alto*0.53)
        self.rectas_ciudades.insert(11, tam_image_12)
        if len(self.rectas_ciudades) > 12:
            self.rectas_ciudades.pop(12)
        pygame.draw.circle(self.win, self.rojo, (tam_image_12.left, tam_image_12.top), 4, 5)

        tam_image_13 = tam_image_1.copy()
        tam_image_13.left += (self.tam_mapa_ancho*0.195)
        tam_image_13.top += (self.tam_mapa_alto*0.42)
        self.rectas_ciudades.insert(12, tam_image_13)
        if len(self.rectas_ciudades) > 13:
            self.rectas_ciudades.pop(13)
        pygame.draw.circle(self.win, self.rojo, (tam_image_13.left, tam_image_13.top), 4, 5)

        tam_image_14 = tam_image_1.copy()
        tam_image_14.left += (self.tam_mapa_ancho*0.076)
        tam_image_14.top += (self.tam_mapa_alto*0.629)
        self.rectas_ciudades.insert(13, tam_image_14)
        if len(self.rectas_ciudades) > 14:
            self.rectas_ciudades.pop(14)
        pygame.draw.circle(self.win, self.rojo, (tam_image_14.left, tam_image_14.top), 4, 5)

        tam_image_15 = tam_image_1.copy()
        tam_image_15.left += (self.tam_mapa_ancho*0.42)
        tam_image_15.top += (self.tam_mapa_alto*0.029)
        self.rectas_ciudades.insert(14, tam_image_15)
        if len(self.rectas_ciudades) > 15:
            self.rectas_ciudades.pop(15)
        pygame.draw.circle(self.win, self.rojo, (tam_image_15.left, tam_image_15.top), 4, 5)

        tam_image_16 = tam_image_1.copy()
        tam_image_16.left += (self.tam_mapa_ancho*0.319)
        tam_image_16.top += (self.tam_mapa_alto*0.044)
        self.rectas_ciudades.insert(15, tam_image_16)
        if len(self.rectas_ciudades) > 16:
            self.rectas_ciudades.pop(16)
        pygame.draw.circle(self.win, self.rojo, (tam_image_16.left, tam_image_16.top), 4, 5)

        tam_image_17 = tam_image_1.copy()
        tam_image_17.left += (self.tam_mapa_ancho*0.4)
        tam_image_17.top += (self.tam_mapa_alto*0.09)
        self.rectas_ciudades.insert(16, tam_image_17)
        if len(self.rectas_ciudades) > 17:
            self.rectas_ciudades.pop(17)
        pygame.draw.circle(self.win, self.rojo, (tam_image_17.left, tam_image_17.top), 4, 5)

        tam_image_18 = tam_image_1.copy()
        tam_image_18.left += (self.tam_mapa_ancho*0.363)
        tam_image_18.top += (self.tam_mapa_alto*0.459)
        self.rectas_ciudades.insert(17, tam_image_18)
        if len(self.rectas_ciudades) > 18:
            self.rectas_ciudades.pop(18)
        pygame.draw.circle(self.win, self.rojo, (tam_image_18.left, tam_image_18.top), 4, 5)

    #Se registra la distancia existente entre la ciudad origen y 
    #cada una de las ciudades destino posibles
    def valores_recorridos(self):
        self.dictionary_relations = {
            self.ciudades[0] : {vertice: random.randint(16, 580) for vertice in self.relaciones[0]},
            self.ciudades[1] : {vertice: random.randint(1, 400) for vertice in self.relaciones[1]},
            self.ciudades[2] : {vertice: random.randint(8, 500) for vertice in self.relaciones[2]},
            self.ciudades[3] : {vertice: random.randint(9, 980) for vertice in self.relaciones[3]},
            self.ciudades[4] : {vertice: random.randint(20, 50) for vertice in self.relaciones[4]},
            self.ciudades[5] : {vertice: random.randint(35, 190) for vertice in self.relaciones[5]},
            self.ciudades[6] : {vertice: random.randint(18, 200) for vertice in self.relaciones[1]},
            self.ciudades[7] : {vertice: random.randint(29, 60) for vertice in self.relaciones[1]},
            self.ciudades[8] : {vertice: random.randint(72, 324) for vertice in self.relaciones[1]},
            self.ciudades[9] : {vertice: random.randint(269, 412) for vertice in self.relaciones[1]},
            self.ciudades[10] : {vertice: random.randint(1, 25) for vertice in self.relaciones[1]},
            self.ciudades[11] : {vertice: random.randint(5, 59) for vertice in self.relaciones[1]},
            self.ciudades[12] : {vertice: random.randint(80, 1000) for vertice in self.relaciones[1]},
            self.ciudades[13] : {vertice: random.randint(15, 24) for vertice in self.relaciones[1]},
            self.ciudades[14] : {vertice: random.randint(860, 870) for vertice in self.relaciones[1]},
            self.ciudades[15] : {vertice: random.randint(1, 9) for vertice in self.relaciones[1]},
            self.ciudades[16] : {vertice: random.randint(56, 70) for vertice in self.relaciones[1]},
            self.ciudades[17] : {vertice: random.randint(6, 15) for vertice in self.relaciones[1]},
        }