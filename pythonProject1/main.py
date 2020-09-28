import pygame, random

#ancho ventana
WIDTH = 800
#largo ventana
HEIGHT = 600

#colores
BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED = (255,0,0)

#inicio librerias
pygame.init()
pygame.mixer.init()#inicio mixer(va a servir para configurar el sonido)
#Creo mi ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juegazo")
#reloj
clock = pygame.time.Clock()
#creo la calse jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/shipp.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()#verifico si se presiono una tecla
        if keystate[pygame.K_LEFT]:#si se presiono la tecla izquierda ejecuto:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:#si se presiono la tecla derecha ejecuto:
            self.speed_x = 5
        self.rect.x += self.speed_x#le sumo la velocidad para mover al jugador

        #para que no se salga el jugador de la ventana pongo los siguientes limites
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
#creo meteoros
class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/meteorGrey_med1.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100, -40)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 5)

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 22 :
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)


#creo un grupo para almacenar jugador
all_sprites = pygame.sprite.Group()
#creo instancia jugador
player = Player()
#agrego jugador a la lista
all_sprites.add(player)


#Bucle principal
running = True
while running:

    clock.tick(60)#60 frames por segundo

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:#salgo del programa
            running = False


    # Update
    all_sprites.update()

    # Draw / Render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    # * después * de dibujar todo, voltea la pantalla.
    pygame.display.flip()

pygame.quit()








