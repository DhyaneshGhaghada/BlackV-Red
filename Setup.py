# By Dhyanesh Ghaghada

# Importing the necessary modules
import pygame
from pygame.locals import *
import sys
import math
import random
from pygame import mixer

# initializing pygame and sound  - here, mixer
pygame.init()
mixer.init()

# Defining width and height for window
WIDTH = 800
HEIGHT = 600

# Frames per second
FPS = 60
clock = pygame.time.Clock()

# Loading Player Imgs
player1_Img = pygame.image.load("data/player1.png")
player2_Img = pygame.image.load("data/player2.png")
player2_Img_rotation = pygame.transform.rotate(player2_Img, 180)

# Loading Bullet Imgs
bulletImg = pygame.image.load('data/bullet.png')
bulletScaleImg = pygame.transform.scale(bulletImg, (16, 16))
bulletImg_rotated_1 = pygame.transform.rotate(bulletScaleImg, -90)
bulletImg_rotated_2 = pygame.transform.rotate(bulletScaleImg, 90)

# Loading Logo Img
MyLogo_UnScaled = pygame.image.load("data/MyLogo.png")
MyLogo = pygame.transform.scale(MyLogo_UnScaled, (50, 50))

# Loading Sound
shot_sound = pygame.mixer.Sound("data/GunShotSound.mp3")
kill_sound = pygame.mixer.Sound("data/Kill_Sound.mp3")

icon_list = [player1_Img, player2_Img_rotation]
pygame.display.set_icon(random.choice(icon_list))

# Loading Font
font = pygame.font.Font("data/Silkscreen/slkscr.ttf", 20)

# Some Variables
movement_speed = 3
bullet_speed = 7
isFired_1 = False
isFired_2 = False
score1 = 0
score2 = 0

# RGB Colors
colors = {

	'white' : (255, 255, 255),
	'black' : (0, 0, 0),
	'gray' : (128, 128, 128),
	'red' : (255, 0, 0),
	'cyan' : (0, 255, 255)

}

# Displaying Caption
pygame.display.set_caption("Black-v-Red")

