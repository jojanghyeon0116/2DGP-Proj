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


def init(job_name, current_hp=None, current_money=None, current_level=None, current_exp=None):
    global running
    global platform
    global health_bar
    running = True

    # -------------------------------------------------------------
    # 1. 캐릭터 및 배경 설정
    common.character = Character(job_name, 200, 220, current_hp=current_hp, current_money=current_money, current_level=current_level, current_exp=current_exp)
    game_world.add_object(common.character, 1)

    back_ground = Ground(common.character)
    game_world.add_object(back_ground, 0)

    # -------------------------------------------------------------
    # 2. 플랫폼 및 몬스터 배치 (확장된 스테이지 구현)

    monsters = []
    platform = []

    # 🚩 플랫폼 배치 (기존 4개 유지)

    # Platform 1 (시작 지점 근처) - World X: 200, Y: 300
    platform1 = Platform(common.character, back_ground, 200, 300)
    game_world.add_object(platform1, 0)
    platform.append(platform1)

    # Platform 2 (중앙 왼쪽) - World X: 550, Y: 400
    platform2 = Platform(common.character, back_ground, 550, 400)
    game_world.add_object(platform2, 0)
    platform.append(platform2)

    # Platform 3 (중앙 오른쪽) - World X: 900, Y: 300
    platform3 = Platform(common.character, back_ground, 900, 300)
    game_world.add_object(platform3, 0)
    platform.append(platform3)



    # 1. 바닥 (World Y: 220) - 7마리
    for i in range(7):
        m = Monster(common.character)
        m.x, m.y = 300 + i * 150, 220
        game_world.add_object(m, 1)
        monsters.append(m)

    # 2. Platform 1 위 (World X: 200, Y: 350) - 2마리
    for i in range(2):
        m = Monster(common.character)
        m.x, m.y = 150 + i * 100, 380
        game_world.add_object(m, 1)
        monsters.append(m)

    # 3. Platform 2 위 (World X: 550, Y: 450) - 3마리
    for i in range(3):
        m = Monster(common.character)
        m.x, m.y = 450 + i * 80, 480
        game_world.add_object(m, 1)
        monsters.append(m)

    # 4. Platform 3 위 (World X: 900, Y: 350) - 3마리
    for i in range(3):
        m = Monster(common.character)
        m.x, m.y = 800 + i * 100, 380
        game_world.add_object(m, 1)
        monsters.append(m)


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

    # -------------------------------------------------------------
    # 4. 충돌 페어 설정

    game_world.add_collision_pair('character:item', common.character, None)
    game_world.add_collision_pair('character:back_ground', common.character, back_ground)
    game_world.add_collision_pair('character:portal', common.character, portal)

    # 몬스터와 충돌 페어 연결
    for m in monsters:
        game_world.add_collision_pair('character:monster', common.character, m)
        game_world.add_collision_pair('hitbox:monster', None, m)
        game_world.add_collision_pair('skill:monster', None, m)
        game_world.add_collision_pair('projectile:monster', None, m)
        game_world.add_collision_pair('monster:platform', m, None)

    # 플랫폼과 충돌 페어 연결
    for p in platform:
        game_world.add_collision_pair('character:platform', common.character, p)
        game_world.add_collision_pair('monster:platform', None, p)


def update():
    global platform

    if platform:
        offset_value = platform[0].update()
    else:
        offset_value = 0

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