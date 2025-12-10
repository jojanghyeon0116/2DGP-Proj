from pico2d import *
import game_world
import game_framework
import character_selection as start_mode

open_canvas(1024, 800)
bgm = load_music('InTheForest.wav')
bgm.set_volume(100)
bgm.repeat_play()
game_framework.run(start_mode)
update_canvas()

