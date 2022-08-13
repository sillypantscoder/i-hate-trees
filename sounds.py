import pygame.mixer as mixer

mixer.init()

chainsaw = mixer.Sound('assets/chainsaw-07-combined.wav')
chainsaw_end = mixer.Sound('assets/chainsaw-01-end.wav')

chainsaw_channel = mixer.find_channel(True)

def start_chainsaw():
	chainsaw_channel.play(chainsaw, loops=-1)

def stop_chainsaw():
	chainsaw_channel.stop()
	chainsaw_channel.play(chainsaw_end)

def menu_start():
	mixer.music.load('assets/9. KIWF+More+Scared+of+You.wav')
	mixer.music.play(-1)

def gameplay_start():
	mixer.music.load('assets/5. black_game_music.wav')
	mixer.music.play(-1)

def stop_background():
	mixer.music.stop()
