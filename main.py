import pygame
import random

pygame.init()
clock = pygame.time.Clock()

# Game Window
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Variables
FPS = 80
ground_scroll = 0
speed = 5
flying = False
game_over = False
pipe_gap = 150

last_pipe = pygame.time.get_ticks() - 1500

# Loading Images
background = pygame.transform.scale(pygame.image.load('assets/bg.png'),(screen_width, screen_height)).convert_alpha()
ground = pygame.image.load("assets/ground.png").convert_alpha()
restart = pygame.image.load("assets/restart.png").convert_alpha()

restart_rect = restart.get_rect(center=(screen_height/2, 300))

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        for i in range(1, 4):
            img = pygame.image.load(f"assets/bird{i}.png")
            self.images.append(img)
        self.rect = img.get_rect(center=(x, y))
        self.image = self.images[self.index]
        self.gravity = 0
        self.buttondown = False
        

    def update(self):
        if flying == False:
            self.gravity += 0.2
            if self.gravity > 8:
                self.gravity = 8
            self.rect.y += self.gravity

        self.index += 0.2
        self.image = self.images[int(self.index) % len(self.images)]

        if len(self.images) <= self.index:
            self.index = 0

        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.buttondown == False:
                self.buttondown = True
                self.gravity = -8

            if pygame.mouse.get_pressed()[0] == 0:
                self.buttondown = False

            self.image = pygame.transform.rotate(self.images[int(self.index)], self.gravity * -2)
        
        else:
            self.image = pygame.transform.rotate(self.images[int(self.index)], -90)
        
            
        

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/pipe.png')
        self.rect = self.image.get_rect()
                
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
                        
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
                        
    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()
        
bird_group = pygame.sprite.Group()
Flappy = Bird(50, screen_height/2)
bird_group.add(Flappy)


pipe_group = pygame.sprite.Group()


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
 
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or Flappy.rect.top < 0:
        game_over = True
    
    time_now = pygame.time.get_ticks()
    if game_over == False:
        if time_now - last_pipe > 1500:
            random_pipe_pos = [100, 200, 250, 350, 300]
            take_pipe_pos = random.choice(random_pipe_pos)
            btm_pipe = Pipe(700, take_pipe_pos, 1)
            top_pipe = Pipe(700, take_pipe_pos, -1)
            pipe_group.add(top_pipe)
            pipe_group.add(btm_pipe)
            last_pipe = time_now
    
    screen.blit(background, (0, 0)) 
    pipe_group.draw(screen)
    pipe_group.update()
    screen.blit(ground, (ground_scroll, 500))


    if Flappy.rect.bottom >= 500:
        game_over = True

    if game_over == False:  
        flying = False
        bird_group.draw(screen)
        bird_group.update()
        ground_scroll -= speed
        if abs(ground_scroll - speed) > 35:
            ground_scroll = 0
    
    else:
        screen.blit(restart, restart_rect)

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()