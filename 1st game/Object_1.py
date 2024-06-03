import pygame
import math
from Utils import img_load
from Ray import ray

class g_object():
	def __init__(self,pos,sprite,variant= 1,Reflect = False,color = None):
		self.variant = str(variant)
		self.pos = tuple(pos)
		self.surface = sprite
		self.color = color
		self.game = None
		self.shoot_at = False
		self.Reflect = Reflect
		self.fall_speed = 0
		self.rect = self.surface.get_rect(topleft = self.pos)
		self.pick_able = False
		self.ray_color = None
		self.sprite = None

	def Render(self,surf):
		surf.blit(self.surface,self.pos)

	def clone(self,pos):

		if self.game:
			return type(self)(pos,self.surface,self.color,self.variant,self.game)
		elif self.color :
			return type(self)(pos,self.surface,self.color,self.variant)
		elif self.sprite:
			return type(self)(pos,self.sprite,self.variant)

		return type(self)(pos,self.surface,self.variant)

	def color_swap(self,old_c,new_c,):
		img_copy = pygame.Surface((32,32))
		img_copy.fill(new_c)
		self.surface.set_colorkey(old_c)
		img_copy.blit(self.surface, (0, 0))
		self.surface = img_copy

class Ground(g_object):
	def __init__(self,pos,sprite,variant=1):
		super().__init__(pos,sprite,variant)
		self.type = "Ground"

	def update(self,surf):
		
		self.rect = self.surface.get_rect(topleft = self.pos)
		self.Render(surf)

class Glass(g_object):
	def __init__(self,pos,sprite,variant=1):
		super().__init__(pos,sprite,variant)
		self.type = "Glass"
		self.Reflect = True

	def update(self,surf):
		
		self.rect = self.surface.get_rect(topleft = self.pos)
		self.Render(surf)

class Ladder(g_object):
	def __init__(self,pos,sprite,variant=1):
		super().__init__(pos,sprite,variant)
		self.type = "Ladder"

	def update(self,surf):	
		self.rect = self.surface.get_rect(topleft = self.pos)
		self.Render(surf)

class Transparent(g_object):
	def __init__(self,pos,sprite,color,variant,game):
		super().__init__(pos,sprite,variant,False,color)
		self.type = "Transparent"
		self.conector = None
		self.sprite = sprite
		self.game = game
		self.color_swap((255,255,255),self.color)
		self.rect = self.surface.get_rect(topleft = self.pos)

	def update(self,surf):
		"""
		if self.conector.active:
			self.surface = img_load("Black_Blackground/Box.png",4)
			self.rect = self.surface.get_rect(topleft = self.pos)
		else:
			self.surface = self.sprite
			self.rect = pygame.Rect((0,0),(0,0))
"""
		self.rect = self.surface.get_rect(topleft = self.pos)
		self.color_swap((255,255,255),self.color)	
		self.Render(surf)


	def find_the_conection(self):
		for blox in self.game.blox:
			if blox.type == "Orb" and blox.variant == self.variant:
				self.conector = blox


class Box(g_object):
	def __init__(self,pos,sprite,color,variant,game):
		super().__init__(pos,sprite,variant)
		self.type = "Box"
		self.pick_able = True
		self.is_pick_up = False
		self.target = None
		self.velocity = 0
		self.game = game
	def update(self,surf):
		pass
	"""
		if not self.is_pick_up:
			self.rect = self.surface.get_rect(topleft = self.pos)
			self.Render(surf)
			self.physic()
		else:
			self.rect = pygame.Rect((0,0),(0,0))
			self.pos = self.target.pos[:]
	"""

	def find_pos(self):
		if self.target.direction:
			self.pos[0] = self.pos[0] - (32)
		else:
			self.pos[0] = self.pos[0] + (32)
			

	def physic(self):
		self.pos[1] += self.velocity
		self.collisions = {'up': False, 'down': False}
		self.rect = self.surface.get_rect(topleft = self.pos)
		x = self.game.blox + self.game.special_blox
		objs = self.rect.collideobjectsall(x,key=lambda o: o.rect)
		for obj in objs:
			if obj == self:
				continue
			if self.rect.colliderect(obj.rect): 
				if self.velocity> 0:
					self.rect.bottom = obj.rect.top
					self.collisions["down"] = True
				if self.velocity < 0:
					self.rect.top = obj.rect.bottom
					self.collisions["up"] = True

				self.pos[1] = self.rect.y

		self.velocity = min(10, self.velocity + 0.5)
		if self.collisions["up"] or self.collisions["down"]:
			self.velocity = 0

class Orb(g_object):
	def __init__(self,pos,sprite,color,variant):
		super().__init__(pos,sprite,variant,False,color)
		self.type = "Orb"
		self.active = False
		self.color_swap((255,255,255),color)
		
	def update(self,surf):
		if self.shoot_at and self.ray_color == self.color:
			self.active = True
		else:
			self.active = False
		self.Render(surf)
		self.shoot_at = False
		self.ray_color = None
		self.rect = self.surface.get_rect(topleft = self.pos)

class lazer_box(g_object):
	def __init__(self,pos,sprite,variant):
		super().__init__(pos,sprite,variant)
		self.type = "lazer_box"
		self.surface.fill(variant)

	def update(self,surf):
		self.rect = self.surface.get_rect(topleft = self.pos)

class key(g_object):
	def __init__(self,pos,sprite,variant=1):
		super().__init__(pos,sprite,variant)
		self.type = "Key"

	def update(self,surf):
		self.rect = self.surface.get_rect(topleft = self.pos)
		self.Render(surf)


class Door(g_object):
	def __init__(self,pos,sprite,variant=1):
		super().__init__(pos,pygame.Surface((0,0)),variant)
		self.type = "Door"
		self.key = None
		self.sprite = sprite
		self.surface = self.sprite[0]
		self.rect = self.surface.get_rect(topleft = self.pos)
	def update(self,surf):
		if not self.key:
			self.rect = self.surface.get_rect(topleft = self.pos)
			self.surface = self.sprite[1]
		else:
			self.surface = self.sprite[0]

		self.Render(surf)

	def find_key(self,objs):
		for i in objs:
			if i.type == "Key":
				self.key = i

class Player_spawner(g_object):
	def __init__(self,pos,sprite,variant=1):
		super().__init__(pos,sprite,variant)
		self.type = "Player_spawner"
		
	def update(self,surf):
		self.rect = self.surface.get_rect(topleft = self.pos)
		self.Render(surf)

class Decoration(g_object):
	def __init__(self,pos,sprite,variant=1):
		super().__init__(pos,sprite,variant)
		self.type = "Decoration"

	def update(self,surf):
		self.rect = self.surface.get_rect(topleft = self.pos)
		self.Render(surf)
		

