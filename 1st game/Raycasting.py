import pygame
import sys
import Object
import json
from Player import player
from Utils import sprite_sheet_cutter,img_load

class Game():
	def __init__(self):
		pygame.mixer.init()
		pygame.init()
		self.running = True
		self.screen_x = 640		
		self.screen_y = 640
		self.rays = []
		self.screen = pygame.display.set_mode((self.screen_x, self.screen_y),pygame.SRCALPHA)
		self.clock = pygame.time.Clock()
		pygame.display.set_icon(sprite_sheet_cutter("Black_Blackground/character_a.png",32,32,4)[0])
		pygame.display.set_caption("Light:Reflection")
		self.blox = []		
		self.special_blox = []
		self.pick_able_blox = []
		#self.Player = player((0,320),self)
		self.door = None
		self.key = None
		self.end = False
		self.Plate = {
		"Box_1":Object.Box((0,0),img_load("Black_Blackground/Box.png",4),(255,255,255),1,self),
		"Glass_1":Object.Glass((0,0),img_load("Black_Blackground/Glass.png",4)),
		"Transparent_red":Object.Transparent((0,0),img_load("Black_Blackground/Transparent.png",4),(255,0,77),"red",self),
		"Orb_red":Object.Orb((0,0),img_load("Black_Blackground/orb_b.png",4),(255,0,77),"red"),
		"Transparent_green":Object.Transparent((0,0),img_load("Black_Blackground/Transparent.png",4),(0,228,54),"green",self),
		"Orb_green":Object.Orb((0,0),img_load("Black_Blackground/orb_b.png",4),(0,228,54),"green"),
		"Transparent_blue":Object.Transparent((0,0),img_load("Black_Blackground/Transparent.png",4),(41,173,255),"blue",self),
		"Orb_blue":Object.Orb((0,0),img_load("Black_Blackground/orb_b.png",4),(41,173,255),"blue"),
		"lazer_box_red":Object.Laser_box((0,0),(255,0,77)),
		"lazer_box_green":Object.Laser_box((0,0),(0,228,54)),
		"lazer_box_blue":Object.Laser_box((0,0),(41,173,255)),
		"Door_1":Object.Door((0,0),sprite_sheet_cutter("Black_Blackground/door_b.png",32,32,4)),
		"Key_1":Object.key((0,0),img_load("Black_Blackground/Key_b.png",4)),
		"Player_spawner_1":Object.Player_spawner((0,0),sprite_sheet_cutter("Black_Blackground/character_a.png",32,32,4)[0])
		}


		for i,s in enumerate(sprite_sheet_cutter("Black_Blackground/Ground.png",32,32,4)):
			self.Plate["Ground_"+str(i)] = Object.Ground((0,0),s,i)
		for i,s in enumerate(sprite_sheet_cutter("Black_Blackground/Ladder.png",32,32,4)):
			self.Plate["Ladder_"+str(i)] = Object.Ladder((0,0),s,i)
		for i,s in enumerate(sprite_sheet_cutter("Black_Blackground/Decoration.png",32,32,4)):
			self.Plate["Decoration_"+str(i)] = Object.Decoration((0,0),s,i)

		with open ("map/map_2.json","r") as f:
			x = json.load(f)
			self.load_file(x)

		for blox in self.blox:
			if blox.type == "Transparent":
				blox.find_the_conection()

		#self.blox.append(self.key)
		#self.door.find_key(self.key)


	def update(self):
		while self.running:
			self.screen.fill((0,0,0))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT or event.key == pygame.K_a:
						self.Player.movement_x[0] = True
					if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
						self.Player.movement_x[1] = True
					if event.key == pygame.K_UP or event.key == pygame.K_w:		
						if self.Player.is_climbing:
							self.Player.movement_y[0] = True
						else:
							self.Player.jump()
					if event.key == pygame.K_DOWN or event.key == pygame.K_s:
						self.Player.movement_y[1] = True

					if event.key == pygame.K_j:
						self.Player.Put_down(self.blox)
						if self.Player.is_holding and self.Player.put_down:
							self.Player.target.find_pos()
							self.Player.target.is_pick_up = False
							self.Player.target.target = None
							self.Player.is_holding = False
							self.Player.target = None
						elif not self.Player.is_holding:
							objs = self.Player.pick_up_range.collideobjects(self.pick_able_blox,key=lambda o: o.rect)
							if objs:
								self.Player.target = objs
								self.Player.target.is_pick_up = True
								self.Player.target.target = self.Player
								self.Player.is_holding = True
					if event.key == pygame.K_k and self.Player.target:
						if self.Player.target.type == "Laser_box":
							self.Player.target.active = not self.Player.target.active
						
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT or event.key == pygame.K_a:
						self.Player.movement_x[0] = False
					if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
						self.Player.movement_x[1] = False
					if event.key == pygame.K_UP or event.key == pygame.K_w:
						self.Player.movement_y[0] = False
					if event.key == pygame.K_DOWN or event.key == pygame.K_s:
						self.Player.movement_y[1] = False
			
			
			for i in self.blox:
				i.update(self.screen)


			for i in self.special_blox:
					i.update(self.blox,self.screen)
					i.Render(self.screen)

			#if self.key:
			#	if self.key.is_touch:
			#		self.key = None
			#		self.blox.pop()
			#		self.door.key = None

			#self.Player.update(self.blox+self.special_blox)
			#self.Player.Render(self.screen)
			
			pygame.display.flip()
			self.clock.tick(60)

		pygame.mixer.quit()
		pygame.quit()
		sys.exit()
	def delete_key():
		self.key = None

	def load_file(self,data):
		for i in data.values():
			x = self.Plate[i["type"]].clone(i["pos"])
			if x.pick_able:
				self.pick_able_blox.append(x)
			if x.type == "Laser_box":
				self.special_blox.append(x)
			elif x.type == "Key":
				self.key = self.Plate[i["type"]].clone(i["pos"])
			elif x.type == "Door":

				self.door = self.Plate[i["type"]].clone(i["pos"])
				self.blox.append(self.door)
			elif x.type == "Player_spawner":
				self.Player.pos = list(x.pos)[:]
			else:
				self.blox.append(x)

if __name__ == '__main__':
	game = Game()
	game.update()