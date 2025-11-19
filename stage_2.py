from pico2d import *
import Skill
import game_world
from Item import *
import game_framework
from Character import Character
from background import Portal, Shop
import monster

def handle_events():
    global running
    global skill_effect
    global characters
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            characters.handle_event(event)

def init(job_name):
    global characters
    global running
    global platform

    running = True
    characters = Character(job_name)
    game_world.add_object(characters, 1)

    shop = Shop(characters)

    portal = Portal(characters, shop, 1200, 220)
    game_world.add_object(portal, 0)

    game_world.add_collision_pair('character:item', characters, None)
    game_world.add_collision_pair('character:back_ground', characters, shop)
    game_world.add_collision_pair('character:portal', characters, portal)

def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

