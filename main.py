import pygame
WIDTH, HEIGHT = 500,500
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()
running = True

class PLAYER:
    global player_move_speed
    def __init__(self):
        self.x = 175
        self.y = 450
        self.size = (150,10)
    def draw_player(self):
        pygame.draw.rect(screen, (255,255,255), (self.x, self.y, self.size[0], self.size[1]))
    def move_left(self):
        if self.x >= 10:
            self.x -= player_move_speed
    def move_right(self):
        if self.x <= 490 - self.size[0]:
            self.x += player_move_speed

class BALL():
    def __init__(self):
        self.x = 250
        self.y = 460
        self.velocityX = 1
        self.velocityY = -3
        self.radius = 10
    def draw_ball(self):
        pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.radius)
    def move_ball(self):
        global running
        self.x += self.velocityX
        self.y += self.velocityY
        # wall colissions
        if self.x <= 0 + self.radius:
            self.velocityX *= -1
        if self.y <= 0 - self.radius:
            running = False
        if self.x >= 500 - self.radius:
            self.velocityX *= -1
        if self.y >= 500 - self.radius:
            self.velocityY *= -1

bricks = []

def draw_bricks():
    for i, brick in enumerate(bricks):
        pygame.draw.rect(screen, (255,255,255), (brick[0], brick[1], brick[2], brick[3], ))

def add_bricks_to_list():
    global bricks
    sizeX = 112
    sizeY = 40
    xPosses = [1,1,1,1]
    yPosses = [1,1,1,1,1,1]
    for i, xpos in enumerate(xPosses):
        xpos = 10 +(i*(sizeX + 10))
        for i, ypos in enumerate(yPosses):
            ypos = 10 + (i*(sizeY + 10))
            bricks.append((xpos, ypos, sizeX, sizeY))

noclip_timer = 0
def collide_player(x, y, xSize, ySize):
    center_top = x + (xSize / 2)
    global noclip_timer
    if ball.x >= x - ball.radius and ball.x <= x + xSize + ball.radius and ball.y >= y - ball.radius and ball.y <= y + ySize + ball.radius:
        ball.velocityY *= -1
        relative_to_center = (ball.x - center_top) / 20
        ball.velocityX = relative_to_center
        noclip_timer += 1
        if noclip_timer >= 5: # 5 is the amount of frames it takes to noclip back
            ball.y = 440
            ball.velocityY = -2
    else:
        noclip_timer = 0


def collide_brick(x, y, xSize, ySize):
    global noclip_timer
    if ball.x >= x - ball.radius and ball.x <= x + xSize + ball.radius and ball.y >= y - ball.radius and ball.y <= y + ySize + ball.radius:
        ball.velocityY *= -1
        noclip_timer += 1
        return True

    
player = PLAYER()
player_move_speed = 10

ball = BALL()

add_bricks_to_list()

while running:
    screen.fill((0,10,0))

    player.draw_player()
    draw_bricks()
    ball.draw_ball()
    ball.move_ball()

    collide_player(player.x, player.y, player.size[0], player.size[1])
    
    for i, brick in enumerate(bricks):
        if collide_brick(brick[0], brick[1], brick[2], brick[3]):
            print(i)
            bricks.pop(i)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    elif keys[pygame.K_RIGHT]:
        player.move_right()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)
pygame.quit()