# Collision Detection
def isCollision(playerX, playerY, bulletX, bulletY):
    distance = math.sqrt(math.pow(playerX - bulletX, 2) + (math.pow(playerY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# For Drawing Text
def draw_font():
	player1_text = font.render("Player 1", True, colors['white'])
	player2_text = font.render("Player 2", True, colors['white'])
	score_1 = font.render("Score: " + str(score1), True, colors['black'])
	score_2 = font.render("Score: " + str(score2), True, colors['red'])

	screen.blit(player1_text, (0, 0))
	screen.blit(player2_text, (WIDTH - 120, 0))
	screen.blit(score_1, (0, HEIGHT - 30))
	screen.blit(score_2, (WIDTH / 2 + 10, HEIGHT - 30))

# Player Components/Functions/Class
class Player:
	def __init__(self, x, y, img_to_draw):
		self.x = x
		self.y = y
		self.img_to_draw = img_to_draw
		self.imgRect = self.img_to_draw.get_rect()

	def getImg_Rect(self):
		return self.imgRect

	def getCoordinates(self):
		return self.x, self.y

	def draw(self):
		# self.img_to_draw = img_to_draw
		screen.blit(self.img_to_draw, (self.x, self.y))

	def setCoordinates(self, x, y):
		self.x, self.y = x, y

	def addCoordinates(self, x, y):
		self.x += x
		self.y += y

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def setX(self, x):
		self.x = x

	def setY(self, y):
		self.y = y

# Bullet components/functions/class
class Bullet(Player):
	def __init__(self, bullet_img, x, y):
		self.bullet_img = bullet_img
		self.x = x
		self.y = y
		self.bulletRect = self.bullet_img.get_rect()

	def getBullet_Rect(self):
		return self.bulletRect

	def draw(self):
		screen.blit(self.bullet_img, (self.x, self.y))

class Button(Player):
	def __init__(self, x, y, width, height, win, colorB):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.win = win
		self.colorB = colorB
		self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

	def draw_Button(self):
		pygame.draw.rect(self.win, self.colorB, self.buttonRect)

	def collisionPoint(self, Mouse_Position):
		if self.buttonRect.collidepoint(Mouse_Position):
			return True
		else:
			False

# Text Components
class Text(Player):
	def __init__(self, text, x, y, color):
		self.text = text
		self.x = x
		self.y = y
		self.color = color
		self.Text = font.render(self.text, True, self.color)

	def draw_Text(self):
		screen.blit(self.Text, (self.x, self.y))

# Winning Functions
def who_wins(winners_text, x, y, color):
	win_font = pygame.font.Font("data/Silkscreen/slkscreb.ttf", 25)

	text = win_font.render(winners_text, True, color)
	screen.blit(text, (x, y))	

# Start Menu Function
def start_menu(width, height):
	global screen
	running = True

	screen = pygame.display.set_mode((width, height))
	start_button = Button(width/2 - 75, height/2 - 25, 150, 50, screen, colors['black'])
	start_text = Text("Start Game?", start_button.getX(), start_button.getY() - 50, colors['black'])
	game_name_text = Text("Black-V-Red", start_button.getX(), start_button.getY() + 15, colors['white'])

	while running:

		screen.fill(colors['cyan'])
		
		start_button.draw_Button()
		start_text.draw_Text()
		game_name_text.draw_Text()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				mousePos = event.pos
				if start_button.collisionPoint(mousePos):
					main(WIDTH, HEIGHT)	

		pygame.display.update()
		pygame.display.flip()			

# Main Function
def main(width, height):
	global screen
	global running
	global isFired_1
	global isFired_2
	global score1
	global score2
	global player_1
	global player_2
	global movement_speed
	global bullet_speed

	screen = pygame.display.set_mode((width, height))

	player_1 = Player(width/2 - 150, height/2, player1_Img)
	player_2 = Player(width/2 + 150, height/2, player2_Img_rotation)

	bullet_1 = Bullet(bulletImg_rotated_1, 0, 0)
	bullet_2 = Bullet(bulletImg_rotated_2, 0, 0)

	bullet_1.setCoordinates(player_1.getX() + 20, player_1.getY() + 15)
	bullet_2.setCoordinates(player_2.getX() + 20, player_2.getY() + 18)

	reset_button = Button(WIDTH/2 - 50, 0, 100, 50, screen, colors['cyan'])
	reset_button_text = Text("Reset", reset_button.getX() + 15, reset_button.getY() + 15, colors['black'])

	running = True
	while running:

		screen.fill(colors["gray"])

		screen.blit(MyLogo, (width - 50, height - 50))

		pygame.draw.line(screen, colors['black'], (width/2, height), (width/2, 0), 5)

		reset_button.draw_Button()
		reset_button_text.draw_Text()

		# Handling Inputs
		keys = pygame.key.get_pressed()

		if keys[K_LEFT] and player_2.getX() >= width/2:
			player_2.addCoordinates(-movement_speed, 0)

		if keys[K_RIGHT] and player_2.getX() <= width - 50:
			player_2.addCoordinates(movement_speed, 0)

		if keys[K_UP] and player_2.getY() >= 0:
			player_2.addCoordinates(0, -movement_speed)

		if keys[K_DOWN] and player_2.getY() <= height - 50:
			player_2.addCoordinates(0, movement_speed)

		if keys[K_a] and player_1.getX() >= 0:
			player_1.addCoordinates(-movement_speed, 0)

		if keys[K_d] and player_1.getX() <= width/2 - 50:
			player_1.addCoordinates(movement_speed, 0)

		if keys[K_w] and player_1.getY() >= 0:
			player_1.addCoordinates(0, -movement_speed)

		if keys[K_s] and player_1.getY() <= height - 50:
			player_1.addCoordinates(0, movement_speed)

		if keys[K_e]:
			if bullet_1.getX() == player_1.getX() + 20:
				isFired_1 = True
				pygame.mixer.Sound.play(shot_sound)
		
		if keys[K_SPACE]:
			if bullet_2.getX() == player_2.getX() + 20:
				isFired_2 = True
				pygame.mixer.Sound.play(shot_sound)

		if keys[K_ESCAPE]:
			running = False

		if bullet_1.getX() >= width:
			isFired_1 = False

		if bullet_2.getX() <= 0:
			isFired_2 = False

		if isFired_1:
			bullet_1.draw()
			bullet_1.addCoordinates(bullet_speed, 0)
			

		if isFired_2:
			bullet_2.draw()
			bullet_2.addCoordinates(-bullet_speed, 0)

		if isFired_1 == False:
			bullet_1.setCoordinates(player_1.getX() + 20, player_1.getY() + 15)
			

		if isFired_2 == False:
			bullet_2.setCoordinates(player_2.getX() + 20, player_2.getY() + 18)

		player_1.draw()
		player_2.draw()	

		draw_font()

		collision1 = isCollision(player_2.getX(), player_2.getY(), bullet_1.getX(), bullet_1.getY())
		collision2 = isCollision(player_1.getX(), player_1.getY(), bullet_2.getX(), bullet_2.getY())

		if collision1:
			isFired_1 = False
			score1 += 1
			pygame.mixer.Sound.play(kill_sound)

		if collision2:
			isFired_2 = False
			score2 += 1
			pygame.mixer.Sound.play(kill_sound)

		if score1 == 10:
			who_wins("Player 1 Wins!!!", width/2 - 150, height/2, colors['black'])
			movement_speed = 0
			bullet_speed = 0
			if keys[K_ESCAPE]:
				start_menu(WIDTH, HEIGHT)
				
		if score2 == 10:
			who_wins("Player 2 Wins!!!", width/2 - 150, height/2, colors['red'])
			movement_speed = 0
			bullet_speed = 0
			if keys[K_ESCAPE]:
				start_menu(WIDTH, HEIGHT)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				mousePos = event.pos
				if reset_button.collisionPoint(mousePos):
					score1 = 0
					score2 = 0
					player_1.setCoordinates(WIDTH/2 - 150, HEIGHT/2)
					player_2.setCoordinates(WIDTH/2 + 150, HEIGHT/2)
					movement_speed = 3
					bullet_speed = 7		

		pygame.display.update()
		pygame.display.flip()
		clock.tick(FPS)

start_menu(WIDTH, HEIGHT)