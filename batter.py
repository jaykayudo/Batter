"""
Created by jaykayudo
"""
import pygame, time, sys
from pygame.locals import *

pygame.init()



class BrickGame:
	def __init__(self):

		

		#window init
		self.WIDTH = 800
		self.HEIGHT  = 600
		icon = pygame.image.load('icon.png')
		self.window = pygame.display.set_mode((self.WIDTH,self.HEIGHT)) 
		pygame.display.set_caption('Batter')
		pygame.display.set_icon(icon)

		self.BLUE = (0,0,255)
		self.BLACK = (0,0,0)
		self.GREEN = (0,255,0)
		self.WHITE = (255,255,255)
		self.RED = (255,0,0)
		self.GRAY = (192,192,192)

		self.clock = pygame.time.Clock()

		#bat init
		self.bat = pygame.image.load('bat.png').convert_alpha()
		self.posy =  540
		self.posx = 400
		self.batrect = self.bat.get_rect()
		self.batrect.topleft = (self.posx,self.posy)


		#ball init
		self.ball = pygame.image.load('ball.png')
		self.ballrect = self.ball.get_rect()
		self.bx = self.batrect.center[0]
		self.by = self.batrect.center[1]- 12
		speed = -5
		self.mx,self.my = (speed,speed)
		self.ballrect.topleft = (self.bx,self.by)

		#player live
		self.lives = 3

		#brick init
		self.brick = pygame.image.load('brick.png')
		self.bricks = []
		self.bricksizex = 31
		self.bricksizey = 11
		for y in range(5):
			pos0 = (y*30) +100
			for x in range(1,20):
				pos1 = (x*35) + 70
				self.bricks.append((pos1,pos0))


		self.running = True
		self.ballplayed = False
		self.balllift = False
		movex = 0
		movey = 0
		#print(batrect)

		while self.running:
			self.window.fill((192,192,192))
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					quit()
				if event.type == MOUSEBUTTONDOWN:
					self.ballplayed = True
				if event.type == MOUSEMOTION:
					mousex,mousey = event.pos
				if event.type == KEYDOWN:
					if event.key == K_LEFT:
						movex =- 10
					if event.key == K_RIGHT:
						movex =+ 10
				if event.type == KEYUP and event.key == K_LEFT or event.type == KEYUP and event.key == K_RIGHT:
						movex = 0

			self.window.blit(self.ball,self.ballrect)
			self.window.blit(self.bat,self.batrect)	
				


			self.posx += movex
			self.batrect.topleft = (self.posx,self.posy)

			# preventing bat to move at of the wall
			if self.batrect.topleft[0] >= self.WIDTH - 60:
				self.posx = self.WIDTH - 60
				self.posy = 540
				movex = 0
				self.batrect.topleft = (self.posx,self.posy)
			if self.batrect.topleft[0] <= 0:
				self.posx = 0
				self.posy = 540
				movex = 0
				self.batrect.topleft = (self.posx,self.posy)

			#event to happen when ball is playedn
			if self.ballplayed:
				self.ballrect.topleft = (self.bx,self.by)
				self.bx += self.mx
				self.by += self.my
				self.balllift = True

			else:
				self.bx = self.batrect.center[0]
				self.by = self.batrect.center[1]- 12
				self.ballrect.topleft = (self.bx,self.by)
				try:
					pygame.draw.aaline(self.window,self.BLUE,self.ballrect.center,event.pos,1)
					if self.ballrect.topleft[0] > event.pos[0]:
						self.mx = -5
					else:
						self.mx = 5
				except:
					pass

						

			

			for b in self.bricks:
				self.window.blit(self.brick,b)

			# bounce effect
			if self.bx <=0:
				self.mx *= -1
			if self.bx >= self.WIDTH - 16:
				self.mx *= -1
			if self.by <= 0:
				self.my *= -1

			#ball and bat collision
			batx,baty,batsizex,batsizey = self.batrect
			if self.balllift:
				if self.bx >= batx and self.bx < batx + batsizex:
					if self.by >= baty - 8 and self.by <(baty - 8)  + batsizey:
				
						self.my *= -1

			#if ball falls out 
			if self.by > 600:
				self.lives -= 1
				self.bx = self.batrect.center[0]
				self.by = self.batrect.center[1]- 12
				self.ballplayed = False
				self.balllift = False

				self.ballrect.topleft = (self.bx,self.by)
				try:
					if self.ballrect.topleft[0] > event.pos[0]:
						self.mx = -5
					else:
						self.mx = 5
				except:
					pass
				self.my = -5


			#ball and bricks collision
			brickremoved = None
			for b in self.bricks:
				b0 = b[0]
				b1 = b[1]
				if self.bx >= b0 and self.bx < b0 + self.bricksizex :
					if self.by >= b1 - 8 and self.by <(b1 - 8)  + self.bricksizey or self.by >= b1 and self.by <= b1 + self.bricksizey:
						brickremoved = b
						
						break
			if brickremoved:
				self.bricks.remove(brickremoved)
				self.my *= -1

			if self.bricks == []:
				self.messagescreen('You Win',self.WHITE)
				time.sleep(2)
				self.running = False
				break
			if self.lives  == 0:
				self.messagescreen('GameOver',self.BLACK)
				time.sleep(2)
				self.running = False
				break
			self.draw_lives(self.lives)	



			




			pygame.display.update()
			self.clock.tick(30)

	def messagescreen(self,text,color):
		myfont = pygame.font.SysFont('stencil',130)
		mytext = myfont.render(text,1,color)
		mytextrect = mytext.get_rect()
		mytextrect.center = (self.WIDTH/2,self.HEIGHT/2)
		self.window.blit(mytext,mytextrect)
		pygame.display.update()


	def draw_lives(self,lives):
		liveposy = 30
		for x in range(1,lives+1):
			liveposx = (x * 20) + 20
			self.window.blit(self.ball,(liveposx,liveposy))


