import pygame
import Object_1
from Utils import sprite_sheet_cutter,img_load,write
import sys

class Plate():
	def __init__(self):
		pass

	def update(self,box):
		pygame.init()
		self.running = True
		self.screen_x = 330
		self.screen_y = 330
		self.screen = pygame.display.set_mode((self.screen_x, self.screen_y),pygame.SRCALPHA)
		self.clock = pygame.time.Clock()
		self.rect = pygame.Rect(0,0,16,16)
		self.current = None
		self.Block = [Object_1.Box((0,0),img_load("Black_Blackground/Box.png",4),(255,255,255),1,self),
		Object_1.lazer_box((0,0),pygame.Surface((32,32)),"red"),Object_1.lazer_box((0,0),pygame.Surface((32,32)),"green"),Object_1.lazer_box((0,0),pygame.Surface((32,32)),"blue"),
		Object_1.Transparent((0,0),img_load("Black_Blackground/Transparent.png",4),(255,0,77),"red",self),
		Object_1.Orb((0,0),img_load("Black_Blackground/orb_b.png",4),(255,0,77),"red"),
		Object_1.Transparent((0,0),img_load("Black_Blackground/Transparent.png",4),(0,228,54),"green",self),
		Object_1.Orb((0,0),img_load("Black_Blackground/orb_b.png",4),(0,228,54),"green"),
		Object_1.Transparent((0,0),img_load("Black_Blackground/Transparent.png",4),(41,173,255),"blue",self),
		Object_1.Orb((0,0),img_load("Black_Blackground/orb_b.png",4),(41,173,255),"blue"),
		Object_1.Glass((0,0),img_load("Black_Blackground/Glass.png",4)),
		Object_1.Door((0,0),sprite_sheet_cutter("Black_Blackground/door_b.png",32,32,4)),
		Object_1.key((0,0),img_load("Black_Blackground/Key_b.png",4)),
		Object_1.Player_spawner((0,0),sprite_sheet_cutter("Black_Blackground/character_a.png",32,32,4)[0])]

		for i,s in enumerate(sprite_sheet_cutter("Black_Blackground/Ground.png",32,32,4)):
			self.Block.append(Object_1.Ground((0,0),s,i))
		for i,s in enumerate(sprite_sheet_cutter("Black_Blackground/Ladder.png",32,32,4)):
			self.Block.append(Object_1.Ladder((0,0),s,i))
		for i,s in enumerate(sprite_sheet_cutter("Black_Blackground/Decoration.png",32,32,4)):
			self.Block.append(Object_1.Decoration((0,0),s,i))

		
		x=y=i=0
		while y <330:
			x = 0
			while x <330:
				if i  == len(self.Block):
					break
				self.Block[i].pos = [x,y]
				x +=33
				i += 1
			if i  == len(self.Block):
				break
			y += 33
		for block in self.Block:
			block.update(self.screen)
		
		while self.running:
			self.screen.fill((0,0,0))
			for block in self.Block:
				block.Render(self.screen)
			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					self.running = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.Mouse()
					obj = self.rect.collideobjects(self.Block, key=lambda o:o.rect)
					if obj:
						self.current = obj
						print(self.current.type+"_"+self.current.variant)
						box.put(self.current.type+"_"+self.current.variant)
			if self.current:			
				write(self,32,self.current.type+"_"+self.current.variant,(0,280),(255,255,255))

			pygame.display.flip()
			self.clock.tick(60)
			

		pygame.mixer.quit()
		pygame.quit()
		sys.exit()
	
	def Mouse(self):
		self.rect.topleft = pygame.mouse.get_pos()

