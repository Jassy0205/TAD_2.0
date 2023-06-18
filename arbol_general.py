import pygame
pygame.init()   

    #Se crea una función que imprima el titulo del primer input: El número de nodos a dibujar
    def input_title(self):
        text_surface = self.base_font.render(self.base, True, (100,30,22))
        self.win.blit(text_surface, (30,10))

    #función que imprima el titulo de los dos input siguientes: 
    #valor del nodo hijo y el valor del padre
    def input_value_and_father(self):
        text_surface = self.base_font.render(self.value, True, (100,30,22))
        self.win.blit(text_surface, (30,50))

        text_surface = self.base_font.render(self.father, True, (100,30,22))
        self.win.blit(text_surface, (550,50))

    #Función que acciona todo el proceso del arbol
    def input_information(self):
        self.input_title()
        self.input_nodes()
        input_rect_1 = pygame.Rect(200, 45, 50, 30)
        input_rect_2 = pygame.Rect(720, 45, 80, 30)
        cont = 0

        while not self.terminar_arbol:
            for event in pygame.event.get():

                if event.type == pygame.QUIT: 
                    self.terminar_arbol = True

                while cont < self.numeros:
                    self.input_value_and_father()
                    pygame.draw.rect(self.win, (0,0,0), input_rect_1, 2)
                    pygame.draw.rect(self.win,  (0,0,0), input_rect_2, 2)

                    i = self.input_value(input_rect_1, input_rect_2)
                    j = self.input_father(input_rect_1, input_rect_2)
                    self.draw_nodes()

                    if j == "Hola" or i == "Hola": 
                        cont = self.numeros
                    elif j == True: 
                        cont += 1

                    self.borrar_info(input_rect_1, input_rect_2)

                print(self.nodes)
                print(self.parents)
                self.draw_nodes()

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE: 
                        self.user_text = self.user_text[:-1]
                        self.win.fill((255,255,255))
                        self.input_title()
                    elif event.key == pygame.K_SPACE:
                        r = self.validar_int(self.user_text)
                        if r != False:
                            self.terminar_1 = True
                        else: 
                            self.user_text = self.user_text[:-1]
                            self.win.fill((255,255,255))
                            self.input_title()
                    else:
                        self.user_text += event.unicode

            pygame.draw.rect(self.win, (0,0,0), self.input_rect, 2)
            text_surface = self.base_font.render(self.user_text, True, (28,40,51))
            self.win.blit(text_surface, (350,10))
            pygame.display.flip()

        self.numeros = r
        print(self.numeros)

    def validar_nodo_cabeza(self, father):
        padre = father.lower()
        print(padre, 'g', len(self.nodes))

        if len(self.nodes) == 1:
            if padre == "n" or padre == "none":
                self.parents.append(father)
                return True 
            else:
                self.out_range()
                self.nodes = []
                return False
        elif self.parents[0] == 'n' or self.parents[0] == 'none':
            self.parents.append(father)

    #Metodo que reciba la información del input del valor del nodo a ingresar
    def input_value(self, input_rect_1, input_rect_2):
        terminar_value = False
        value = ''

        while not terminar_value:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    terminar_value = True
                    return "Hola"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: 
                        terminar_value = True
                    elif event.key == pygame.K_BACKSPACE: 
                        value = value[:-1]
                        self.borrar_info(input_rect_1, input_rect_2)
                    else:
                        value += event.unicode

            text_surface_1 = self.base_font.render(value, True, (27,48,49))
            self.win.blit(text_surface_1, (210,50))
            pygame.display.flip()

        self.ingresar_node(value, input_rect_1, input_rect_2)

    #Se verifica que el nuevo noodo que se desea ingresar no esté ya incorporado en la lista
    def ingresar_node(self, value, input_rect_1, input_rect_2):
        if value in self.nodes:
            self.borrar_info(input_rect_1, input_rect_2)
            self.input_value(input_rect_1, input_rect_2)
        else: 
            self.nodes.append(value)

    #Metodo que reciba la información del input del valor del nodo padre
    # del nuevo nodo a ingresar
    def input_father(self, input_rect_1, input_rect_2):
        terminar_father = False
        father = ''

        while not terminar_father:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    terminar_father = True
                    return "Hola"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: 
                        terminar_father = True
                    elif event.key == pygame.K_BACKSPACE: 
                        father = father[:-1]
                        self.borrar_info(input_rect_1, input_rect_2)
                    else:
                        father += event.unicode

            text_surface_2 = self.base_font.render(father, True, (27,48,49))
            self.win.blit(text_surface_2, (730,50))
            pygame.display.flip()

        #self.parents.append(father)
        r = self.validar_nodo_cabeza(father)
        return r

    def borrar_info(self, input_rect_1, input_rect_2):
        self.win.fill((255,255,255))
        self.input_title()
        self.input_value_and_father()
        pygame.draw.rect(self.win, (0,0,0), self.input_rect, 2)
        pygame.draw.rect(self.win, (0,0,0), input_rect_1, 2)
        pygame.draw.rect(self.win, (0,0,0), input_rect_2, 2)
        text_surface = self.base_font.render(self.user_text, True, (28,40,51))
        self.win.blit(text_surface, (350,10))
        self.draw_nodes()

    #Metodo que busca y dibuja a la raíz del arbol 
    def draw_nodes(self):
        x = 300
        y = 160
        listo = False
        cont = 0
        i = 0

        while not listo and len(self.nodes) >= 1 and len(self.parents) >= 1:
            if self.parents[i] == 'n' or self.parents[i] == 'none':
                pygame.draw.circle(self.win, (100,10,255), (400,100), 20, 5)
                texto = self.nodes[i]
                text_surface = self.base_font.render(texto, True, (0,255,255))
                self.win.blit(text_surface, (392,90))
                self.son_padre(self.nodes[i], 400, 100)
                listo = True
                cont += 1
            elif cont == 0 and i == len(self.parents)-1:
                cont += 1
                #self.out_range()
                listo = True

            i += 1
            pygame.display.flip()

    #Imprime un mensaje en la interfaz grafica si no se ingresa un nodo "raíz" al arbol
    def out_range(self):
        text = '---------- NO HAY NODO RAIZ -------------'
        text_surface = self.base_font.render(text, True, (255,0,0))
        self.win.blit(text_surface, (150,self.alto-20))
        pygame.display.flip()

    #Metodo que dibuja los circulos para representar los nodos graficamente 
    # y las lineas que representan los enlaces entre los nodos
    def son_padre(self, value, xinicial, yinicial):
        y = yinicial+100
        suma = y/100
        x = xinicial - (suma*50)
        resta = 50

        for i in range(len(self.parents)):
            if value == self.parents[i]:
                print(x,'hola', self.nodes[i])
                if suma > 2:
                    print('hg1')
                    x += 50
                pygame.draw.circle(self.win, (100,10,255), (x,y), 20, 5)
                pygame.draw.line(self.win, (100,0,105), (xinicial-5,yinicial+10), (x,y-10), 4)
                texto = self.nodes[i]
                text_surface = self.base_font.render(texto, True, (0,255,255))
                self.win.blit(text_surface, (x-5,y-10))
                
                pygame.display.flip()

                self.son_padre(self.nodes[i], x, y)
                if suma > 2:
                    print('hg')
                    x -= 80
                    resta += (suma*40)
                x += ((suma*100)+70)-resta
