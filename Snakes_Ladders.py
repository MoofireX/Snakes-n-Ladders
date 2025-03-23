#Snakes and Ladders
#By: Suraj Saripalli
import pygame # type: ignore
import random
import time

p1_square = 1
p2_square = 1

snakes = [16,46,49,62,64,74,89,92,95,99]
snake_end = [6,25,11,19,60,53,68,88,75,80]
ladders = [2,7,8,15,21,28,36,51,71,78,87]
ladder_end = [38,14,31,26,42,84,44,67,91,98,94]

def game_init():
    square = 1
    square0 = (200, 660)
    turn = 1
    direction1 = 1
    direction2 = 1
    pygame.init()
    screen = pygame.display.set_mode((900, 800))
    pygame.display.set_caption("2 player Snakes and Ladders")
    bg = pygame.image.load("snakes+ladders.jpg")
    clock = pygame.time.Clock()
    return square, turn, screen, clock, square0, bg, direction1, direction2

square, turn, screen, clock, square0, bg, direction1, direction2 = game_init()

class dice(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def die_setup(x, y):
    roll_me = pygame.image.load("roll.png").convert_alpha()
    die1 = pygame.image.load("1.png").convert_alpha()
    die2 = pygame.image.load("2.png").convert_alpha()
    die3 = pygame.image.load("3.png").convert_alpha()
    die4 = pygame.image.load("4.png").convert_alpha()
    die5 = pygame.image.load("5.png").convert_alpha()
    die6 = pygame.image.load("6.png").convert_alpha()
    roll_it = dice("roll.png", x, y)
    dice1 = dice("1.png", x, y)
    dice2 = dice("2.png", x, y)
    dice3 = dice("3.png", x, y)
    dice4 = dice("4.png", x, y)
    dice5 = dice("5.png", x, y)
    dice6 = dice("6.png", x, y)
    dies = pygame.sprite.Group()
    dies.add(roll_it, dice1, dice2, dice3, dice4, dice5, dice6)
    return dies, roll_me, die1, die2, die3, die4, die5, die6, roll_it, dice1, dice2, dice3, dice4, dice5, dice6

dies, roll_me, die1, die2, die3, die4, die5, die6, roll_it, dice1, dice2, dice3, dice4, dice5, dice6 = die_setup(0,0)

def dice_logic(clicked):
    global roll_me, die1, die2, die3, die4, die5, die6, screen
    if clicked:
        roll = random.randint(1,6)
        if roll == 1:
            screen.blit(die1, (0,0))
        elif roll == 2:
            screen.blit(die2, (0,0))
        elif roll == 3:
            screen.blit(die3, (0,0))
        elif roll == 4:
            screen.blit(die4, (0,0))
        elif roll == 5:
            screen.blit(die5, (0,0))
        elif roll == 6:
            screen.blit(die6, (0,0))
    pygame.display.flip()
    return roll

class player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def player_setup():
    player1 = player("p1.jpg", square0[0], square0[1])
    player2 = player("p2.png", square0[0], square0[1])
    players = pygame.sprite.Group(player1, player2)
    return player1, player2, players

player1, player2, players = player_setup()

def player_logic(roll):
    global player1, player2, players, turn, direction1, direction2, p1_square, p2_square
    moves = 0
    threshold = 650
    threshold2 = 200
    if turn == 1:
        if p1_square + roll > 100:
            turn = 2
        if player1.rect.x + roll*50 > threshold and direction1 == 1:
            while player1.rect.x != threshold:
                player1.rect.x += 50
                moves += 1
            player1.rect.y -= 50
            player1.rect.x -= ((roll-1) - moves)*50
            direction1 = 2
            moves = 0
        elif player1.rect.x - roll*50 < threshold2 and direction1 == 2:
            while player1.rect.x != threshold2:
                player1.rect.x -= 50
                moves += 1
            player1.rect.y -= 50
            player1.rect.x += ((roll-1) - moves)*50
            direction1 = 1
            moves = 0

        elif player1.rect.x + roll*50 <= threshold and direction1 == 1:
            player1.rect.x += roll*50
        elif player1.rect.x + roll*50 >= threshold2 and direction1 == 2:
            player1.rect.x -= roll*50  
        p1_square += roll 
        turn = 2
    else:
        if p2_square + roll > 100:
            turn = 1
        if player2.rect.x + roll*50 > threshold and direction2 == 1:
            while player2.rect.x != threshold:
                player2.rect.x += 50
                moves += 1
            player2.rect.y -= 50
            player2.rect.x -= ((roll-1) - moves)*50
            direction2 = 2
            moves = 0
        elif player2.rect.x - roll*50 < threshold2 and direction2 == 2:
            while player2.rect.x != threshold2:
                player2.rect.x -= 50
                moves += 1
            player2.rect.y -= 50
            player2.rect.x += ((roll-1) - moves)*50
            direction2 = 1
            moves = 0

        elif player2.rect.x + roll*50 <= threshold and direction2 == 1:
            player2.rect.x += roll*50
        elif player2.rect.x + roll*50 >= threshold2 and direction2 == 2:
            player2.rect.x -= roll*50 
        p2_square += roll
        turn = 1
def prequisites():
    p1_pos = (player1.rect.x, player1.rect.y)
    p2_pos = (player2.rect.x, player2.rect.y)
    screen.blit(bg, (0,0))
    screen.blit(roll_me, (0,0))
    players.draw(screen)
    pygame.display.flip()
    return p1_pos, p2_pos

def advanced_logic():
    global roll, p1_square, p2_square
    if p1_square in snakes:
        destination = snake_end[snakes.index(p1_square)]
        while p1_square != destination:
            player_logic(destination - p1_square)
            pygame.display.flip()
    elif p1_square in ladders:
        destination = ladder_end[ladders.index(p1_square)]
        while p1_square != destination:
            player_logic(destination - p1_square)
            pygame.display.flip()
    if p2_square in snakes:
        destination = snake_end[snakes.index(p2_square)]
        while p2_square != destination:
            player_logic(destination - p2_square)
            pygame.display.flip()
    elif p2_square in ladders:
        destination = ladder_end[ladders.index(p2_square)]
        while p1_square != destination:
            player_logic(destination - p2_square)
            pygame.display.flip()

p1_pos, p2_pos = prequisites()

while True:
    clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type ==pygame.MOUSEBUTTONDOWN:
          if roll_it.rect.collidepoint(event.pos):
              clicked = True
              roll = dice_logic(clicked)
              clicked = False
              time.sleep(3)
              screen.blit(bg, (0,0))
              screen.blit(roll_me, (0,0))
              player_logic(roll)
              advanced_logic()
              if p1_square == 100:
                print("player1 won!")
                break
              elif p2_square == 100:
                print("player2 won!")
                break
              else:
                players.draw(screen)
    pygame.display.flip()    