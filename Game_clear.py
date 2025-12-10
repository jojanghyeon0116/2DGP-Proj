from pico2d import *

import UI
from Item import *
import game_framework
import common

image = None
def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
def init():
    global image
    if image is None:
        image = load_image('game_clear.png')
def update():
    pass

def draw():
    global image
    clear_canvas()
    game_world.render()
    image.draw(512,400)
    update_canvas()

def finish():
    pass

def pause(): pass
def resume(): pass
