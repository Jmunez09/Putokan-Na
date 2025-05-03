import pygame
import sys
import random
from math import *

# Create A Desktop Window
pygame.init()
width = 1250
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Putokan-Na")
clock = pygame.time.Clock()

# Draw Score
margin = 100
lowerBound = 100
score = 0 
high_score = 0  # New high score variable
game_time = 61  # game time in seconds
time_left = game_time * 1000  # convert to milliseconds

# Colors
white = (230, 230, 230)
black = (0, 0, 0)
lightBlue = (4, 27, 96)
red = (231, 76, 60)
lightGreen = (25, 111, 61)
darkGray = (40, 55, 71)
darkBlue = (64, 178, 239)
green = (35, 155, 86)
yellow = (244, 208, 63)
blue = (46, 134, 193)
purple = (155, 89, 182)
orange = (243, 156, 18)

# Set font project
font = pygame.font.SysFont("Elephant", 35)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def main_menu():
    while True:
        display.fill(purple)
        draw_text("PUTOKAN - NA", font, black, display, width//2, height//4)
        draw_text("Start Game", font, black, display, width//5, height//1.33 - 50)
        draw_text("How to play", font, black, display, width//2, height/1.50)
        draw_text("Quit", font, black, display, width//1.30, height//2 + 100)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return
                if event.key == pygame.K_h:
                    instructions()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def instructions():
    while True:
        display.fill(purple)
        draw_text("HOW  TO  PLAY", font, black, display, width//2, height//4)
        draw_text("Click on balloons to burst them be carefull to the hiden bomb!", font, black, display, width//2, height//2)
        draw_text("Press any key to go back", font, black, display, width//2, height//2 + 50)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

main_menu()

def game():
    global score, high_score
    start_ticks = pygame.time.get_ticks()
    running = True
    while running:
        display.fill(white)
        draw_text("Game Running...", font, black, display, width//2, height//2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(60)


# Load shoot sound effect
burst_sound = pygame.mixer.Sound('Gun.mp3')
explosion_sound = pygame.mixer.Sound('bomb.mp3')

# Function to show timer
def showTimer(time_left):
    minutes = time_left // 60000  # Calculate minutes
    seconds = (time_left % 60000) // 1000  # Calculate remaining seconds
    timer_text = font.render(f"Time Left: {minutes:02}:{seconds:02}", True, red)
    text_rect = timer_text.get_rect(center=(width // 1.30, height - lowerBound + 25))
    display.blit(timer_text, text_rect)

class Balloon:
    def __init__(self, speed):
        self.a = random.randint(30, 40)
        self.b = self.a + random.randint(0, 10)
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed = -speed
        self.proPool = [-1, -1, -1, 0, 0, 0, 0, 1, 1, 1]
        self.length = random.randint(50, 100)
        self.color = random.choice([red, green, purple, orange, yellow, blue])
        self.number = random.randint(0, 10)  # Assign a random number to the balloon

        # 20% chance to contain a hidden bomb
        self.has_bomb = random.random() < 0.5  # 20% probability


    def move(self):
        direct = random.choice(self.proPool)
        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10

        self.y += self.speed * sin(radians(self.angle))
        self.x += self.speed * cos(radians(self.angle))

        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height / 5:
                self.x -= self.speed * cos(radians(self.angle))
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 30:
            self.reset()

    def show(self):
        pygame.draw.line(display, darkBlue, (self.x + self.a / 2, self.y + self.b),
                         (self.x + self.a / 2, self.y + self.b + self.length))
        pygame.draw.ellipse(display, self.color, (self.x, self.y, self.a, self.b))
        pygame.draw.ellipse(display, self.color, (self.x + self.a / 2 - 5, self.y + self.b - 3, 10, 10))

        # Draw the number inside the balloon
        number_font = pygame.font.SysFont("Arial", 25, bold=True)
        number_text = number_font.render(str(self.number), True, black)  # Ensure text is BLACK
        text_rect = number_text.get_rect(center=(self.x + self.a / 2, self.y + self.b / 2))
        display.blit(number_text, text_rect)

    def burst(self):
        global score
        pos = pygame.mouse.get_pos()
        if isonObject(self.x, self.y, self.a, self.b, pos):
            if self.has_bomb:  # If this balloon contains a bomb
                score -= 5  # Penalty for hitting a bomb
                explosion_sound.play()
            else:
                score += self.number  # Add balloon's number to the score
                burst_sound.play()
            self.reset()

    def reset(self):
        self.__init__(random.choice([1, 2, 3, 4]))

class Bomb:
    def __init__(self, speed):
        self.a = 40
        self.b = 40
        self.x = random.randrange(margin, width - self.a - margin)
        self.y = height - lowerBound
        self.angle = 90
        self.speed = -speed
        self.proPool = [-1, 0, 1]

    def move(self):
        direct = random.choice(self.proPool)
        if direct == -1:
            self.angle += -10
        elif direct == 0:
            self.angle += 0
        else:
            self.angle += 10

        self.y += self.speed * sin(radians(self.angle))
        self.x += self.speed * cos(radians(self.angle))

        if (self.x + self.a > width) or (self.x < 0):
            if self.y > height / 5:
                self.x -= self.speed * cos(radians(self.angle))
            else:
                self.reset()
        if self.y + self.b < 0 or self.y > height + 30:
            self.reset()

    def show(self):
        pygame.draw.ellipse(display, black, (self.x, self.y, self.a, self.b))
        pygame.draw.rect(display, black, (self.x + 15, self.y - 10, 10, 10))

    def explode(self):
        global score
        pos = pygame.mouse.get_pos()
        if isonObject(self.x, self.y, self.a, self.b, pos):
            score -= 1
            explosion_sound.play()
            self.reset()

    def reset(self):
        self.__init__(random.choice([1, 2, 3, 4]))

balloons = [Balloon(random.choice([1, 2, 3, 4])) for _ in range(10)]
bombs = [Bomb(random.choice([1, 2, 3, 4])) for _ in range(3)]   

def isonObject(x, y, a, b, pos):
    return x < pos[0] < x + a and y < pos[1] < y + b

def pointer():
    pos = pygame.mouse.get_pos()
    pygame.draw.circle(display, red, pos, 15, 3)

def lowerPlatform():
    pygame.draw.rect(display, darkGray, (0, height - lowerBound, width, lowerBound))

def showScore():
    scoreText = font.render("Balloons Score Burst: " + str(score), True, white)
    highScoreText = font.render("High Score: " + str(high_score), True, white)  # Display high score
    display.blit(scoreText, (30, height - lowerBound + 50))
    display.blit(highScoreText, (500, height - lowerBound + 50))  # Position high score below score

    # Function to load high score from file
def load_high_score():
    try:
        with open("high_score.re", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Function to save high score to file
def save_high_score(score):
    with open("high_score.re", "w") as file:
        file.write(str(score))

# Load high score at the start
high_score = load_high_score()

def game():
    global score, high_score
    score = 0
    start_ticks = pygame.time.get_ticks()
    running = True
    while running:
        time_left = game_time * 1000 - (pygame.time.get_ticks() - start_ticks)
        if time_left <= 0:
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for balloon in balloons:
                    balloon.burst()
                for bomb in bombs:
                    bomb.explode()
        display.fill(white)
        for balloon in balloons:
            balloon.show()
            balloon.move()
        pointer()
        lowerPlatform()
        showScore()
        showTimer(time_left)  # Mo Display timer
        pygame.display.update()
        clock.tick(60)

    # Update high score
    if score > high_score:
        high_score = score
        save_high_score(high_score)  # Save to file

    # Game Over Message
    game_over_text = font.render("Game Over!", True, red)
    display.blit(game_over_text, (width // 2 - 100, height // 2))
    pygame.display.update()
    pygame.time.wait(2000)  # Wait for 2 seconds before quitting

game()
