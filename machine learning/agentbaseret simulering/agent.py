import pygame
import random

# Setup pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))#, pygame.FULLSCREEN)
myfont = pygame.font.SysFont("monospace", 12)
clock = pygame.time.Clock()

# Initialize game variables
done = False
tilstand = 1

class Agent():
    def __init__(self, x, y):
        self.energy = 100
        self.speed = 0.5 + random.random()
        self.radius = 10 + random.random()*10
        self.pos = [x,y]

    def update(self, game):
        pass


class Game():
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.agents = [Agent(random.randint(0,self.w), random.randint(0,self.h)) for i in range(50)]
        self.food = []
        self.round_timer = 500

    def generate_food(self):
        pass

    def update(self):
        for a in self.agents:
            a.update()
        self.round_timer -= 1
        if self.round_timer < 0:
            self.round_timer = 500
            self.generate_food()



def draw_game():
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,800,600))




def output_logic(tilstand):
    if tilstand == 1:
        draw_game()
    elif tilstand == 0:
        draw_menu()

def draw_menu():
    pass


#Main game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            done = True
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_s):
            pass



        #Håndtering af input fra mus
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    update()

    output_logic(tilstand)

    #pygame kommandoer til at vise grafikken og opdatere 60 gange i sekundet.
    pygame.display.flip()
    clock.tick(60)
