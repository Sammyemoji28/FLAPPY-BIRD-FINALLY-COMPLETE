
import pygame
import random

pygame.init()

screen = pygame.display.set_mode((864, 936))
pygame.display.set_caption("FALLPY (FLAPPY) BIRD")

WIDTH = 864
HEIGHT = 936

fps = 60
clock = pygame.time.Clock()

groundScroll = 0
scrollSpeed = 4
flying = False
gameover = False
pipeGap = 150
pipeFrequency = 1500
lastPipe = pygame.time.get_ticks() - pipeFrequency
score = 0
font = pygame.font.SysFont("calibri", 40)
WHITE = (255,255,255)
passPipe = False

bg = pygame.image.load("img/bg.png")
ground = pygame.image.load("img/ground.png")
restartImg = pygame.image.load("img/restart.png")

run = True

class Flappy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1,4):
            img = pygame.image.load(f"img/bird{i}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.velocity = 0
        self.clicked = False

    def update(self):
        if flying == True:
            self.velocity += 0.5
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.velocity)
        
        if gameover == False:
            if self.clicked == False and pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                self.velocity = -10
            if pygame.mouse.get_pressed()[0] == 0:
               self.clicked = False
            self.counter += 1
            flapCooldown = 5
            if self.counter > flapCooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()

        # - pos 1 is TOP pos, and pos -1 is BOTTOM pos
        if pos == -1:
            self.rect.topleft = [x,y + int(pipeGap//2)]
        if pos == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(pipeGap//2)]
    
    def update(self):
        self.rect.x -= scrollSpeed
        if self.rect.right < 0:
            self.kill()

class Restart():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def display(self):
        action = False
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

pipeGroup = pygame.sprite.Group()
birdGroup = pygame.sprite.Group()

flappyBird = Flappy(100, HEIGHT//2)
birdGroup.add(flappyBird)

restart = Restart(WIDTH//2 - 50, HEIGHT//2 - 100, restartImg)

def resetGame():
    global score
    pipeGroup.empty()
    flappyBird.rect.x = 100
    flappyBird.rect.y = HEIGHT//2
    score = 0

while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))
    screen.blit(ground, (groundScroll, 768))

    # - drawing the bird group
    birdGroup.draw(screen)
    birdGroup.update()
    pipeGroup.draw(screen)

    # - check the score
    if len(pipeGroup) > 0:
        if birdGroup.sprites()[0].rect.left > pipeGroup.sprites()[0].rect.left\
            and birdGroup.sprites()[0].rect.right < pipeGroup.sprites()[0].rect.right and passPipe == False:
            passPipe = True
        if passPipe == True:
            if birdGroup.sprites()[0].rect.left > pipeGroup.sprites()[0].rect.right:
                score += 1
                passPipe = False
    text = font.render(str(score), True, WHITE)
    screen.blit(text, (WIDTH//2, 40))

    # - collision between the bird and the pipe
    if pygame.sprite.groupcollide(birdGroup, pipeGroup, False, False) or flappyBird.rect.top < 0:
        gameover = True
    
    if gameover == True:
        if restart.display():
            gameover = False
            resetGame()

    # - checking if bird hit the ground
    if flappyBird.rect.bottom > 768:
        gameover = True
        flying = False
    
    # - if not gameover
    if gameover == False and flying == True:
        # - making the ground scroll / move
        groundScroll -= scrollSpeed
        if abs(groundScroll) > 35:
            groundScroll = 0

        # - making the pipes
        timeNow = pygame.time.get_ticks()
        if timeNow - lastPipe > pipeFrequency:
            pipeHeight = random.randint(-100,100)
            bottomPipe = Pipe(WIDTH, int(HEIGHT//2) + pipeHeight, -1)
            topPipe = Pipe(WIDTH, int(HEIGHT//2) + pipeHeight, 1)
            pipeGroup.add(bottomPipe)
            pipeGroup.add(topPipe)
            lastPipe = timeNow
        pipeGroup.update()

    # - quit function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameover == False:
            flying = True

    pygame.display.update()

pygame.quit()