import pygame

screensize = (500, 500)
screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)

c = pygame.time.Clock()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.VIDEORESIZE:
			screensize = event.size
			screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)
	screen.fill((255, 255, 255))
	pygame.display.flip()
	c.tick(60)