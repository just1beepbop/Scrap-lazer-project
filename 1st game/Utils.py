import pygame
import os
Path = "Assets/"

def write(game,size,text,position,color):
	font = pygame.font.Font("D:/New folder/Pygame/project p/Assets/Absolute 10 Basic.ttf",size)
	text = font.render(str(text),True,color)
	game.screen.blit(text,position)

def img_load(path,size):
	img = pygame.transform.scale_by(pygame.image.load(Path + path),size)
	return img

def imgs_load(path,size):
	imgs = []
	for img_name in (os.listdir(Path + path)):
		imgs.append(img_load(path + '/' + img_name,size))
	return imgs

def sound_load(path):
	sound = pygame.mixer.Sound(Path + "Sound/"+ path)
	return sound

def sprite_sheet_cutter(path,width,height,size):
	imgs = []
	sprite_sheet = pygame.transform.scale_by(pygame.image.load(Path + path),size)
	sheet_width,sheet_height = sprite_sheet.get_size()
	for y in range(0,sheet_height,height):
		for x in range(0,sheet_width,width):
			imgs.append(sprite_sheet.subsurface((x,y,width,height)))
	return tuple(imgs)

def sprite_sheet_cutter_ad(path,size):
	imgs = []
	sprite_sheet = pygame.transform.scale_by(pygame.image.load(Path + path),size)
	mask = pygame.mask.from_surface(sprite_sheet)
	bounding_rects = mask.get_bounding_rects()
	for rect in bounding_rects:
		imgs.append(sprite_sheet.subsurface(rect))
	return tuple(imgs)

def music_play(path):
	pygame.mixer.music.load(Path + path)
	pygame.mixer.music.play(-1)
	
def draw_circle_alpha(surface, color, center, radius):
	target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
	shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
	pygame.draw.circle(shape_surf, color, (radius, radius), radius)
	surface.blit(shape_surf, target_rect)

def draw_eslip(surface, color,rect):
	shape_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
	pygame.draw.ellipse(shape_surf,color,rect)
	surface.blit(shape_surf, rect)

def palette_swap(surf, old_c, new_c):
	img_copy = pygame.Surface(surf.get_size())
	img_copy.fill(new_c)
	surf.set_colorkey(old_c)
	img_copy.blit(surf, (0, 0))
	return img_copy

			

class Animation():
	def __init__(self,imgs,fps,loop,begin,end):
		self.imgs = imgs
		self.fps = fps
		self.begin = begin
		self.end = end
		self.loop = loop
		self.current = begin
		self.is_animating = False

	def update(self):
		self.img = self.imgs[int(self.current)]
		self.current += self.fps
		if self.current >= self.end:
			if self.loop:
				self.current = self.begin
			elif self.is_animating:
				self.is_animating = False
				self.current = self.begin	

		return self.img

class Particle():
	def __init__(self):
		pass

class Particle_dust():
	pass
