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
        self.energy = 200
        self.speed = 0.2 + random.random()*2
        self.radius = 5 + random.random()*10
        self.pos = [x,y]
        self.generation = 255
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
        self.energy -= 0.01*(game.p1*(self.speed)**2 + game.p2*(self.radius/10))



class Game():
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.agents = [Agent(random.randint(0,self.w), random.randint(0,self.h)) for i in range(20)]
        self.food = []
        self.round_timer = 50
        self.food_count = 10
        self.p1 = 5
        self.p2 = 5

    def eat_food(self, f, a):
        for food in self.food:
            if food == f:
                self.food.remove(food)
        new = Agent(a.pos[0], a.pos[1])
        new.speed = a.speed + (random.random() - 0.5)*0.1
        new.radius = a.radius + (random.random()*2 - 1)
        new.generation = 0
        self.agents.append(new)


    def find_nearest_agent(self, pos):
        min_dist = 10000
        a = self.agents[0]
        for a in self.agents:
            dist = math.sqrt((a.pos[0]-pos[0])**2 + (a.pos[1]-pos[1])**2)
            if dist < min_dist:
                min_dist = min_dist
                res = a
        return a

    def get_average_radius(self):
        s = 0
        for a in self.agents:
            s += a.radius
        return s/len(self.agents)


    def get_average_speed(self):
        s = 0
        for a in self.agents:
            s += a.speed
        return s/len(self.agents)


    def get_food_in_range(self, pos, radius):
        food = []
        for f in self.food:
            dist = math.sqrt((f[0]-pos[0])**2 + (f[1]-pos[1])**2)
            if dist < radius:
                food.append(f)
        return food

    def generate_food(self):
        for i in range(self.food_count):
            self.food.append((random.randint(0,self.w), random.randint(0,self.h), random.randint(20,40)))

    def update(self):
        for a in self.agents:
            a.update(self)
            if a.energy < 0:
                self.agents.remove(a)
        self.round_timer -= 1
        if self.round_timer < 0:
            self.round_timer = 500
            self.generate_food()

game = Game(500,500)
speed = 1
current_agent = game.agents[0]

pop_size = [0 for i in range(200)]
avg_radius = [0 for i in range(200)]
avg_speed = [0 for i in range(200)]

def draw_game():
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,800,600))
    pygame.draw.rect(screen, (0,0,255), pygame.Rect(0,0,game.round_timer,3))

    pygame.draw.ellipse(screen, (20,250,75), pygame.Rect(current_agent.pos[0]-15,current_agent.pos[1]-15,30,30))
    for a in game.agents:
        pygame.draw.ellipse(screen, (20,20,20), pygame.Rect(a.pos[0]-a.radius,a.pos[1]-a.radius,a.radius*2,a.radius*2))
        pygame.draw.ellipse(screen, (255,min(int(a.energy),255),a.generation), pygame.Rect(a.pos[0]-6,a.pos[1]-6,12,12))

    for f in game.food:
        pygame.draw.ellipse(screen, (0,255,0), pygame.Rect(f[0],f[1],2,2))

    if game.round_timer % 40 == 0:
        pop_size.pop(0)
        pop_size.append(len(game.agents))

        avg_speed.pop(0)
        avg_speed.append(game.get_average_speed())

        avg_radius.pop(0)
        avg_radius.append(game.get_average_radius())
    #Graf 1
    screen.blit(myfont.render("Population: {}".format(len(game.agents)), 0, (255,255,255)), (550,5))
    pygame.draw.rect(screen, (30,30,50), pygame.Rect(550,20,200,100))
    pygame.draw.lines(screen, (255,255,255), False, [(i+550, 120 - pop_size[i]) for i in range(len(pop_size))])
    #Graf 2
    screen.blit(myfont.render("Average speed: {}".format(game.get_average_speed()), 0, (255,255,255)), (550,125))
    pygame.draw.rect(screen, (30,30,50), pygame.Rect(550,140,200,100))
    pygame.draw.lines(screen, (255,255,255), False, [(i+550, 240 - avg_speed[i]*40) for i in range(len(avg_speed))])
    #Graf 3
    screen.blit(myfont.render("Average radius: {}".format(game.get_average_radius()), 0, (255,255,255)), (550,245))
    pygame.draw.rect(screen, (30,30,50), pygame.Rect(550,260,200,100))
    pygame.draw.lines(screen, (255,255,255), False, [(i+550, 360 - avg_radius[i]*1.5) for i in range(len(avg_radius))])

    #Config
    screen.blit(myfont.render("Food (q/a): {}".format(game.food_count), 0, (255,255,255)), (550,365))
    screen.blit(myfont.render("Speed (w/s): {}".format(speed), 0, (255,255,255)), (550,385))
    screen.blit(myfont.render("Speed cost (e/d): {}".format(game.p1), 0, (255,255,255)), (550,405))
    screen.blit(myfont.render("Radius cost (r/f): {}".format(game.p2), 0, (255,255,255)), (550,425))

    #Current agent
    screen.blit(myfont.render("Speed : {}".format(current_agent.speed), 0, (255,255,255)), (250,525))
    screen.blit(myfont.render("Radius : {}".format(current_agent.radius), 0, (255,255,255)), (250,545))
    screen.blit(myfont.render("Energy : {}".format(current_agent.energy), 0, (255,255,255)), (250,565))

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
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            game.food_count += 1
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_a):
            game.food_count -= 1
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_w):
            speed += 1
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_s):
            speed -= 1
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_e):
            game.p1 += 1
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_d):
            game.p1 -= 1
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_r):
            game.p2 += 1
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_f):
            game.p2 -= 1



        #Håndtering af input fra mus
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            current_agent = game.find_nearest_agent(pos)
    for _ in range(speed):
        game.update()

    output_logic(tilstand)

    #pygame kommandoer til at vise grafikken og opdatere 60 gange i sekundet.
    pygame.display.flip()
    clock.tick(60)