class GameMenu:
	def __init__(self):
		#window init
		self.WIDTH = 800
		self.HEIGHT  = 600
		icon = pygame.image.load('icon.png')
		self.window = pygame.display.set_mode((self.WIDTH,self.HEIGHT)) 
		pygame.display.set_caption('Batter')
		pygame.display.set_icon(icon)

		self.font1 = pygame.font.SysFont('castellar',120)
		self.font2 = pygame.font.SysFont('charlemagne',50)
		self.BLUE = (0,0,255)
		self.BLACK = (0,0,0)
		self.GREEN = (0,205,120)
		self.WHITE = (255,255,255)
		self.RED = (255,0,0)
		self.GRAY = (192,192,192)
		self.cursorchanger = 1

		running = True
		while running:
			self.window.fill(self.GRAY)
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					quit()
				if event.type == KEYDOWN:
					if event.key == K_DOWN:
						self.cursorchanger = 2
					if event.key == K_UP:
						self.cursorchanger = 1
					if event.key == K_RETURN:
						if self.cursorchanger == 1:
							brickgame = BrickGame()
						if self.cursorchanger == 2:
							sys.exit()


			self.maingametext()
			if self.cursorchanger == 1:
				self.startgame()
			if self.cursorchanger == 2:
				self.endgame()
			pygame.display.update()


	def maingametext(self):
		maintext = self.font1.render('BATTER',1,self.BLUE)
		mainrect = maintext.get_rect()
		mainrect.center = (self.WIDTH/2,self.HEIGHT/2 -100)
		pygame.draw.rect(self.window,self.GREEN,[0,mainrect.topleft[0] - 20,800,mainrect[3]])
		self.window.blit(maintext,mainrect)
	def startgame(self):
		starttext = self.font2.render('Start',1,self.BLUE)
		quittext = self.font2.render('Quit',1,self.BLUE)
		indicator = self.font2.render('>>',1,self.GREEN)
		self.window.blit(starttext,(60,300))
		self.window.blit(indicator,(10,300))
		self.window.blit(quittext,(30,350))
	def endgame(self):
		starttext = self.font2.render('Start',1,self.BLUE)
		quittext = self.font2.render('Quit',1,self.BLUE)
		indicator = self.font2.render('>>',1,self.GREEN)
		self.window.blit(starttext,(30,300))
		self.window.blit(indicator,(10,350))
		self.window.blit(quittext,(60,350))



game = GameMenu()


#main game logic
