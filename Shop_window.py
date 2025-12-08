from pico2d import *

import UI
from Item import *
import game_framework
import common

def handle_events():
    event_list = get_events()
    CANVAS_HEIGHT = get_canvas_height()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mouse_y_game_coord = CANVAS_HEIGHT - event.y
            if 520 < event.x < 620 and 170 <  mouse_y_game_coord < 200:
                game_framework.pop_mode()
            elif 350 < event.x < 450 and 480 <  mouse_y_game_coord < 530:
                if common.character.money >= 20:
                    common.character.money -= 20
                    common.character.attack_damage += 5
            elif 350 < event.x < 450 and 380 <  mouse_y_game_coord < 430:
                if common.character.money >= 100:
                    common.character.money -= 100
                    common.character.speed += 10
            elif 350 < event.x < 450 and 280 <  mouse_y_game_coord < 330:
                if common.character.money >= 50:
                    common.character.money -= 50
                    common.character.hp += 20


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
