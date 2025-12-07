from pico2d import *

import UI
from Item import *
import game_framework


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if 520 < event.x < 620 and 600 < event.y < 650:
                game_framework.pop_mode()
def init():
    global pannel
    pannel = UI.Shop_pannel()
    game_world.add_object(pannel, 2)
def update():
    pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.remove_object(pannel)

def pause(): pass
def resume(): pass
