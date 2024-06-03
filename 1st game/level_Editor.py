import pygame
import Object_1
import math
import sys
import json
from Utils import sprite_sheet_cutter,img_load,write

class Level_Editor():
	def __init__(self):
		pass
	
	def update(self,box):
		pygame.init()
		self.running = True
		self.screen_x = 640
		self.screen_y = 640
		self.screen = pygame.display.set_mode((self.screen_x, self.screen_y),pygame.SRCALPHA)
		self.clock = pygame.time.Clock()
		self.type = ("Ground","Glass","Laser_Box","Ladder")
		self.current = None
		self.blox = {}
		self.Map = {}
		self.rect = pygame.Rect(0,0,16,16)
		self.shifting = False
		self.turbo_mode = False
		self.Plate = {
		"Box_1":Object_1.Box((0,0),img_load("Black_Blackground/Box.png",4),(255,255,255),1,self),
		"Glass_1":Object_1.Glass((0,0),img_load("Black_Blackground/Glass.png",4)),
		"Transparent_red":Object_1.Transparent((0,0),img_load("Black_Blackground/Transparent.png",4),(255,0,77),"red",self),
		"Orb_red":Object_1.Orb((0,0),img_load("Black_Blackground/orb_b.png",4),(255,0,77),"red"),
		"Transparent_green":Object_1.Transparent((0,0),img_load("Black_Blackground/Transparent.png",4),(0,228,54),"green",self),
		"Orb_green":Object_1.Orb((0,0),img_load("Black_Blackground/orb_b.png",4),(0,228,54),"green"),
		"Transparent_blue":Object_1.Transparent((0,0),img_load("Black_Blackground/Transparent.png",4),(41,173,255),"blue",self),
		"Orb_blue":Object_1.Orb((0,0),img_load("Black_Blackground/orb_b.png",4),(41,173,255),"blue"),
		"lazer_box_red":Object_1.lazer_box((0,0),pygame.Surface((32,32)),"red"),
		"lazer_box_green":Object_1.lazer_box((0,0),pygame.Surface((32,32)),"green"),
		"lazer_box_blue":Object_1.lazer_box((0,0),pygame.Surface((32,32)),"blue"),
		"Door_1":Object_1.Door((0,0),sprite_sheet_cutter("Black_Blackground/door_b.png",32,32,4)),
		"Key_1":Object_1.key((0,0),img_load("Black_Blackground/Key_b.png",4)),
		"Player_spawner_1":Object_1.Player_spawner((0,0),sprite_sheet_cutter("Black_Blackground/character_a.png",32,32,4)[0])
		}

		for i,s in enumerate(sprite_sheet_cutter("Black_Blackground/Ground.png",32,32,4)):
			self.Plate["Ground_"+str(i)] = Object_1.Ground((0,0),s,i)
		for i,s in enumerate(sprite_sheet_cutter("Black_Blackground/Ladder.png",32,32,4)):
			self.Plate["Ladder_"+str(i)] = Object_1.Ladder((0,0),s,i)
		for i,s in enumerate(sprite_sheet_cutter("Black_Blackground/Decoration.png",32,32,4)):
			self.Plate["Decoration_"+str(i)] = Object_1.Decoration((0,0),s,i)

		while self.running:
			
			self.screen.fill((0,0,0))
			for i in self.blox.values():
				i.Render(self.screen)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

				if event.type == pygame.MOUSEBUTTONDOWN and self.current:
					cordinate = self.grid_pos(pygame.mouse.get_pos())
					if cordinate in self.blox: 
						self.blox.pop(cordinate)
						self.Map.pop(str(cordinate))
					if not self.shifting:
						cordinate = self.grid_pos(pygame.mouse.get_pos())
						x = self.Plate[self.current].clone(cordinate)

						self.blox[cordinate] = x
						self.Map[str(cordinate)] = {"type":x.type+"_"+x.variant,"pos":cordinate}

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_g:
						self.current = box.get()
					if event.key == pygame.K_s:
						with open ("map/map_2.json","w") as f:
							json.dump(self.Map,f)
					if event.key == pygame.K_l:
						with open ("map/map_2.json","r") as f:
							x = json.load(f)
							self.load_file(x)
					if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
						self.shifting = True
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
						self.shifting = False
			write(self,20,self.current,(280,0),(255,255,255))
			pygame.display.flip()
			self.clock.tick(60)
			
		pygame.mixer.quit()
		pygame.quit()
		sys.exit()

	def grid_pos(self,pos):
		x = (pos[0] // 32) *32
		y = (pos[1] // 32) *32
		return (x,y)
	def Mouse(self):
		self.rect.topleft = self.grid_pos(pygame.mouse.get_pos())
	def load_file(self,data):
		for i in data.values():
			x = self.Plate[i["type"]].clone(i["pos"])
			self.blox[x.pos] = x
			self.Map[str(x.pos)] = {"type":x.type+"_"+x.variant,"pos":x.pos}
#pla = Level_Editor()

#pla.update("hib")
