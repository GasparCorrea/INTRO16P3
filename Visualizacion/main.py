import os
import pygame
from random import randint, choice
from pygame.locals import *
from escenas import *
from time import sleep

TITULO = "Intro 2016"

#  Constantes de tamanhos para dibujar.
SPACESHIPS = 45
BATTLEFIELDSIZE = 460.0
BATTLEFIELDDIVISIONS = 20
BATTLEFIELDINICIO = (351, 10)
ESCALA = 4.0/BATTLEFIELDDIVISIONS

# Constantes de giro de las naves.
MOV = {"up": (0,  -1),
       "down": (0, 1),
       "left": (-1,  0),
       "rigth": (1,  0)}

SETH = {"up": 0,
        "down": 180,
        "left": 90,
        "rigth": -90}

# Constantes del juego
Q_turnos = 5
MAX_vidas = 5

# --------------------
# DEFINICION DE CLASES
# --------------------

# Clases de escenas.


class Inicio(Scene):

    """ Ventana de inicio del juego"""

    def __init__(self, director, path_log):
        Scene.__init__(self, director)
        # Informacion de escena
        background_path = os.path.join("data", "background", "portada.jpg")
        self.background = load_image(background_path)

        # Estados de escena
        self.start_replay = False

        # Informacion del replay
        with open(path_log) as log:
            self.replay = log.readlines()
        self.players = cargar_jugadores(self.replay)

        # Musica
        musica_path = os.path.join("data", "music", "xeon6(intro).ogg")
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play(0, 0.0)

    def on_update(self):
        """ Actualizar datos, cambia de escena si es necesario. """

        if self.start_replay:
            pygame.mixer.music.stop()
            self.director.change_scene(Principal(self.director,
                                                 self.players,
                                                 self.replay))

    def on_event(self, event):
        """ Revisa si ocurrio un evento en el bucle principal. """

        if event:
            self.start_replay = True

    def on_draw(self, screen):
        """ Refrescar datos en la pantalla."""

        screen.blit(self.background, (0, 0))


class Principal(Scene):

    """ Aqui se muestra toda la accion, se lee el log, se ven
        los jugadores, sfx, movimientos, etc."""

    def __init__(self, director, dict_players, replay):
        Scene.__init__(self, director)
        # Informacion de escena
        background_path = os.path.join("data", "background", "tablero.jpg")
        self.background = load_image(background_path)

        # Estados de escena
        self.next_turn = True
        self.end_replay = False
        self.linea = ""

        # Informacion del replay
        self.replay = replay
        self.players = dict_players

        # Musica
        musica_path = os.path.join(
            "data", "music", "Arabesque(Main theme).mp3")
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play(100, 0.0)

        # Datos dibujo
        self.acciones = ["","","","","","","","",""]
        self.turnos_restantes = Q_turnos

    def on_update(self):
        """ Actualizar datos, cambia de escena si es necesario. """

        # Si se termino de leer la partida, pasar a los resultados.
        if self.end_replay:
            self.director.change_scene(Estadisticas(self.director,
                                                    self.players))

        # Si se termino de actualizar los datos de un turno, leer el siguiente.
        if self.next_turn:
            del self.acciones[-1]
            self.acciones.insert(0,"")
            self.next_turn = False
            linea = self.replay.pop(0)
            self.linea = linea.strip().split(":")
        accion, argumentos = self.linea
        discriminar_accion(self, accion, argumentos)

    def on_event(self, event):
        """ Revisa si ocurrio un evento en el bucle principal. """

        if event:
            pygame.mixer.music.stop()
            # TEST
            self.end_replay = True

    def on_draw(self, screen):
        """ Refrescar datos en la pantalla."""

        # Fondo
        screen.blit(self.background, (0, 0))

        # Cuadrilla
        dibujar_cuadricula(screen)

        # Textos.
        for i,texto in enumerate(self.acciones):
            if i == 0:
                textinscreen = fuente1.render(texto, 1, (255,255,255))
                screen.blit(textinscreen , (15,90))
            else:
                textinscreen = fuente2.render(texto, 1, (255,255,255))
                screen.blit(textinscreen , (15,85-i*10))

        # Jugadores
        for ide, jugador in self.players.items():
            jugador.mostrar(screen)


class Estadisticas(Scene):
    # TODO

    """ Ventana final del juego, muestra los resultados, tablas, etc."""

    def __init__(self, director, dict_players):
        Scene.__init__(self, director)
        # Informacion de escena
        background_path = os.path.join("data", "background", "portada.jpg")
        self.background = load_image(background_path)

        # Informacion del replay
        self.players = dict_players

        # Musica
        musica_path = os.path.join(
            "data", "music", "Victory and Respite(end).mp3")
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play(0, 0.0)

    def on_update(self):
        """ Actualizar datos, cambia de escena si es necesario. """

        # TODO
        pass

    def on_event(self, event):
        """ Revisa si ocurrio un evento en el bucle principal. """

        # TODO
        if event:
            pass

    def on_draw(self, screen):
        """ Refrescar datos en la pantalla."""

        # TODO
        screen.blit(self.background, (0, 0))
        pass


