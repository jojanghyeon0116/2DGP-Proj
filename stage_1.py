from pico2d import *
import Skill
import game_world
from Item import *
import game_framework
from monster import Monster
from Character import Character
from background import Ground, Platform, Portal
import monster
import stage_2
import UI
import common

def handle_events():
    global running
    global skill_effect
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            common.character.handle_event(event)

def init(job_name, current_hp=None, current_money=None, current_level=None):
    global running
    global platform
    global health_bar
    running = True
    common.character = Character(job_name, 200, 220, current_hp=current_hp, current_money=current_money)
    game_world.add_object(common.character, 1)

    monster = Monster(common.character)
    game_world.add_object(monster, 1)

    back_ground = Ground(common.character)
    game_world.add_object(back_ground, 0)

    platform = Platform(common.character, back_ground, 200, 300)
    game_world.add_object(platform, 0)

    portal = Portal(common.character, back_ground, 1200, 220, next_mode=stage_2)
    game_world.add_object(portal, 0)

    health_bar = UI.HealthBar(common.character)
    game_world.add_object(health_bar, 0)

    skill_icon1 = UI.Skill_icon1(common.character)
    game_world.add_object(skill_icon1, 0)

    skill_icon2 = UI.Skill_icon2(common.character)
    game_world.add_object(skill_icon2, 0)

    skill_icon3 = UI.Skill_icon3(common.character)
    game_world.add_object(skill_icon3, 0)

    money_display = UI.MoneyDisplay(common.character)
    game_world.add_object(money_display, 0)

    level = UI.Level(common.character)
    game_world.add_object(level, 0)

    game_world.add_collision_pair('character:item', common.character, None)
    game_world.add_collision_pair('character:monster', common.character, monster)
    game_world.add_collision_pair('hitbox:monster', None, monster)
    game_world.add_collision_pair('skill:monster', None, monster)
    game_world.add_collision_pair('projectile:monster', None, monster)
    game_world.add_collision_pair('character:platform', common.character, platform)
    game_world.add_collision_pair('character:back_ground', common.character, back_ground)
    game_world.add_collision_pair('character:portal', common.character, portal)

def update():
    global platform  # 🌟 platform 객체 사용 선언
    offset_value = platform.update()

    monster.camera_offset_x = offset_value
    item.camera_offset_x = offset_value
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

