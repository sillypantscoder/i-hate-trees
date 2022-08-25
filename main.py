#!/usr/bin/python3

import pygame
import random
import sounds
import json
from localization import loc, set_lang, getlanglist, get_lang

SHOW_DEBUGS = False
MOBILE_VERSION = False

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
	global SHOW_DEBUGS
	global background_music
	global sounds_active
	global MOBILE_VERSION
	# Load settings
	f = open("settings.json", "r")
	settings = json.load(f)
	f.close()
	SHOW_DEBUGS = settings["show_debugs"]
	MOBILE_VERSION = settings["mobile_version"]
	background_music = settings["background_music"]
	sounds_active = settings["sounds_active"]
	set_lang(settings["lang"])
	if background_music:
		sounds.menu_start()
	# Gameplay
	running = True
	while running:
		selected_option = MENU(loc("Home screen - Title"), [loc("Home screen - Play"), loc("Home screen - Shop"), loc("Home screen - Settings"), loc("Home screen - Save/load")])
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
	"chainsaw_range": 850,
	"chainsaw_upgrades": 2000
}
def SHOP():
	global amount_wood
	global max_chainsaw_heat
	global chainsaw_strength
	global chainsaw_cooling
	global chainsaw_range
	global chainsaw_upgrade_status
	running = True
	while running:
		selected_option = MENU(loc("Home screen - Shop"), [loc("Menus - Exit"),
			f"{loc('Shop - Heat')} ({upgrade_prices['heat_capacity']}/{amount_wood} {loc('Gameplay - Amount of wood')})",
			f"{loc('Shop - Power')} ({upgrade_prices['chainsaw_power']}/{amount_wood} {loc('Gameplay - Amount of wood')})",
			f"{loc('Shop - Cooling')} ({upgrade_prices['cooling_speed']}/{amount_wood} {loc('Gameplay - Amount of wood')})",
			f"{loc('Shop - Range')} ({upgrade_prices['chainsaw_range']}/{amount_wood} {loc('Gameplay - Amount of wood')})",
			f"{loc('Shop - Upgrade')} ({upgrade_prices['chainsaw_upgrades']}/{amount_wood} {loc('Gameplay - Amount of wood')})"])
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
		elif selected_option == 5:
			if amount_wood >= upgrade_prices["chainsaw_upgrades"]:
				amount_wood -= upgrade_prices["chainsaw_upgrades"]
				upgrade_prices["chainsaw_upgrades"] = round(upgrade_prices["chainsaw_upgrades"] * 1.1)
				chainsawname = "chainsaw"
				for i in range(chainsaw_upgrade_status):
					chainsawname = chainsaw_upgrade_mod[i][1].replace("%s", chainsawname)
				MENU(loc("Shop - Upgrade Header"), [chainsaw_upgrade_mod[chainsaw_upgrade_status][0].replace("%s", chainsawname)])
				chainsaw_upgrade_status += 1