# Clases de sprites.

class Jugador(pygame.sprite.Sprite):

    """ Informacion de un jugador """

    def __init__(self, ID):
        pygame.sprite.Sprite.__init__(self)
        # Datos jugador.
        self.ID = ID
        self.alerta = 0
        self.vidas = 2
        self.battlefieldpos_x = 0
        self.battlefieldpos_y = 0
        self.orientacion = 0
        self.visible = True

        # Datos dibujo.
        idspaceship = randint(0, SPACESHIPS-1)
        spaceship = choice(os.listdir(os.path.join("data",
                                                   "sprites",
                                                   "Players")))
        spaceship_path = os.path.join("data",
                                      "sprites",
                                      "Players",
                                      spaceship)

        explotion1_path = os.path.join("data",
                                       "sprites",
                                       "Explotions",
                                       "Explosion1.png")

        explotion2_path = os.path.join("data",
                                       "sprites",
                                       "Explotions",
                                       "Explosion2.png")

        self.images = list()
        self.images.append(cargar_sprite(spaceship_path))
        self.images.append(cargar_sprite(explotion1_path))
        self.images.append(cargar_sprite(explotion2_path))

        self.visible = 0
        self.image = self.images[self.visible]
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.centery = 0

    def aparecer(self, (coor_x, coor_y)):
        """ Coloca un jugador en las coordenadas de cuadrilla x, y."""

        self.visible = 0
        self.image = self.images[self.visible]

        self.battlefieldpos_x = coor_x
        self.battlefieldpos_y = coor_y
        self.orientacion = 0

        new_x, new_y = transformar_coordenadas(coor_x, coor_y)
        self.rect.centerx = new_x
        self.rect.centery = new_y

    def mostrar(self, screen):
        """ Muestra en pantalla el sprite del jugador."""
        if self.visible != -1:
            screen.blit(self.image, self.rect)

    def mover(self, direccion):
        """ Cambia la posicion de un jugador hacia la direccion dada."""

        X, Y = MOV[direccion]
        if SETH[direccion] != self.orientacion:
            rotar = SETH[direccion]-self.orientacion
            self.orientacion = SETH[direccion]
            self.image = pygame.transform.rotate(self.image, rotar)
        else:
            self.battlefieldpos_x = round(self.battlefieldpos_x + X*0.1, 2)
            self.battlefieldpos_y = round(self.battlefieldpos_y + Y*0.1, 2)

            if self.battlefieldpos_y < -1:
                self.battlefieldpos_y = BATTLEFIELDDIVISIONS
            if self.battlefieldpos_y > BATTLEFIELDDIVISIONS+1:
                self.battlefieldpos_y = 0

            if self.battlefieldpos_x < -1:
                self.battlefieldpos_x = BATTLEFIELDDIVISIONS
            if self.battlefieldpos_x > BATTLEFIELDDIVISIONS+1:
                self.battlefieldpos_x = 0

            new_x, new_y = transformar_coordenadas(self.battlefieldpos_x,
                                                   self.battlefieldpos_y)
            self.rect.centerx = new_x
            self.rect.centery = new_y

    def disparar(self, direccion):
        # TODO

        pass

    def quitar_vida(self):
        # TODO

        pass

    def morir(self):
        if self.visible == 0:
            self.visible += 1
            flag = False
            print "musica",

        elif self.visible == 1:
            self.visible += 1
            flag = False

        elif self.visible == 2:
            flag = True

        self.image = self.images[self.visible]
        return flag


    def cambiar_alerta(self, cambio):
        # TODO
        pass

# TODO


class Bala(pygame.sprite.Sprite):

    """ Objeto que representara a los disparos. """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Datos dibujo
        self.imagenes = list()
        for laser in os.listdir(os.path.join("data",
                                             "sprites",
                                             "Laser")):
            path = os.path.join("data",
                                "sprites",
                                "Laser",
                                laser)

            self.imagenes.append(load_image(path, True))

        self.rect = self.imagenes[0].get_rect()
        self.rect.centerx = 0
        self.rect.centery = 0


# ------------------------
# DEFINICION DE FUNCIONES
# ------------------------

def cargar_sprite(path, escala=ESCALA):

    image = load_image(path, True)

    width, height = image.get_size()

    return pygame.transform.scale(image,
                                  (int((width*escala)),
                                   int(height*escala)))


