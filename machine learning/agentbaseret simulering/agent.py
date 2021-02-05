import pygame
import random
import math
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
        self.speed = 0.2 + random.random()*2
        self.radius = 20 + random.random()*30
        self.pos = [x,y]
        self.dir = [random.random() -0.5, random.random()-0.5]
        l = math.sqrt(self.dir[0]**2+self.dir[1]**2)
        self.dir[0] /= l
        self.dir[1] /= l

    def update(self, game):
        food = game.get_food_in_range(self.pos, self.radius)
        if len(food) > 0:
            f = food[0]
            direction = [f[0]-self.pos[0], f[1]-self.pos[1]]
            l = math.sqrt(direction[0]**2+direction[1]**2)
            direction[0] /= l
            direction[1] /= l
            step = min(self.speed,l)
            self.pos[0] += direction[0]*step
            self.pos[1] += direction[1]*step
            if math.sqrt((f[0]-self.pos[0])**2 + (f[1]-self.pos[1])**2) < 0.1:
                self.energy += f[2]
                game.eat_food(f, self)
        else:
            self.pos[0] += self.dir[0]*self.speed
            if self.pos[0] < 0 or self.pos[0] > game.w:
                self.dir[0] *= -1
                self.pos[0] += self.dir[0]*self.speed
            self.pos[1] += self.dir[1]*self.speed
            if self.pos[1] < 0 or self.pos[1] > game.h:
                self.dir[1] *= -1
                self.pos[1] += self.dir[1]*self.speed
        self.energy -= 0.1 * self.speed



class Game():
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.agents = [Agent(random.randint(0,self.w), random.randint(0,self.h)) for i in range(50)]
        self.food = []
        self.round_timer = 50

    def eat_food(self, f, a):
        for food in self.food:
            if food == f:
                self.food.remove(food)
        new = Agent(a.pos[0], a.pos[1])
        new.speed = a.speed + random.random() - 0.5
        new.radius = a.radius + random.random() - 0.5
        self.agents.append(new)

    def get_food_in_range(self, pos, radius):
        food = []
        for f in self.food:
            dist = math.sqrt((f[0]-pos[0])**2 + (f[1]-pos[1])**2)
            if dist < radius:
                food.append(f)
        return food

    def generate_food(self):
        for i in range(10):
            self.food.append((random.randint(0,self.w), random.randint(0,self.h), random.randint(10,20)))

    def update(self):
        for a in self.agents:
            a.update(self)
            if a.energy < 0:
                self.agents.remove(a)
        self.round_timer -= 1
        if self.round_timer < 0:
            self.round_timer = 500
            self.generate_food()

game = Game(800,600)

def draw_game():
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,800,600))
    pygame.draw.rect(screen, (0,0,255), pygame.Rect(0,0,game.round_timer,3))

    for a in game.agents:
        pygame.draw.ellipse(screen, (255,0,0), pygame.Rect(a.pos[0],a.pos[1],a.energy,a.energy))
    for f in game.food:
        pygame.draw.ellipse(screen, (0,255,0), pygame.Rect(f[0],f[1],2,2))




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

    game.update()

    output_logic(tilstand)

    #pygame kommandoer til at vise grafikken og opdatere 60 gange i sekundet.
    pygame.display.flip()
    clock.tick(60)