def SETTINGS():
	global SHOW_DEBUGS
	global background_music
	global sounds_active
	global MOBILE_VERSION
	running = True
	while running:
		on = loc("Settings - On")
		off = loc("Settings - Off")
		selected_option = MENU(loc("Home screen - Settings"), [loc("Menus - Exit"), f"{loc('Settings - Hitboxes')} {on if SHOW_DEBUGS else off}", f"{loc('Settings - Music')} {on if background_music else off}", f"{loc('Settings - Sounds')} {on if sounds_active else off}", f"{loc('Settings - Mobile')} {on if MOBILE_VERSION else off}", loc("Settings - Update"), loc("Settings - Language")])
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
			sounds_active = not sounds_active
			sounds.set_active(sounds_active)
		elif selected_option == 4:
			MOBILE_VERSION = not MOBILE_VERSION
		elif selected_option == 5:
			from git import Repo
			repo = Repo('.')
			repo.git.fetch()
			updates = repo.git.log('--no-decorate', '--pretty=LOCRESETHERE %s%n\t%b', '..origin/main')[:-2].replace("LOCRESETHERE", loc("Settings - Reset Here"))
			updates = [x.split("\n\t\n") for x in updates.split("\n\n")]
			# and combine into one list
			updates = [x for y in updates for x in y]
			# Now we have a list of updates; we can display them in a menu
			opt = MENU(loc("Settings - Update Header"), [loc("Menus - Cancel"), *[(u.replace('\n\t', ' -- ') + " " + loc("Settings - Update Latest Version") if i == 0 else u.replace('\n\t', ' -- ')) for i, u in enumerate(updates)]])
			if opt == -1:
				return False
			elif opt > 0:
				updatessha = repo.git.log('--no-decorate', '--pretty=%H', '..origin/main').split("\n")[opt - 1]
				print(repo.git.show(updatessha))
				repo.git.reset('--hard', updatessha)
		elif selected_option == 6:
			langs = getlanglist()
			option = MENU(loc("Settings - Language"), langs)
			if option == -1:
				return False
			else:
				set_lang(langs[option])
		# Save settings
		f = open("settings.json", "w")
		f.write(json.dumps({"show_debugs": SHOW_DEBUGS, "background_music": background_music, "sounds_active": sounds_active, "mobile_version": MOBILE_VERSION, "lang": get_lang()}))
		f.close()

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
		selected_option = MENU(loc("Home screen - Save/load"), [loc("Menus - Exit"), loc("Files - Save"), loc("Files - Load")])
		if selected_option == -1:
			return False
		elif selected_option == 0:
			return True
		elif selected_option == 1:
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

def drawHouse(personStatus) -> pygame.Surface:
	house: pygame.Surface = pygame.Surface((300, 300), pygame.SRCALPHA)
	house.fill((255, 255, 255, 0))
	# Base
	pygame.draw.rect(house, (200, 200, 255), pygame.Rect(50, 100, 200, 200))
	pygame.draw.rect(house, (50, 0, 10), pygame.Rect(50, 100, 200, 200), 10)
	pygame.draw.polygon(house, (200, 200, 255), ((50, 100), (150, 0), (250, 100)))
	pygame.draw.polygon(house, (50, 0, 10), ((50, 100), (150, 0), (250, 100)), 10)
	# Door
	if personStatus < 61:
		pygame.draw.rect(house, (100, 100, 100), pygame.Rect(85, 200, 50, 90))
		pygame.draw.circle(house, (0, 0, 0), (100, 245), 5)
	else:
		pygame.draw.rect(house, (255, 255, 255), pygame.Rect(85, 200, 50, 90))
		pygame.draw.rect(house, (100, 100, 100), pygame.Rect(125, 200, 10, 90))
	# Window
	if personStatus < 2:
		pygame.draw.rect(house, (150, 150, 100) if personStatus == 1 else (50, 50, 50), pygame.Rect(160, 135, 60, 60))
		pygame.draw.rect(house, (50, 0, 10), pygame.Rect(160, 135, 60, 60), 10)
		pygame.draw.line(house, (50, 0, 10), (190, 135), (190, 195), 10)
		pygame.draw.line(house, (50, 0, 10), (160, 165), (220, 165), 10)
	elif personStatus <= 15:
		pygame.draw.rect(house, (50, 0, 10), pygame.Rect(160, 135, 60, 60))
	else:
		pygame.draw.rect(house, (150, 150, 100), pygame.Rect(160, 135, 60, 60))
		pygame.draw.rect(house, (50, 0, 10), pygame.Rect(160, 135, 60, 60), 10)
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
		self.trees = [drawTree(x) for i in range(random.choices([1, 2, 3], weights=[4, 4, 1], k=1)[0])]
		self.treeoffset = random.randint(140, 200)
		self.personStatus = random.choices([0, 1], weights=[1, 1], k=1)[0]
		# Person status:
		# 	0: no person
		# 	1: person is waiting
		# 	2-15: window breaking  ---\
		# 	16-25: window broken      |- person coming out animation
		# 	26-60: waiting  ----------/
		# 	61: person came out
		self.visited = False # Whether the player has gone past the door.
							 # This is to ensure that a person doesn't come
							 # out of the house if the player hasn't
							 # interacted with the house yet.
		self.width = self.draw().get_width()
	def draw(self) -> pygame.Surface:
		solidHouse = drawHouse(self.personStatus)
		house = pygame.Surface(solidHouse.get_size(), pygame.SRCALPHA)
		house.blit(solidHouse, (0, 0))
		house.set_alpha(130 if self.visited else 70)
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

