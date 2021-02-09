import pygame
import random
import math

# Setup pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))#, pygame.FULLSCREEN)
myfont = pygame.font.SysFont("monospace", 12)
clock = pygame.time.Clock()
bane = pygame.image.load('bane2.png')
# Initialize game variables
done = False
tilstand = 1


class Car():
    def __init__(self, weights):
        self.pos = [0,250]
        self.dir = 0
        self.weights = weights
        self.steer = 0

    def update(self, inputs):
        self.steer = self.evaluate(inputs)
        self.dir += self.steer
        if self.dir > 1.5:
            self.dir = 1.5
        if self.dir < -1.5:
            self.dir = -1.5
        self.pos[0] += math.cos(self.dir)
        self.pos[1] += math.sin(self.dir)


    def dot(self,l1,l2):
        a = 0
        for i in range(len(l1)):
            a += l1[i]*l2[i]
        return a

    def evaluate(self, inputs):
        #1/(1+e^{-x})
        x = self.dot(inputs,self.weights[0:len(inputs)]) + self.weights[-1]
        print(x)
        L = 0.1
        k = 1
        return (L/(1+math.exp(-k*x)))-0.05



class Game():
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.car = Car([random.random()-0.5 for i in range(6)])
        self.latest_input = []
        self.points = []
        self.population = []
        self.avg = 0

    def get_weights_by_selection(self):
        c1 = random.choice(self.population)
        c2 = random.choice(self.population)
        weights = [0 for i in range(len(c1[0]))]
        for i in range(len(c1[0])):
            if random.random() > 0.5:
                weights[i] = c1[0][i]
            else:
                weights[i] = c2[0][i]
            if random.random() > 0.01:
                weights[i] = random.random()-0.5
        return weights

    def update(self):
        inputs = []
        game.points = []
        for v in [-math.pi/3,-math.pi/6,0,math.pi/6,math.pi/3]:
            l = 1
            x = self.car.pos[0] + l * math.cos(v + self.car.dir)
            y = self.car.pos[1] + l * math.sin(v + self.car.dir)
            c = bane.get_at((int(x),int(y)))
            while c == (0,0,0,255) and l < 150:
                x = self.car.pos[0] + l * math.cos(v + self.car.dir)
                y = self.car.pos[1] + l * math.sin(v + self.car.dir)
                try:
                    c = bane.get_at((int(x),int(y)))
                except:
                    c = (0,0,0,255)
                l += 1

            game.points.append((x,y))
            inputs.append(l/100)

        game.latest_input = inputs
        self.car.update(inputs)

        if self.car.pos[0] > 550 or bane.get_at((int(self.car.pos[0]),int(self.car.pos[1]))) != (0,0,0,255):
            self.population.append((self.car.weights, self.car.pos[0]))
            if len(self.population) > 100:
                self.population.sort(key = lambda x:x[1], reverse=True)
                self.population = self.population[0:100]
                sum = 0
                for c in self.population:
                    sum += c[1]
                self.avg = sum/100


            #print("Fitness: {}".format(self.car.pos[0]))
            self.car = Car([random.random()-0.5 for i in range(6)])
            if len(game.population) > 50 and random.random() > 0.5:
                self.car.weights = game.get_weights_by_selection()
                #print("Selection!")

game = Game(500,500)

def draw_game():
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,800,600))
    screen.blit(bane, [0, 0])


    pygame.draw.ellipse(screen, (255,255,255), pygame.Rect(game.car.pos[0]-6, game.car.pos[1]-6,12,12))


    screen.blit(myfont.render("inputs: {}".format(game.latest_input), 0, (255,255,255)), (20,20))
    screen.blit(myfont.render("output: {:0.2f}".format(game.car.steer), 0, (255,255,255)), (20,40))
    #screen.blit(myfont.render("network: {}".format(game.car.weights), 0, (255,255,255)), (20,60))
    screen.blit(myfont.render("speed: {}".format(speed), 0, (255,255,255)), (20,80))
    screen.blit(myfont.render("Average fitness: {}".format(game.avg), 0, (255,255,255)), (20,100))
    if len(game.population) > 0:
        screen.blit(myfont.render("Max fitness: {}".format(game.population[0][1]), 0, (255,255,255)), (20,120))

    for p in game.points:
        pygame.draw.ellipse(screen, (200,100,200), pygame.Rect(p[0],p[1], 5, 5))


def output_logic(tilstand):
    if tilstand == 1:
        draw_game()
    elif tilstand == 0:
        draw_menu()

def draw_menu():
    pass

speed = 1

#Main game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            done = True
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            bane = pygame.image.load('bane3.png')
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_w):
            bane = pygame.image.load('bane2.png')
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_a):
            speed -= 1
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_s):
            speed += 1

        #Håndtering af input fra mus
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
    for i in range(speed):
        game.update()

    output_logic(tilstand)

    #pygame kommandoer til at vise grafikken og opdatere 60 gange i sekundet.
    pygame.display.flip()
    clock.tick(60)
