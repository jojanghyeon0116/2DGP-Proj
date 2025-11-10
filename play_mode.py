from pico2d import *
import Skill
import game_world
from Item import *
import game_framework
from monster import Monster
from Character import Character

def handle_events():
    global running
    global skill_effect
    global characters
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            characters.handle_event(event)

def init(job_name):
    global characters
    global running

    running = True
    characters = Character(job_name)
    game_world.add_object(characters, 1)

    monster = Monster(characters)
    game_world.add_object(monster, 1)

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