def drawPerson() -> pygame.Surface:
	person: pygame.Surface = pygame.Surface((100, 200), pygame.SRCALPHA)
	person.fill((255, 255, 255, 0))
	# Head
	pygame.draw.ellipse(person, (0, 0, 0), pygame.Rect(0, 0, 100, 75), 5)
	pygame.draw.line(person, (0, 0, 0), (25, 10), (35, 40), 5) # Left eye
	pygame.draw.line(person, (0, 0, 0), (75, 10), (65, 40), 5) # Right eye
	pygame.draw.line(person, (0, 0, 0), (30, 60), (50, 50), 5) # Left mouth
	pygame.draw.line(person, (0, 0, 0), (70, 60), (50, 50), 5) # Right mouth
	# Body
	pygame.draw.line(person, (0, 0, 0), (50, 75), (50, 150), 5) # Body
	pygame.draw.line(person, (0, 0, 0), (0, 112), (100, 112), 5) # Arm
	pygame.draw.line(person, (0, 0, 0), (50, 150), (0, 200), 5) # Left leg
	pygame.draw.line(person, (0, 0, 0), (50, 150), (100, 200), 5) # Right leg
	return person

class Person:
	def __init__(self, x):
		self.x = x
		self.y = 200 - playersize
		self.v = [0, 0]
		self.img = drawPerson()
		self.health = 60 * 5
		self.canmoveleft = True
		self.canmoveright = True
	def draw(self) -> pygame.Surface:
		r = self.img.copy()
		# Health bar
		barWidth = 60
		barHeight = 10
		pygame.draw.rect(r, (255, 0, 0), pygame.Rect((r.get_width() / 2) - (barWidth / 2), 10, barWidth, barHeight))
		pygame.draw.rect(r, (0, 255, 0), pygame.Rect((r.get_width() / 2) - (barWidth / 2), 10, barWidth * (self.health / (60 * 5)), barHeight))
		return r

max_chainsaw_heat: int = 100
playersize: int = 10
background_music: bool = True
sounds_active: bool = True