def dibujar_cuadricula(screen):
    cuadrado = BATTLEFIELDSIZE / BATTLEFIELDDIVISIONS
    coor_x = BATTLEFIELDINICIO[0]
    coor_y = BATTLEFIELDINICIO[1]
    while coor_x < BATTLEFIELDINICIO[0]+BATTLEFIELDSIZE+cuadrado:
        pygame.draw.line(screen, (125, 125, 125),
                         (coor_x, BATTLEFIELDINICIO[1]),
                         (coor_x, BATTLEFIELDINICIO[1]+BATTLEFIELDSIZE),
                         1)
        pygame.draw.line(screen, (125, 125, 125),
                         (BATTLEFIELDINICIO[0], coor_y),
                         (BATTLEFIELDINICIO[0]+BATTLEFIELDSIZE, coor_y),
                         1)
        coor_x += cuadrado
        coor_y += cuadrado


def transformar_coordenadas(coor_x, coor_y):
    cuadrado = BATTLEFIELDSIZE / BATTLEFIELDDIVISIONS
    new_x = BATTLEFIELDINICIO[0]+(coor_x*cuadrado)+(cuadrado/2)
    new_y = BATTLEFIELDINICIO[1]+(coor_y*cuadrado)+(cuadrado/2)
    return new_x, new_y


def cargar_jugadores(log):
    jugadores = dict()
    while True:
        linea = log.pop(0)
        accion, argumentos = linea.strip().split(":")
        if accion == "conectado":
            print "conectado:", argumentos
            jugadores[argumentos] = Jugador(argumentos)
        elif argumentos == "comenzar":
            return jugadores

# TODO


def discriminar_accion(scene, accion, argumentos):
    """ Por cada comando del logfile, determina que accion tomar."""

    if accion == "aparecer":
        sleep(0.05)
        ID, x, y = argumentos.split(",")
        jugador = scene.players[ID]
        jugador.aparecer((int(x), int(y)))
        scene.next_turn = True
        scene.acciones[0] = "Aparecio: {0} en: ({1},{2})".format(ID,x,y) 

    # falta si termina la partida
    elif accion == "juego" and argumentos == "terminar":
        sleep(3)
        scene.end_replay = True

    elif accion == "moverse":
        ID, new_x, new_y = argumentos.split(",")
        scene.acciones[0] = "Movimiento: {0} hacia: ({1},{2})".format(ID,new_x,new_y)
        new_x = int(new_x)
        new_y = int(new_y)

        jugador = scene.players[ID]
        coor_x = jugador.battlefieldpos_x
        coor_y = jugador.battlefieldpos_y
        resultado = (round(new_x - coor_x, 2), round(new_y - coor_y, 2))

        if 0.01 < resultado[0] <= 1 or resultado[0] < -1:
            jugador.mover("rigth")
        elif -0.01 > resultado[0] >= -1 or resultado[0] > 1:
            jugador.mover("left")
        elif 0.01 < resultado[1] <= 1 or resultado[1] < -1:
            jugador.mover("down")
        elif -0.01 > resultado[1] >= -1 or resultado[1] > 1:
            jugador.mover("up")
        else:
            scene.next_turn = True

    # TODO
    elif accion == "disparar":
        origen, coor_x, coor_y, objetivo = argumentos.split(",")
        if objetivo == "None":
            scene.acciones[0] = "Disaparo fallido: {0} a ({1},{2})".format(origen, coor_x, coor_y)
        else:
            scene.acciones[0] = "Disaparo acertado: {0} a {1}".format(origen,objetivo)
        jugador_origen = scene.players[origen]
        pass

    elif accion == "muerte":
        sleep(0.7)
        scene.acciones[0] = "Muere: {0}".format(argumentos)
        jugador = scene.players[argumentos]
        scene.next_turn = jugador.morir()
        if scene.next_turn:
            scene.turnos_restantes = Q_turnos

    elif accion == "colision":
        sleep(0.7)
        scene.acciones[0] = "Colisiona: {0}".format(argumentos)
        jugador = scene.players[argumentos]
        scene.next_turn = jugador.morir()
        if scene.next_turn:
            scene.turnos_restantes = Q_turnos


    elif accion == "desconectado":
        sleep(0.5)
        scene.acciones[0] = "Se ha desconectado: {0}".format(argumentos)
        del scene.players[argumentos]
        scene.next_turn = True


    # TODO
    elif accion == "resultado":
        pass

    elif accion == "alertar":
        ID, nivel = argumentos.split(",")
        scene.players[ID].alerta = int(nivel)
    
    else:
        print accion, argumentos
        pass

# -----
# MAIN
# -----

if __name__ == "__main__":
    #path = raw_input("Ingrese log: ")
    path = "test.log"
    Main = MainFrame(TITULO)
    Main.change_scene(Inicio(Main, path))
    Main.loop()
