import pygame
import random

pygame.init()

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

class Casa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 60), pygame.SRCALPHA)
        self.dibujar_casa()
        self.rect = self.image.get_rect(topleft=(x, y))

    def dibujar_casa(self):
        rosa = (255, 182, 193)
        cafe = (139, 69, 19)
        celeste = (173, 216, 230)
        pygame.draw.rect(self.image, rosa, (0, 10, 50, 50))
        pygame.draw.polygon(self.image, cafe, [(0, 10), (25, 0), (50, 10)])
        pygame.draw.rect(self.image, celeste, (10, 25, 10, 10))
        pygame.draw.rect(self.image, celeste, (30, 25, 10, 10))

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

grupo_casas = pygame.sprite.Group()
grupo_carros = pygame.sprite.Group()
jugador = Jugador()
grupo_jugador = pygame.sprite.GroupSingle(jugador)

for x in range(0, ANCHO, 60):
    grupo_casas.add(Casa(x + 5, 40)) 
    grupo_casas.add(Casa(x + 5, ALTO - 100)) 

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

colisiones = 0
MAX_COLISIONES = 3
ejecutando = True

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

    dibujar_autopista()
    grupo_casas.draw(pantalla)
    grupo_carros.draw(pantalla)
    grupo_jugador.draw(pantalla)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()