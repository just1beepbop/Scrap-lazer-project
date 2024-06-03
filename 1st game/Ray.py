import pygame
import math
import Utils

class ray_system():
	def __init__(self):
		pass

class ray():
	def __init__(self,pos,number,color,End=None):
		self.pos = pygame.math.Vector2(pos)
		self.end = pygame.math.Vector2(self.pos)
		self.Next_Ray = None
		self.targets = None
		self.target = None
		self.color = color
		self.number = number
		self.Rect = None
		self.live = False
		self.vector = pygame.Vector2(1,0)
		if End:
			self.End =  pygame.math.Vector2(End)
			self.live = True

	def Update(self,angle,rects,surf):

		self.Check(angle,rects,surf)
		if self.targets:
			self.find_target(angle)
			if self.target:
				x = self.end_point(self.target,angle)
				self.target.shoot_at = True
				self.target.ray_color = self.color
				if x and self.target.Reflect == True:
					self.Reflect(x[2])
		pygame.draw.aaline(surf,self.color,self.pos,self.end,100)
		if self.Next_Ray:
			self.Next_Ray.Update(x[1],rects,surf)
		
		

	def Reflect(self,angle):
		self.vector = pygame.Vector2(1,0).rotate(angle)
		if self.number < 100:
			self.Next_Ray = ray(self.end-self.vector,self.number+1,self.color)
	
	def Check(self,angle,rects,surf):

		self.end += pygame.math.Vector2(1000,0).rotate(-angle-90)
		if self.live:
			self.end = pygame.math.Vector2(self.End)

		self.Rect = pygame.Rect(min(self.end.x,self.pos.x),min(self.end.y,self.pos.y),abs(self.end.x-self.pos.x),abs(self.end.y-self.pos.y))
		if self.end.x-self.pos.x == 0:
			self.Rect.width = 10
		if self.end.y-self.pos.y == 0:
			self.Rect.height = 10

		#pygame.draw.rect(surf,self.color,self.Rect)

		self.targets = self.Rect.collideobjectsall(rects,key=lambda o: o.rect)

	def end_point(self,target,angle):
		dic = {}
		one = self.caculate((self.pos,self.end),(target.rect.topleft,target.rect.topright))
		if one: dic[pygame.math.Vector2(one).distance_to(self.pos)] = [one,180-angle,angle-90]
		two = self.caculate((self.pos,self.end),(target.rect.topright,target.rect.bottomright))
		if two: dic[pygame.math.Vector2(two).distance_to(self.pos)] = [two,-angle,angle+90]
		three = self.caculate((self.pos,self.end),(target.rect.bottomleft,target.rect.bottomright))
		if three: dic[pygame.math.Vector2(three).distance_to(self.pos)] = [three,180-angle,angle-90]
		four = self.caculate((self.pos,self.end),(target.rect.bottomleft,target.rect.topleft))
		if four: dic[pygame.math.Vector2(four).distance_to(self.pos)] = [four,-angle,angle+90]
		if dic.keys():
			lis = [i for i in dic.keys() if i is not None]
			minv = min(lis)
			self.end = dic[minv][0]
			return dic[minv]

			

	def find_target(self,angle):
		for i in self.targets:
			if not self.target and self.end_point(i,angle):
				self.target = i
				continue
			elif self.target:
				if self.pos.distance_to(i.rect.center) < self.pos.distance_to(self.target.rect.center):
					if self.end_point(i,angle):
						self.target = i

	def caculate(self,first,second):
		den = (first[0][0] - first[1][0])*(second[0][1]-second[1][1])-(first[0][1]-first[1][1])*(second[0][0]-second[1][0])
		if den == 0:
			return
		t = ((first[0][0]-second[0][0])*(second[0][1]-second[1][1])-(first[0][1]-second[0][1])*(second[0][0]-second[1][0]))/den
		u = -((first[0][0]-first[1][0])*(first[0][1]-second[0][1])-(first[0][1]-first[1][1])*(first[0][0]-second[0][0]))/den
		if 0 <= t <= 1 and 0 <= u <= 1:
			return (first[0][0]+t*(first[1][0]-first[0][0]),first[0][1]+t*(first[1][1]-first[0][1]))
		else:
			return None
	def Render(self,surf):
		pygame.draw.aaline(surf,self.color,self.pos,self.end,100)
