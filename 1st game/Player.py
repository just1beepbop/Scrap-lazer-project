import pygame
import math
import Utils

class player():
	def __init__(self,pos,game):
		self.pos = list(pos)
		self.type = "player"
		self.direction = False
		self.state = "Idle"
		self.sprite = Utils.sprite_sheet_cutter("Black_Blackground/character_a.png",32,32,4)
		self.Animation = {
		"Idle":Utils.Animation(self.sprite,0,True,0,0),
		"Run":Utils.Animation(self.sprite,0.2,True,1,5),
		"Climb":Utils.Animation(self.sprite,0.2,True,5,7),
		"Jump":Utils.Animation(self.sprite,0,True,7,7)
		}

		self.velocity = [3.5,0]
		self.movement_x = [False,False]
		self.movement_y = [False,False]
		self.is_climbing = False
		self.air_time = 0
		self.jump_time = 2
		self.jump_height = -7
		self.is_holding = False
		self.target = None
		self.pick_up_range = pygame.Rect((self.pos[0]-16,self.pos[1]),(64,64))
		self.put_down = False
		self.game = game

	def update(self,rects):
		self.pick_up_range = pygame.Rect((self.pos[0]-16,self.pos[1]),(64,64))
		self.state = "Idle"
		self.is_climbing = False
		self.air_time +=1
		self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
		frame_moment = ((self.velocity[0])*(self.movement_x[1]-self.movement_x[0]),self.velocity[1])
		self.pos[0] += frame_moment[0]
		self.Rect()
		objs = self.rect.collideobjectsall(rects,key=lambda o: o.rect)
		for obj in objs:
			if obj.type == "Ladder":
				self.is_climbing = True
			elif obj.type == "Key":
				obj.is_touch = True
			elif obj.type == "Door":
				self.game.end = True
			elif self.rect.colliderect(obj.rect):
				if self.movement_x[1]:
					self.rect.right = obj.rect.left
					self.collisions["right"] = True
				if self.movement_x[0]:
					self.rect.left = obj.rect.right
					self.collisions["left"] = True
				self.pos[0] = self.rect.x



		self.pos[1] += frame_moment[1]
		self.Rect()
		objs = self.rect.collideobjectsall(rects,key=lambda o: o.rect)
		for obj in objs:
			if obj.type == "Ladder":
				self.is_climbing = True
			elif obj.type == "Key":
				obj.is_touch = True
			elif obj.type == "Door":
				self.game.end = True
			elif self.rect.colliderect(obj.rect): 
				if self.velocity[1] > 0:
					self.rect.bottom = obj.rect.top
					self.collisions["down"] = True
				if self.velocity[1] < 0:
					self.rect.top = obj.rect.bottom
					self.collisions["up"] = True
					self.velocity[1] = 0
				self.pos[1] = self.rect.y


		if frame_moment[0] != 0:
			self.velocity[0] = min(5,self.velocity[0]+ 0.35)
			self.state = "Run"
			if self.movement_x[1]:
				self.direction = False
			if self.movement_x[0]:
				self.direction = True
		else:
			self.velocity[0] = 3.5

		self.velocity[1] = min(10, self.velocity[1] + 0.5)

		if self.collisions['down']:
			self.jump_time = 2
			self.velocity[1] = 0
			self.air_time = 0
		elif self.air_time > 4:
			self.state = "Jump"

		if self.is_climbing:
			self.state = "Climb"
			self.velocity[1] = 3.5*(self.movement_y[1]-self.movement_y[0])

		if 0 not in self.velocity:
			self.surface = pygame.transform.flip(self.Animation[self.state].update(),self.direction,False)

	def jump(self):
		if not self.is_holding:
			self.jump_height = -7
		else:
			self.jump_height = -6
		if self.jump_time > 0:
			self.velocity[1] = self.jump_height
			self.jump_time -=1
	def Render(self,surf):
		surf.blit(self.surface,self.pos)
		if self.target:
			self.target.Render(surf)
	def Rect(self):
		self.rect = pygame.Rect(self.pos,(32,32))
	def Put_down(self,rects):
		if self.direction:
			x = self.pos[0] - (32)
		else:
			x = self.pos[0] + (32)
		rect = pygame.Rect(x,self.pos[1],32,32)
		obj = rect.collideobjects(rects,key=lambda o: o.rect)
		if obj:
			self.put_down = False
		else:
			self.put_down = True

