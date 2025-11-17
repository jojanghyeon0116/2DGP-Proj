from pico2d import *
import Skill
import game_world
from Item import *
import game_framework
from monster import Monster
from Character import Character
from background import Ground, Platform


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

    running = True
    characters = Character(job_name)
    game_world.add_object(characters, 1)

    monster = Monster(characters)
    game_world.add_object(monster, 1)

    back_ground = Ground(characters)
    game_world.add_object(back_ground, 0)

    platform = Platform(characters, back_ground, 200, 300)
    game_world.add_object(platform, 0)

    game_world.add_collision_pair('character:item', characters, None)
    game_world.add_collision_pair('character:monster', characters, monster)
    game_world.add_collision_pair('skill:monster', None, monster)
    game_world.add_collision_pair('projectile:monster', None, monster)
    game_world.add_collision_pair('character:platform', characters, platform)
    game_world.add_collision_pair('character:back_ground', characters, back_ground)

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

