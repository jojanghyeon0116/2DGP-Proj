from pico2d import *
import Skill
import game_world
from Item import *
import game_framework
from Character import Character
from background import Portal, Shop
import monster
import stage_3
import UI
import Shop_window
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
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            center_x, center_y = get_canvas_width() // 2, get_canvas_height() // 2
            if center_x - 50 < event.x < center_x + 50 and center_y - 50 < event.y < center_y + 50:
                game_framework.push_mode(Shop_window)
        else:
            common.character.handle_event(event)

def init(job_name, current_hp=None, current_money=None, current_level=None):
    global running
    global platform

    running = True
    common.character = Character(job_name, 400, 200, current_hp=current_hp, current_money=current_money)
    game_world.add_object(common.character, 1)

    shop = Shop(common.character)
    game_world.add_object(shop, 0)

    portal = Portal(common.character, shop, 800, 200, next_mode=stage_3)
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
    game_world.add_collision_pair('character:back_ground', common.character, shop)
    game_world.add_collision_pair('character:portal', common.character, portal)

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

