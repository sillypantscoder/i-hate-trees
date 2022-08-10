import pygame
import random

screensize: "tuple[int, int]" = (500, 500)
screen: pygame.Surface = pygame.display.set_mode(screensize, pygame.RESIZABLE)

def drawHouse() -> pygame.Surface:
	house: pygame.Surface = pygame.Surface((300, 300), pygame.SRCALPHA)
	house.fill((255, 255, 255, 0))
	# Base
	pygame.draw.rect(house, (200, 200, 255), pygame.Rect(50, 100, 200, 200))
	pygame.draw.rect(house, (50, 0, 10), pygame.Rect(50, 100, 200, 200), 10)
	pygame.draw.polygon(house, (200, 200, 255), ((50, 100), (150, 0), (250, 100)))
	pygame.draw.polygon(house, (50, 0, 10), ((50, 100), (150, 0), (250, 100)), 10)
	# Door
	pygame.draw.rect(house, (100, 100, 100), pygame.Rect(85, 200, 50, 90))
	pygame.draw.circle(house, (0, 0, 0), (100, 245), 5)
	# Window
	pygame.draw.rect(house, (150, 150, 100), pygame.Rect(160, 135, 60, 60))
	pygame.draw.rect(house, (50, 0, 10), pygame.Rect(160, 135, 60, 60), 10)
	pygame.draw.line(house, (50, 0, 10), (190, 135), (190, 195), 10)
	pygame.draw.line(house, (50, 0, 10), (160, 165), (220, 165), 10)
	return house

def drawTree() -> pygame.Surface:
	tree: pygame.Surface = pygame.Surface((200, 200), pygame.SRCALPHA)
	tree.fill((255, 255, 255, 0))
	treeX = 50
	treeWidth = random.randint(30, 65)
	treeHeight = random.randint(50, 100) + (treeWidth / 2)
	# Base
	pygame.draw.rect(tree, (100, 50, 0), pygame.Rect(treeX, 200 - treeHeight, treeWidth, treeHeight))
	pygame.draw.rect(tree, (50, 0, 10), pygame.Rect(treeX, 200 - treeHeight, treeWidth, treeHeight), 10)
	# Leaves
	pygame.draw.circle(tree, (0, 150, 0), (treeX + (treeWidth / 2), 200 - treeHeight), 50)
	return {"img": tree, "hitbox": pygame.Rect(treeX, 200 - treeHeight, treeWidth, treeHeight)}

class House:
	def __init__(self):
		self.house = drawHouse()
		self.trees = [drawTree() for i in range(random.choices([1, 2, 3], weights=[4, 4, 1], k=1)[0])]
		self.treeoffset = random.randint(140, 200)
	def draw(self) -> pygame.Surface:
		house = pygame.Surface(self.house.get_size(), pygame.SRCALPHA)
		house.blit(self.house, (0, 0))
		house.set_alpha(130)
		combined = pygame.Surface((self.treeoffset + (len(self.trees) * 80) + 80, 300), pygame.SRCALPHA)
		combined.blit(house, (0, 0))
		cum_x = self.treeoffset + 0
		for tree in self.trees:
			combined.blit(tree["img"], (cum_x, 100))
			cum_x += 80
		return combined

world: "list[House]" = []
playerpos: "list[int, int]" = [0, 150] # CENTER position of player
playerv: "list[int, int]" = [0, 0] # Velocity of player

c = pygame.time.Clock()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.VIDEORESIZE:
			screensize = event.size
			screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)
	# Drawing
	screen.fill((150, 255, 255))
	scroll = (screensize[0] / 2) - playerpos[0]
	cum_x = scroll + 0
	for h in world:
		s = h.draw()
		screen.blit(s, (cum_x, screensize[1] - s.get_height()))
		cum_x += s.get_width()
	# Adding new houses
	if cum_x < screensize[0]:
		world.append(House())
	# Draw the player
	playersize = 10
	pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((screensize[0] / 2) - (playersize / 2), (screensize[1] - playerpos[1]) - (playersize / 2), playersize, playersize))
	# Tick the player
	playerpos[0] += playerv[0]
	playerpos[1] += playerv[1]
	if playerpos[1] < playersize / 2:
		playerpos[1] = playersize / 2
		playerv[1] = 0
	else:
		playerv[1] -= 0.1
	playerv[0] *= 0.995
	# Flip
	pygame.display.flip()
	c.tick(60)