world: "list[House]" = []
people: "list[Person]" = [Person(200)]
playerpos: "list[int, int]" = [0, 150] # CENTER position of player
playerv: "list[int, int]" = [0, 0] # Velocity of player
amount_wood: int = 10000000000000000000000000
chainsaw_heat: int = 0
chainsaw_strength: int = 1
chainsaw_cooling: int = 0.4
chainsaw_range: int = 50
chainsaw_upgrade_status: int = 0
chainsaw_upgrade_mod: "list[str]" = [
	[loc("Upgrade Mod - " + modname + " - Message"), loc("Upgrade Mod - " + modname + " - Mod")]
		for modname in ["Handle", "Faster", "Jet"]
]

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
	mobile_centertap: int = 0
	mobile_centertap_display: int = 0

	c = pygame.time.Clock()
	running = True
	while running:
		keys = pygame.key.get_pressed()
		mousepos = pygame.mouse.get_pos()
		mousedown = pygame.mouse.get_pressed()[0]
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			elif event.type == pygame.VIDEORESIZE:
				screensize = event.size
				screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)
				# Jinglefoodle Bingledoodle Quandavius Quanderfoodle the Third died of air traffic
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return True
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					# if mouse is in center 3rd of screen:
					if mousepos[0] > screensize[0] / 3 and mousepos[0] < screensize[0] / 3 * 2:
						if mousepos[1] > screensize[1] / 3 and mousepos[1] < screensize[1] / 3 * 2:
							mobile_centertap += 60
		# Drawing
		screen.fill((150, 255, 255))
		if MOBILE_VERSION:
			# Top
			overlay = pygame.Surface((screensize[0] // 3, screensize[1] // 3), pygame.SRCALPHA)
			overlay.fill((0, 0, 0, 100))
			screen.blit(overlay, (screensize[0] // 3, 0))
			# Left
			overlay = pygame.Surface((screensize[0] // 3, screensize[1] // 3), pygame.SRCALPHA)
			overlay.fill((0, 0, 0, 100))
			screen.blit(overlay, (0, screensize[1] // 3))
			# Right
			overlay = pygame.Surface((screensize[0] // 3, screensize[1] // 3), pygame.SRCALPHA)
			overlay.fill((0, 0, 0, 100))
			screen.blit(overlay, (screensize[0] // (3 / 2), screensize[1] // 3))
			# Bottom
			overlay = pygame.Surface((screensize[0] // 3, screensize[1] // 3), pygame.SRCALPHA)
			overlay.fill((0, 0, 0, 100))
			screen.blit(overlay, (screensize[0] // 3, screensize[1] // (3 / 2)))
		#treerects = []
		scroll = (screensize[0] / 2) - playerpos[0]
		cum_x = scroll + 0
		for h in world:
			# Draw
			if cum_x >= -h.width and cum_x <= screensize[0]:
				s = h.draw()
				screen.blit(s, (cum_x, screensize[1] - s.get_height()))
				# Person status
				doorx = cum_x + (h.width / 3) + (-scroll)
				if h.personStatus > 1 and h.personStatus <= 61:
					h.personStatus += 1
					if h.personStatus == 61:
						people.append(Person(doorx))
				elif h.personStatus == 1:
					if h.visited and random.randint(0, 60 * 30) == 1:
						h.personStatus = 2
				if keys[pygame.K_SPACE] or (MOBILE_VERSION and mousedown and mousepos[1] > screensize[1] * (2 / 3)):
					# Chainsaw making noise!
					if h.visited and h.personStatus == 1 and random.randint(0, 60) == 1:
						h.personStatus = 2
				# Check if the player has visited this house
				if playerpos[0] > doorx:
					h.visited = True
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
							if keys[pygame.K_UP] or keys[pygame.K_w] or (MOBILE_VERSION and mousedown and mousepos[1] < screensize[1] / 3):
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
						if keys[pygame.K_SPACE] or (MOBILE_VERSION and mousedown and mousepos[1] > screensize[1] * (2 / 3)):
							sounds.chainsaw_active()
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
						if keys[pygame.K_SPACE] or (MOBILE_VERSION and mousedown and mousepos[1] > screensize[1] * (2 / 3)):
							sounds.chainsaw_active()
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
					# People
					for p in people:
						hitbox = pygame.Rect(p.x, screensize[1] - p.y, p.img.get_width(), p.img.get_height())
						if SHOW_DEBUGS: pygame.draw.rect(screen, (0, 0, 255), hitbox.move(scroll, 0), 1) # Person hitbox
						if hitbox.colliderect(hit):
							# Which side of the tree did we hit?
							if hitbox.bottom - playersize < hit.top:
								# Top
								p.v[1] = 0
								p.y = (screensize[1] - hit.top) + p.img.get_height()
							elif hitbox.centerx < hit.left:
								# Hit left of tree
								p.v[0] = 0
								p.x = hit.left - p.img.get_width()
								p.canmoveright = False
							elif hitbox.centerx > hit.right:
								# Hit right of tree
								p.v[0] = 0
								p.x = hit.right
								p.canmoveleft = False
					tree_x += 80
			cum_x += h.width
		# Adding new houses
		if cum_x < screensize[0]:
			world.append(House(cum_x))
		# Draw the player
		playerrect = pygame.Rect((screensize[0] / 2) - (playersize / 2), (screensize[1] - playerpos[1]) - (playersize / 2), playersize, playersize)
		pygame.draw.rect(screen, (0, 0, 0), playerrect)
		# Player movement
		if keys[pygame.K_LEFT] or keys[pygame.K_a] \
			or (MOBILE_VERSION and mousedown and mousepos[0] < screensize[0] / 3 and mousepos[1] < screensize[1] * (2/3)) \
			or (MOBILE_VERSION and mousedown and mousepos[0] < screensize[0] / 3):
				playerv[0] -= 2
		elif keys[pygame.K_RIGHT] or keys[pygame.K_d] \
			or (MOBILE_VERSION and mousedown and mousepos[0] > screensize[0] * (2/3) and mousepos[1] < screensize[1] * (2/3)) \
			or (MOBILE_VERSION and mousedown and mousepos[0] > screensize[0] * (2/3)):
			playerv[0] += 2
		# Tick the player
		playerpos[0] += playerv[0]
		playerpos[1] += playerv[1]
		if playerpos[1] < playersize / 2:
			playerpos[1] = playersize / 2
			playerv[1] = 0
			if keys[pygame.K_UP] or keys[pygame.K_w] or (MOBILE_VERSION and mousedown and mousepos[1] < screensize[1] / 3):
				playerv[1] += 5
		else:
			playerv[1] -= 0.1
		playerv[0] *= 0.7
		if playerpos[0] < -screensize[0]:
			playerpos[0] = -screensize[0]
			playerv[0] = 250
		if MOBILE_VERSION:
			mobile_centertap -= 1
			mobile_centertap_display = (mobile_centertap_display + mobile_centertap) / 2
			if mobile_centertap < 0:
				mobile_centertap = 0
			if mobile_centertap > 250:
				return True
			if mobile_centertap > 105:
				overlay = pygame.Surface((screensize[0] // 3, screensize[1] // 3), pygame.SRCALPHA)
				overlay.fill((0, 0, 0, 0))
				pygame.draw.circle(overlay, (0, 0, 0, 100), (overlay.get_width() / 2, overlay.get_height() / 2), mobile_centertap_display - 105)
				screen.blit(overlay, (screensize[0] // 3, screensize[1] // 3))
		# Chainsaw heat
		if sounds.chainsaw_previous_status:
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
		# Tick the people
		for p in people:
			screen.blit(p.draw(), (p.x + scroll, screensize[1] - p.y)) # Draw
			p.x += p.v[0]
			p.y += p.v[1]
			p.v[0] *= 0.7
			p.v[1] -= 0.1
			if p.y < p.img.get_height(): # Collision with floor
				p.y = p.img.get_height()
				p.v[1] = 0
			p.health -= 1
			if p.health <= 0:
				people.remove(p)
			# Move towards player
			if p.x < playerpos[0] + (p.img.get_width() / -2):
				if p.canmoveright:
					# Move right
					p.v[0] += 0.4
				else:
					# Jump
					p.v[1] += 0.65
			if p.x > playerpos[0] + (p.img.get_width() / -2):
				if p.canmoveleft:
					# Move left
					p.v[0] -= 0.4
				else:
					# Jump
					p.v[1] += 0.65
			p.canmoveleft = True
			p.canmoveright = True
		# Draw the text
		text = font.render(f"{loc('Gameplay - Amount of wood')}: {amount_wood}", True, (0, 0, 0))
		screen.blit(text, (0, 0))
		# Flip
		pygame.display.flip()
		c.tick(60)
		sounds.chainsaw_active_tick()

MAIN()