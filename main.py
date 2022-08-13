#!/usr/bin/python3

import pygame
import random
import sounds

SHOW_DEBUGS = False

screensize: "tuple[int, int]" = (500, 500)
screen: pygame.Surface = pygame.display.set_mode(screensize, pygame.RESIZABLE)

pygame.font.init()
font = pygame.font.SysFont("monospace", 20)

def MENU(headertext, items):
	global screen
	global screensize

	menufont = pygame.font.SysFont("monospace", 35)

	c = pygame.time.Clock()
	running = True
	while running:
		clicked = False
		mousepos = pygame.mouse.get_pos()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return -1
			elif event.type == pygame.VIDEORESIZE:
				screensize = event.size
				screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				clicked = True
		screen.fill((255, 255, 255))
		# HEADER
		header = menufont.render(headertext, 1, (0, 0, 0))
		screen.blit(header, ((screensize[0] // 2) - (header.get_width() // 2), 10))
		pygame.draw.line(screen, (0, 0, 0), (0, header.get_height() + 20), (screensize[0], header.get_height() + 20), 5)
		last_height = header.get_height() * 1.5
		# BUTTONS
		btnindex = 0
		for itemtext in items:
			btn_text = menufont.render(itemtext, 1, (0, 0, 0)) # Render the text.
			buttonPadding = 10 # Amount of padding around the text.
			buttonY = last_height + buttonPadding + 40 # Top of button: bottom of last item + padding + extra padding.
			buttonRect = pygame.Rect(buttonPadding, buttonY, btn_text.get_height(), btn_text.get_height()) # Dimensions of the button.
			pygame.draw.circle(screen, (0, 0, 0), (buttonRect.centerx, buttonRect.centery), buttonRect.width * 0.5) # === Draw the button. ===
			screen.blit(btn_text, (buttonRect.right + buttonPadding, buttonY)) # Draw the text.
			textRect = pygame.Rect(0, buttonY, screensize[0], btn_text.get_height()) # Dimensions of the text.
			if textRect.collidepoint(mousepos): # If the mouse is over the text...
				pygame.draw.circle(screen, (0, 0, 0), (buttonRect.centerx, buttonRect.centery), buttonRect.width * 0.7) # Draw the hovered button.
				if clicked: # If the text is clicked...
					return btnindex # Return the index of the clicked button.
			last_height = buttonY + btn_text.get_height() + buttonPadding
			btnindex += 1
		# Flip
		pygame.display.flip()
		c.tick(60)

def MAIN():
	sounds.menu_start()
	running = True
	while running:
		selected_option = MENU("i hate trees", ["play", "shop", "settings", "save/load"])
		if selected_option == -1:
			running = False
		elif selected_option == 0:
			if background_music: sounds.gameplay_start()
			running = GAMEPLAY()
			if background_music: sounds.menu_start()
		elif selected_option == 1:
			running = SHOP()
		elif selected_option == 2:
			running = SETTINGS()
		elif selected_option == 3:
			running = SAVELOAD()
	sounds.stop_background()

upgrade_prices = {
	"heat_capacity": 100,
	"chainsaw_power": 800,
	"cooling_speed": 550,
	"chainsaw_range": 850
}
def SHOP():
	global amount_wood
	global max_chainsaw_heat
	global chainsaw_strength
	global chainsaw_cooling
	global chainsaw_range
	running = True
	while running:
		selected_option = MENU("shop", ["exit",
			f"upgrade heat capacity ({upgrade_prices['heat_capacity']}/{amount_wood} wood)",
			f"upgrade chainsaw power ({upgrade_prices['chainsaw_power']}/{amount_wood} wood)",
			f"upgrade cooling speed ({upgrade_prices['cooling_speed']}/{amount_wood} wood)",
			f"upgrade chainsaw range ({upgrade_prices['chainsaw_range']}/{amount_wood} wood)"])
		if selected_option == -1:
			return False
		elif selected_option == 0:
			return True
		elif selected_option == 1:
			if amount_wood >= upgrade_prices["heat_capacity"]:
				amount_wood -= upgrade_prices["heat_capacity"]
				max_chainsaw_heat += 10
				upgrade_prices["heat_capacity"] = round(upgrade_prices["heat_capacity"] * 1.1)
		elif selected_option == 2:
			if amount_wood >= upgrade_prices["chainsaw_power"]:
				amount_wood -= upgrade_prices["chainsaw_power"]
				chainsaw_strength += 1
				upgrade_prices["chainsaw_power"] = round(upgrade_prices["chainsaw_power"] * 1.1)
		elif selected_option == 3:
			if amount_wood >= upgrade_prices["cooling_speed"]:
				amount_wood -= upgrade_prices["cooling_speed"]
				chainsaw_cooling += 1
				upgrade_prices["cooling_speed"] = round(upgrade_prices["cooling_speed"] * 1.1)
		elif selected_option == 4:
			if amount_wood >= upgrade_prices["chainsaw_range"]:
				amount_wood -= upgrade_prices["chainsaw_range"]
				chainsaw_range += 10
				upgrade_prices["chainsaw_range"] = round(upgrade_prices["chainsaw_range"] * 1.1)

def SETTINGS():
	global SHOW_DEBUGS
	global background_music
	running = True
	while running:
		selected_option = MENU("settings", ["exit", f"show colored rectangles {'ON' if SHOW_DEBUGS else 'OFF'}", f"background music {'ON' if background_music else 'OFF'}", "update the game"])
		if selected_option == -1:
			return False
		elif selected_option == 0:
			return True
		elif selected_option == 1:
			SHOW_DEBUGS = not SHOW_DEBUGS
		elif selected_option == 2:
			background_music = not background_music
			if background_music:
				sounds.menu_start()
			else:
				sounds.stop_background()
		elif selected_option == 3:
			from git import Repo
			repo = Repo('.')
			repo.git.fetch()
			updates = repo.git.log('--no-decorate', '--pretty=Update to: %s%n\t%b', '..origin/main')[:-2]
			updates = [x.split("\n\t\n") for x in updates.split("\n\n")]
			# and combine into one list
			updates = [x for y in updates for x in y]
			# Now we have a list of updates; we can display them in a menu
			opt = MENU("updates", ["cancel", *[(u.replace('\n\t', ' -- ') + " (latest)" if i == 0 else u.replace('\n\t', ' -- ')) for i, u in enumerate(updates)]])
			if opt == -1:
				return False
			elif opt > 0:
				updatessha = repo.git.log('--no-decorate', '--pretty=%H', '..origin/main').split("\n")[opt - 1]
				print(repo.git.show(updatessha))
				repo.git.reset('--hard', updatessha)

def SAVELOAD():
	global amount_wood
	global max_chainsaw_heat
	global chainsaw_strength
	global chainsaw_cooling
	global chainsaw_range
	global world
	global playerpos
	running = True
	while running:
		selected_option = MENU("save/load", ["exit", "save", "load"])
		if selected_option == -1:
			return False
		elif selected_option == 0:
			return True
		elif selected_option == 1:
			import json
			obj = {
				"amount_wood": amount_wood,
				"max_chainsaw_heat": max_chainsaw_heat,
				"chainsaw_strength": chainsaw_strength,
				"chainsaw_cooling": chainsaw_cooling,
				"chainsaw_range": chainsaw_range,
				"playerpos": playerpos,
				"world": [
					[{"maxTreeStrength": t["maxTreeStrength"], "treeStrength": t["treeStrength"]} for t in h.trees] for h in world
				]
			}
			f = open("save.json", "w")
			f.write(json.dumps(obj))
			f.close()
		elif selected_option == 2:
			import json
			f = open("save.json", "r")
			obj = json.loads(f.read())
			f.close()
			amount_wood = obj["amount_wood"]
			max_chainsaw_heat = obj["max_chainsaw_heat"]
			chainsaw_strength = obj["chainsaw_strength"]
			chainsaw_cooling = obj["chainsaw_cooling"]
			chainsaw_range = obj["chainsaw_range"]
			playerpos = obj["playerpos"]
			world = []
			for i, h in enumerate(obj["world"]):
				world.append(House(i * 250))
				world[i].trees = []
				for j, t in enumerate(h):
					world[i].trees.append(drawTree(j * 100))
					world[i].trees[j]["maxTreeStrength"] = t["maxTreeStrength"]
					world[i].trees[j]["treeStrength"] = t["treeStrength"]
					if world[i].trees[j]["treeStrength"] <= 0:
						stump = drawTreeStump(world[i].trees[j]["treeWidth"])
						world[i].trees[j]["hitbox"] = stump["hitbox"]
						world[i].trees[j]["img"] = stump["img"]

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

def drawTree(x) -> pygame.Surface:
	tree: pygame.Surface = pygame.Surface((200, 200), pygame.SRCALPHA)
	tree.fill((255, 255, 255, 0))
	treeX = 50
	treeMod = 1 + ((x * x) / 10000000)
	treeWidth = random.randint(round(30 * treeMod), round(65 * treeMod))
	treeHeight = random.randint(round(50 * treeMod), round(100 * treeMod)) + (treeWidth / 2)
	# Base
	pygame.draw.rect(tree, (100, 50, 0), pygame.Rect(treeX, 200 - treeHeight, treeWidth, treeHeight))
	pygame.draw.rect(tree, (50, 0, 10), pygame.Rect(treeX, 200 - treeHeight, treeWidth, treeHeight), 10)
	# Leaves
	pygame.draw.circle(tree, (0, 150, 0), (treeX + (treeWidth / 2), 200 - treeHeight), 50)
	return {"img": tree, "hitbox": pygame.Rect(treeX, 200 - treeHeight, treeWidth, treeHeight + playersize), "maxTreeStrength": (treeWidth * treeHeight) // 100, "treeStrength": (treeWidth * treeHeight) // 100, "treeWidth": treeWidth}

def drawTreeStump(oldTreeWidth) -> pygame.Surface:
	tree: pygame.Surface = pygame.Surface((200, 200), pygame.SRCALPHA)
	tree.fill((255, 255, 255, 0))
	treeX = 50 + random.randint(-5, 5)
	treeWidth = oldTreeWidth + random.randint(-5, 5)
	treeHeight = random.randint(5, 30) + (treeWidth / 2)
	# Stump
	pygame.draw.rect(tree, (100, 50, 0), pygame.Rect(treeX, 200 - treeHeight, treeWidth, treeHeight))
	pygame.draw.rect(tree, (50, 0, 10), pygame.Rect(treeX, 200 - treeHeight, treeWidth, treeHeight), 10)
	return {"img": tree, "hitbox": pygame.Rect(treeX, 200 - treeHeight, treeWidth, treeHeight + playersize)}

class House:
	def __init__(self, x):
		self.house = drawHouse()
		self.trees = [drawTree(x) for i in range(random.choices([1, 2, 3], weights=[4, 4, 1], k=1)[0])]
		self.treeoffset = random.randint(140, 200)
		self.width = self.draw().get_width()
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
			# Strength bar
			if tree["treeStrength"] > 0 and tree["treeStrength"] < tree["maxTreeStrength"]:
				barWidth = 60
				barHeight = 10
				pygame.draw.rect(combined, (255, 0, 0), pygame.Rect(cum_x - (barWidth / 2), 200, barWidth, barHeight))
				pygame.draw.rect(combined, (0, 255, 0), pygame.Rect(cum_x - (barWidth / 2), 200, barWidth * (tree["treeStrength"] / tree["maxTreeStrength"]), barHeight))
		return combined

max_chainsaw_heat: int = 100
playersize: int = 10
background_music: bool = True

world: "list[House]" = []
playerpos: "list[int, int]" = [0, 150] # CENTER position of player
playerv: "list[int, int]" = [0, 0] # Velocity of player
amount_wood: int = 0
chainsaw_heat: int = 0
chainsaw_strength: int = 1
chainsaw_cooling: int = 0.4
chainsaw_range: int = 50

def GAMEPLAY():
	global screen
	global screensize
	global world
	global playerpos
	global playerv
	global amount_wood
	global chainsaw_heat

	particles = []
	chainsaw0 = pygame.image.load("assets/chainsaw_0.png")
	chainsaw1 = pygame.image.load("assets/chainsaw_1.png")

	c = pygame.time.Clock()
	running = True
	while running:
		keys = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			elif event.type == pygame.VIDEORESIZE:
				screensize = event.size
				screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return True
				elif event.key == pygame.K_SPACE:
					sounds.start_chainsaw()
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					sounds.stop_chainsaw()
		# Drawing
		screen.fill((150, 255, 255))
		#treerects = []
		scroll = (screensize[0] / 2) - playerpos[0]
		cum_x = scroll + 0
		for h in world:
			# Draw
			if cum_x >= -h.width and cum_x <= screensize[0]:
				s = h.draw()
				screen.blit(s, (cum_x, screensize[1] - s.get_height()))
				# Check for collisions
				tree_x = cum_x + h.treeoffset
				for t in h.trees:
					hit = t["hitbox"]
					hit = pygame.Rect(hit.x + tree_x + (-scroll), hit.y + (screensize[1] - t["img"].get_height()), hit.width, hit.height)
					hit.normalize()
					if SHOW_DEBUGS: pygame.draw.rect(screen, (255, 0, 0), hit.move(scroll, 0), 1) # Tree hitboxes
					# Collision
					if 		hit.collidepoint((playerpos[0] - (playersize / 2), screensize[1] + (-playerpos[1]) + (playersize / 2))) \
						or 	hit.collidepoint((playerpos[0] + (playersize / 2), screensize[1] + (-playerpos[1]) + (playersize / 2))):
						# Detect side of collision
						if playerpos[1] + (playersize * 1) > screensize[1] - hit.top:
							# Top
							playerpos[1] = (screensize[1] - hit.top) + (playersize / 2)
							playerv[1] = 0
							# Jump if necessary
							if keys[pygame.K_UP] or keys[pygame.K_w]:
								playerv[1] += 5
						elif playerpos[0] < hit.centerx:
							# Left
							playerpos[0] = hit.left - (playersize / 2)
							playerv[0] = 0
						else:
							# Right
							playerpos[0] = hit.right + (playersize / 2)
							playerv[0] = 0
					# Chainsaw
					chainsaw = pygame.Rect(playerpos[0] - (chainsaw_range / 2), (screensize[1] - playerpos[1]) - (chainsaw_range / 2), chainsaw_range, chainsaw_range)
					if chainsaw_heat < max_chainsaw_heat:
						if keys[pygame.K_SPACE]:
							if SHOW_DEBUGS: pygame.draw.rect(screen, (0, 0, 255), chainsaw.move(scroll, 0), 1) # Active chainsaw hitbox
							chstatus = random.choice([True, False])
							screen.blit(chainsaw0 if chstatus else chainsaw1, (playerpos[0] - (chainsaw_range / 2) + scroll, (screensize[1] - playerpos[1]) - (chainsaw_range / 2)))
							if t["treeStrength"] > 0 and hit.colliderect(chainsaw):
								t["treeStrength"] -= chainsaw_strength
								if t["treeStrength"] <= 0:
									# Cut down the tree!
									# Convert to stump
									stump = drawTreeStump(t["treeWidth"])
									t["hitbox"] = stump["hitbox"]
									t["img"] = stump["img"]
									# Get wood
									amount_wood = round(amount_wood + t["maxTreeStrength"])
									# Add lots of wood particles
									for i in range(30):
										if random.random() < 1:
											woodsize = random.randint(1, 20)
											wood = pygame.Surface((woodsize, woodsize))
											wood.fill(random.choice([
												(30, 15, 5),
												(100, 50, 0),
												(50, 0, 10)
											]))
											particles.append({
												"pos": [
													random.randint(hit.left, hit.right),
													random.randint(hit.top, hit.bottom) + (-(screensize[1] - t["img"].get_height())) + (-hit.height)
												],
												"v": [random.randint(-11, 11) / 10, random.randint(7, 22) / 10],
												"time": random.randint(35, 120),
												"img": wood,
												"gravity": 0.1
											})
								# Add wood particle
								if random.random() < 0.25:
									woodsize = random.randint(1, 20)
									wood = pygame.Surface((woodsize, woodsize))
									wood.fill(random.choice([
										(30, 15, 5),
										(100, 50, 0),
										(50, 0, 10)
									]))
									particles.append({
										"pos": [
											random.randint(hit.left, hit.right),
											random.randint(hit.top, hit.bottom) + (-(screensize[1] - t["img"].get_height())) + (-hit.height)
										],
										"v": [random.randint(-7, 7) / 10, random.randint(7, 14) / 10],
										"time": random.randint(35, 120),
										"img": wood,
										"gravity": 0.1
									})
					else:
						if SHOW_DEBUGS: pygame.draw.rect(screen, (255, 150, 0), chainsaw.move(scroll, 0), 1) # Overheated chainsaw hitbox
						# Add smoke particle
						if random.random() < 0.08:
							woodsize = random.randint(25, 50)
							wood = pygame.Surface((woodsize, woodsize), pygame.SRCALPHA)
							wood.fill((0, 0, 0, 0))
							pygame.draw.circle(wood, (0, 0, 0, 100), (woodsize / 2, woodsize / 2), woodsize / 2)
							particles.append({
								"pos": [
									playerpos[0] + (woodsize / -2),
									playerpos[1] - (woodsize / -2)
								],
								"v": [random.randint(-7, 7) / 10, random.randint(7, 14) / 10],
								"time": random.randint(10, 70),
								"img": wood,
								"gravity": 0
							})
					tree_x += 80
			cum_x += h.width
		# Adding new houses
		if cum_x < screensize[0]:
			world.append(House(cum_x))
		# Draw the player
		playerrect = pygame.Rect((screensize[0] / 2) - (playersize / 2), (screensize[1] - playerpos[1]) - (playersize / 2), playersize, playersize)
		pygame.draw.rect(screen, (0, 0, 0), playerrect)
		# Player movement
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			playerv[0] -= 2
		elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			playerv[0] += 2
		# Tick the player
		playerpos[0] += playerv[0]
		playerpos[1] += playerv[1]
		if playerpos[1] < playersize / 2:
			playerpos[1] = playersize / 2
			playerv[1] = 0
			if keys[pygame.K_UP] or keys[pygame.K_w]:
				playerv[1] += 5
		else:
			playerv[1] -= 0.1
		playerv[0] *= 0.7
		if playerpos[0] < -screensize[0]:
			playerpos[0] = -screensize[0]
			playerv[0] = 250
		# Chainsaw heat
		if keys[pygame.K_SPACE]:
			chainsaw_heat += 1
		else:
			chainsaw_heat -= chainsaw_cooling
		if chainsaw_heat <= 0:
			chainsaw_heat = 0
		else:
			bar_width = 50
			bar_height = 10
			shift = [screensize[0] / 2, screensize[1] - playerpos[1]]
			shift[0] -= bar_width / 2
			shift[1] -= playersize * 3.5
			pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, 0, bar_width, bar_height).move(*shift))
			pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 0, ((max_chainsaw_heat - chainsaw_heat) / max_chainsaw_heat) * bar_width, bar_height).move(*shift))
		# Draw the particles
		for p in particles:
			p["pos"][0] += p["v"][0]
			p["pos"][1] += p["v"][1]
			p["v"][1] -= p["gravity"]
			p["time"] -= 1
			screen.blit(p["img"], (p["pos"][0] + scroll, screensize[1] - p["pos"][1]))
			if p["time"] <= 0:
				particles.remove(p)
		# Draw the text
		text = font.render(f"Wood: {amount_wood}", True, (0, 0, 0))
		screen.blit(text, (0, 0))
		# Flip
		pygame.display.flip()
		c.tick(60)

MAIN()