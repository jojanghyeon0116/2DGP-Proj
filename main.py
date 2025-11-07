from pico2d import *

import Skill
import monster
from Character import Character
from Item import item
CHARACTER_POSITIONS = {
    # Swordsman 영역 (예시: x=100 ~ 300)
    'Swordsman': (50, 300),
    # Wizard 영역 (예시: x=350 ~ 550)
    'Wizard': (300, 550),
    # Archer 영역 (예시: x=600 ~ 800)
    'Archer': (550, 800)
}
# 캐릭터들의 Y축 범위는 캔버스 중앙 근처 (851px 기준, 예를 들어 y=400 ~ 500)
CHARACTER_Y_RANGE = (200, 500)

selection_image = None
def load_selection_image():
    global selection_image
    if selection_image is None:
        selection_image = load_image('character_select.png')

def show_character_selection():
    global characterjob
    global character_select
    global selection_image
    load_selection_image()
    clear_canvas()
    if selection_image:
        selection_image.draw(800 // 2, 851 // 2)
    update_canvas()
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            global running
            running = False
            character_select = False

        # 마우스 이벤트 처리
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                # Y좌표 변환 (Pico2D 좌하단 (0,0) 기준)
                mouse_x, mouse_y = event.x, 800 - 1 - event.y

                # Y축 범위 내에 있는지 확인
                if CHARACTER_Y_RANGE[0] <= mouse_y <= CHARACTER_Y_RANGE[1]:

                    # 1. Swordsman 선택 영역 확인
                    if CHARACTER_POSITIONS['Swordsman'][0] <= mouse_x <= CHARACTER_POSITIONS['Swordsman'][1]:
                        characterjob = 'Swordsman'
                        character_select = False

                    # 2. Wizard 선택 영역 확인
                    elif CHARACTER_POSITIONS['Wizard'][0] <= mouse_x <= CHARACTER_POSITIONS['Wizard'][1]:
                        characterjob = 'Wizard'
                        character_select = False

                    # 3. Archer 선택 영역 확인
                    elif CHARACTER_POSITIONS['Archer'][0] <= mouse_x <= CHARACTER_POSITIONS['Archer'][1]:
                        characterjob = 'Archer'
                        character_select = False

    pass

def handle_events():
    global running
    global skill_effect
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_LCTRL:
                if not characters.attacking and not characters.jumping and not characters.hurt and characters.hp > 0:
                    characters.attacking = True
                    characters.image = load_image(f'{characterjob}/Attack.png')  # Attack.png 로드
                    characters.frame = 0
            if not characters.attacking:
                if event.key == SDLK_RIGHT:
                    characters.direction_x = 1
                    characters.move = True
                elif event.key == SDLK_LEFT:
                    characters.direction_x = -1
                    characters.move = True
                elif event.key == SDLK_SPACE:
                    if not characters.jumping:  # 점프 중이 아닐 때만 점프 가능
                        characters.image = load_image(f'{characterjob}/Jump.png')
                        characters.direction_y = 1
                        characters.jumping = True
                        characters.move = True
                        characters.frame = 0
                elif event.key == SDLK_g:
                    characters.hurt = True
                    characters.image = load_image(f'{characterjob}/Hurt.png')
                    characters.frame = 0
                elif event.key == SDLK_c:
                    skill_effect.skill_p = 1
                    skill_effect.image = load_image(f'{characterjob}/Skill1.png')
                    if characterjob == 'Swordsman':
                        characters.image = load_image(f'{characterjob}/Run.png')
                        characters.frame = 0
                        characters.direction_x = 1
                        skill_effect.x = characters.x + 50
                        skill_effect.y = characters.y - 20
                    else:
                        skill_effect.x = characters.x + 50
                        skill_effect.y = characters.y - 20
                        characters.attacking = True
                        characters.image = load_image(f'{characterjob}/Attack.png')  # Attack.png 로드
                        characters.frame = 0
                elif event.key == SDLK_x:
                    skill_effect.skill_p = 2
                    skill_effect.image = load_image(f'{characterjob}/Skill2.png')
                    if characterjob == 'Wizard':
                        skill_effect.x = characters.x + 50
                        skill_effect.y = characters.y - 20
                        characters.attacking = True
                        characters.image = load_image(f'{characterjob}/Attack.png')  # Attack.png 로드
                        characters.frame = 0
                    elif characterjob == 'Archer':
                        skill_effect.x = characters.x + 50
                        skill_effect.y = characters.y - 20
                        characters.attacking = True
                        characters.image = load_image(f'{characterjob}/Attack.png')  # Attack.png 로드
                        characters.frame = 0
                elif event.key == SDLK_z:
                    skill_effect.skill_p = 3
                    skill_effect.image = load_image(f'{characterjob}/Skill3.png')
                    skill_effect.x = characters.x + 50
                    skill_effect.y = characters.y - 20
                    characters.attacking = True
                    characters.image = load_image(f'{characterjob}/Attack.png')  # Attack.png 로드
                    characters.frame = 0

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                if characters.direction_x == 1:
                    characters.image = load_image(f'{characterjob}/Idle.png')
                characters.direction_x = 0
                characters.move = False
            elif event.key == SDLK_LEFT:
                if characters.direction_x == -1:
                    characters.image = load_image(f'{characterjob}/Idle.png')
                characters.direction_x = 0
                characters.move = False
            elif event.key == SDLK_SPACE:
                characters.move = False


def reset_world():
    global world
    global characters
    global skill_effect
    global item
    world = []

    characters = Character(characterjob)
    world.append(characters)
    skill_effect = Skill.skill_effect(characters, characterjob, 0)
    world.append(skill_effect)
    monster.monster = monster.monster(characters)
    world.append(monster.monster)
    item = item(4)
    world.append(item)


def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

running = True
character_select = True
open_canvas(800,851)
while character_select:
    show_character_selection()
reset_world()
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.1)
close_canvas()
