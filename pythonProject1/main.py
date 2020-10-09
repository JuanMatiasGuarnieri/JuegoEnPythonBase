import pygame, random

#ancho ventana
WIDTH = 1000#800
#largo ventana
HEIGHT = 563#600

#colores
BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
#inicio librerias
pygame.init()
pygame.mixer.init()#inicio mixer(va a servir para configurar el sonido)
#Creo mi ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juegazo")
#reloj
clock = pygame.time.Clock()

#icono con la Cara de Luis
gameIcon = pygame.image.load("assets/miniaturaJuegoCaraDeLuis.png")
pygame.display.set_icon(gameIcon)

#ventana de Pausa
def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                elif event.key == pygame.K_p:
                    pygame.quit()
                    quit()
            screen.blit(background, [0, 0])
            draw_text(screen, "Pausado", 80, WIDTH // 2, HEIGHT // 4)
            draw_text(screen, "Presione ESC para Continuar o P para Salir", 50, WIDTH // 2, HEIGHT // 2)
            # draw_text(screen, "Presione una tecla", 20, WIDTH // 2, HEIGHT* 3/4)
            pygame.display.flip()




        pygame.display.update()
        clock.tick(5)



#dibujo el score
def draw_text(surface, text, size,x ,y):
    front = pygame.font.SysFont("serif",size,bold=1)
    text_surface = front.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)
#dibujo la barra de vida
def draw_shield_bar(surface,x,y,percentage):
    BAR_LENGHT=350
    BAR_HEIGHT=35
    fill = (percentage/100)*BAR_LENGHT
    border = pygame.Rect(x,y,BAR_LENGHT,BAR_HEIGHT)
    fill = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface,WHITE,border,2) #el 2 es para que sea un poco mas grueso que el 1 que va por defecto

#creo la calse jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/ship2.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100 #vida/escudp

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()#verifico si se presiono una tecla
        if keystate[pygame.K_LEFT]:#si se presiono la tecla izquierda ejecuto:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:#si se presiono la tecla derecha ejecuto:
            self.speed_x = 5
        if keystate[pygame.K_UP]:
            self.speed_y = -5
        if keystate[pygame.K_DOWN]:
            self.speed_y = 5
        self.rect.x += self.speed_x#le sumo la velocidad para mover al jugador
        #para que no se salga el jugador de la ventana pongo los siguientes limites
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top) #creo un disparo que sale del centro de arriba de la nave
        all_sprites.add(bullet)#lo agrego a la lista de sprites
        bullets.add(bullet)#lo agrego a la lista de disparos
        laser_sound.play() #reproduce el sonido cada que dispara

#creo meteoros
class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/meteorGrey_med1.png").convert()
		self.image.set_colorkey(BLACK)#quito el fondo negro
		self.rect = self.image.get_rect()#obtengo la recta
		self.rect.x = random.randrange(WIDTH - self.rect.width)#valor de inicio random
		self.rect.y = random.randrange(-100, -40) #el -100,- 40 es para dar el efecto de que esta bajando
		self.speedy = random.randrange(1, 10)#velocidad
		self.speedx = random.randrange(-5, 5)#para que vaya hacia los cotados

	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 22 :#si el meteoro ya no es visible en la pantalla vuelve a aparecer
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(1, 8)


#creo los disparos
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x   #el center x es el centro del objeto
        #velocidad
        self.speedy = -10 #negativo por que el disparo sube por pantalla

    def update(self):
        #el disparo sube automaticamente
        self.rect.y += self.speedy
        #una vez el disparo sale de la ventana la elimino de la lista de sprites para que no ocupe espacio de memoria
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center):#center:centro la explosion en el asteroide
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 #el contador que cambia las imagenes
        self.last_update = pygame.time.get_ticks() #pausa el reloj del juego para ver los cambios
        self.frame_rate = 50#control de velocidad de explosion
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(explosion_anim):#si llegue al final de la lista eliminos todos los sprites
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background,[0,0])
    draw_text(screen, "Juegazo",85,WIDTH//2,HEIGHT//4)
    draw_text(screen,"Presione una tecla para Jugar",50,WIDTH//2,HEIGHT//2)
    #draw_text(screen, "Presione una tecla", 20, WIDTH // 2, HEIGHT* 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


#Explosion imagenes
explosion_anim = []
for i in range(9):
	file = "assets/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70, 70))
	explosion_anim.append(img_scale)


#cargar imagen de fondo
background = pygame.image.load("assets/background.png").convert()

#cargar sonidos
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")

pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.set_volume(0.1) #volumen musica

def cargar_meteoro():
    meteor = Meteor()  # vuelvo a crear meteros si los destrui
    all_sprites.add(meteor)
    meteor_list.add(meteor)

#Game Over
game_over = True

pygame.mixer.music.play(loops = - 1) #reproduzco musica

#Bucle principal
running = True
while running:

    if game_over:

        show_go_screen()

        game_over = False
        # creo instancia jugador
        player = Player()
        # creo un grupo para almacenar jugador
        all_sprites = pygame.sprite.Group()
        # agrego jugador a la lista
        all_sprites.add(player)
        # creo grupo para meteoros
        meteor_list = pygame.sprite.Group()
        # grupo de disparos
        bullets = pygame.sprite.Group()

        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)  # lo agrego a la lista de todos los sprites
            meteor_list.add(meteor)  # agrego a la lista de meteoros

        score = 0

    clock.tick(60)#60 frames por segundo

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:#salgo del programa
            running = False
        elif event.type == pygame.KEYDOWN:#con la tecla space se dispara
            if event.key == pygame.K_SPACE:
                player.shoot()
            elif event.key == pygame.K_ESCAPE:
                pause()

    all_sprites.update()

    #detectar-colision-meteoro-disparo                   #2 true para que desaparezcan los disparos y los asteroides
    hits = pygame.sprite.groupcollide(meteor_list,bullets,True,True)#groupcollide verifica las colisiones de un grupo contra otro grupo
    for hit in hits:
        score +=1 #aumenta 1 el score por cada asteroide destruido
        explosion_sound.play() #reproduce el sonido de la explosion
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        cargar_meteoro() #vuelvo a crear meteros si los destrui

    #detectar-colision-nave-asteroide
    hits =pygame.sprite.spritecollide(player, meteor_list, True) #con True desapareden los objetos,con False no pasa nada
    for hit in hits:
        player.shield -=25
        explosion_sound.play()  # reproduce el sonido de la explosion
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        cargar_meteoro()  # vuelvo a crear meteros si los destrui
        if player.shield <= 0:
            game_over = True

    screen.blit(background,[0,0])
    all_sprites.draw(screen)

    #Score
    draw_text(screen, str(score),45,WIDTH//2,10)
    #Salud
    draw_shield_bar(screen,5,5,player.shield)

    pygame.display.flip()

pygame.quit()









