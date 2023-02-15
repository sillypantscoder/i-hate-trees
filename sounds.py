import pygame.mixer as mixer

can_play_sounds = False
try:
	mixer.init()
	can_play_sounds = True
except:
	can_play_sounds = False
	print("ERROR: CANNOT PLAY SOUNDS\n")

if can_play_sounds:
	chainsaw = mixer.Sound('assets/chainsaw-07-combined.wav')
	chainsaw_end = mixer.Sound('assets/chainsaw-01-end.wav')

	chainsaw_channel = mixer.find_channel(True)

def start_chainsaw():
	if can_play_sounds and sounds_active:
		chainsaw_channel.play(chainsaw, loops=-1)

def stop_chainsaw():
	if can_play_sounds and sounds_active:
		chainsaw_channel.stop()
		chainsaw_channel.play(chainsaw_end)

def menu_start():
	if not can_play_sounds: return
	mixer.music.load('assets/9. KIWF+More+Scared+of+You.wav')
	mixer.music.play(-1)

def gameplay_start():
	if not can_play_sounds: return
	mixer.music.load('assets/5. black_game_music.wav')
	mixer.music.play(-1)

def stop_background():
	if not can_play_sounds: return
	mixer.music.stop()

chainsaw_active_status = False
chainsaw_previous_status = False

def chainsaw_active():
	global chainsaw_active_status
	chainsaw_active_status = True

def chainsaw_active_tick():
	global chainsaw_active_status
	global chainsaw_previous_status
	if chainsaw_active_status and not chainsaw_previous_status and sounds_active:
		start_chainsaw()
	elif not chainsaw_active_status and chainsaw_previous_status:
		stop_chainsaw()
	chainsaw_previous_status = chainsaw_active_status
	chainsaw_active_status = False

sounds_active = True
def set_active(status):
	global sounds_active
	sounds_active = status
