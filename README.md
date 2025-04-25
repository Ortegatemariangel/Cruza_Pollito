# Juego del pollito

- Este juego consiste en un pollito que necesita cruzar al otro lado de la calle sin colisionar con los carros, el pollito tiene 3 oportunidades (vidas) para lograrlo.

### Para empezar la programacion de este juego lo primero que tenemos que hacer es importar las librerias necesarias, en este caso fueron : 
- import pygame
- import random

### Despues de esto inicializamos pygame, definimos el ancho de la venteana, el nombre del juego, los colores y los carriles, asi como esto:

ANCHO, ALTO = 600, 600

CARRILES_SUP = [250, 280]
CARRILES_INF = [320, 350]

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Autopista con casitas y sprites")
reloj = pygame.time.Clock()

AMARILLO = (255, 255, 0)
AZUL_CIELO = (135, 206, 235)
GRIS_OSCURO = (50, 50, 50)
AMARILLO_LINEA = (255, 255, 0)
VERDE = (0, 255, 0)
rosa = (255, 182, 193)
cafe = (139, 69, 19)
celeste = (173, 216, 230)

### Despues definimos la clase "casa"

class Casa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 60), pygame.SRCALPHA)
        self.dibujar_casa()
        self.rect = self.image.get_rect(topleft=(x, y))

    def dibujar_casa(self):
    
        pygame.draw.rect(self.image, rosa, (0, 10, 50, 50))
        pygame.draw.polygon(self.image, cafe, [(0, 10), (25, 0), (50, 10)])
        pygame.draw.rect(self.image, celeste, (10, 25, 10, 10))
        pygame.draw.rect(self.image, celeste, (30, 25, 10, 10))

- Lo que hicimos anteriormente fue definir la clase casa y definir la imagen de la casa, con pygame.SRCALPHA lo que hicimos fue darle transparencia a el fondo de la casa que fue para guiarnos, posterior a eso hacemos una casa sobre como queremos que queden las demas, le agregamos colores y las coordenadas, como estamos trabajando con Sprite group no es necesario hacer todas las casas una por una, lo cual facilita el trabajo.

### Lo siguiente es definir la clase "carro"

class Carro(pygame.sprite.Sprite):
    def __init__(self, x, y, vel_x):
        super().__init__()
        self.image = pygame.Surface((30, 30)) 
        self.image.fill(VERDE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = vel_x

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.right < 0 or self.rect.left > ANCHO:
            self.kill()

- Igual que con la clase "casa" definimos la imagen y el tamaño de los cuadrados que simulan los carros, definimos el color, la velocidad, las coordenadas y la posicion en la que se muevan los carros si se mueven a la derecha o a la izquierda. 

### Definimos la clase "jugador"

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 25))
        self.image.fill(AMARILLO)
        self.rect = self.image.get_rect(center=(ANCHO // 2, ALTO - 50))
        self.velocidad = 5

    def update(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad

- Al igual que en las clases anteriores definimos la imagen del objeto , el tamaño, el color y la velocidad.
- Como es el jugaddor debe moverse, entonces le ponemos un condicional para que cuando se le presionen las teclas para mover a la drecha, izquierda, arriba y abajo.

### Agregamos los grupos 

grupo_casas = pygame.sprite.Group()
grupo_carros = pygame.sprite.Group()
jugador = Jugador()
grupo_jugador = pygame.sprite.GroupSingle(jugador)

for x in range(0, ANCHO, 60):
    grupo_casas.add(Casa(x + 5, 40)) 
    grupo_casas.add(Casa(x + 5, ALTO - 100)) 

- Pues aca agregamos los grupos, pero como el jugador esta solo se le pone el modo single, tambien agregamos un for in range que consiste en crear un rango de numero de casas para agruparlas y que sea mas sencillo hacerlo, tambien ponemos coordenadas.

### Creamos y definimos las clase "Carros" y la "autopista"

def crear_carro():
    if random.random() < 0.03:
        if random.random() < 0.5:
            y = random.choice(CARRILES_SUP)
            carro = Carro(ANCHO, y, -3)
        else:
            y = random.choice(CARRILES_INF)
            carro = Carro(-30, y, 3)
        grupo_carros.add(carro)

def dibujar_autopista():
    pygame.draw.rect(pantalla, GRIS_OSCURO, (0, 240, ANCHO, 120))
    pygame.draw.line(pantalla, AMARILLO_LINEA, (0, 300), (ANCHO, 300), 2)

- para crear el carro aregamos un random con numero de tiempo y posiciones aleatorias, en los carriles superiores e inferiores.

- Para la autopista solo hicimos un rectangulo de color gris oscuro, le agregamos las coordenadas y tambien una linea amarilla en la mitad que separe los carriles, le agregamos las coordenadas y el grosor de la linea rellenada.

### Colisiones
colisiones = 0
MAX_COLISIONES = 3
ejecutando = True

- Agregamos esto para el numero de vidas del pollito, el contador de colisiones empiezan desde cero, a medida que se va ejecutando tiene un maximo de 3 oportunidadess osea solo puede chocar 3 veces maximo y agregamos el true para que mientras se esta ejecutando el juego se haga eta funcion.

### Bucle, Agregamos un while.

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()
    pantalla.fill(AZUL_CIELO)

    crear_carro()
    grupo_carros.update()
    jugador.update(teclas)

    if pygame.sprite.spritecollide(jugador, grupo_carros, True):
        colisiones += 1
        if colisiones >= MAX_COLISIONES:
            print("¡GAME OVER!")
            ejecutando = False

### Agregamos a la pantalla los grupos 

    dibujar_autopista()
    grupo_casas.draw(pantalla)
    grupo_carros.draw(pantalla)
    grupo_jugador.draw(pantalla)

    pygame.display.flip()
    reloj.tick(60)

### Se ejecuta con :

- pygame.quit()