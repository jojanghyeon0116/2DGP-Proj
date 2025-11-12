import game_framework
from pico2d import *
import play_mode
from Character import Character

CHARACTER_POSITIONS = {
    # Swordsman 영역 (예시: x=100 ~ 300)
    'Swordsman': (50, 300),
    # Wizard 영역 (예시: x=350 ~ 550)
    'Wizard': (400, 650),
    # Archer 영역 (예시: x=600 ~ 800)
    'Archer': (700, 1000)
}
# 캐릭터들의 Y축 범위는 캔버스 중앙 근처 (851px 기준, 예를 들어 y=400 ~ 500)
CHARACTER_Y_RANGE = (200, 500)

def init():
     global image
     global running
     image = load_image('character_select.png')
     running = True

def finish():
    global image
    del image

def update():
    pass

def draw():
    clear_canvas()
    image.draw(1024 // 2, 800 // 2, 1024, 800)
    update_canvas()

def handle_events():
    global characterjob
    global running
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:  # 마우스 이벤트 처리
            if event.button == SDL_BUTTON_LEFT:
                # Y좌표 변환 (Pico2D 좌하단 (0,0) 기준)
                mouse_x, mouse_y = event.x, 800 - 1 - event.y
                # Y축 범위 내에 있는지 확인
                if CHARACTER_Y_RANGE[0] <= mouse_y <= CHARACTER_Y_RANGE[1]:

                    # 1. Swordsman 선택 영역 확인
                    if CHARACTER_POSITIONS['Swordsman'][0] <= mouse_x <= CHARACTER_POSITIONS['Swordsman'][1]:
                        characterjob = 'Swordsman'
                        game_framework.change_mode(play_mode, characterjob)
                        clear_canvas()

                    # 2. Wizard 선택 영역 확인
                    elif CHARACTER_POSITIONS['Wizard'][0] <= mouse_x <= CHARACTER_POSITIONS['Wizard'][1]:
                        characterjob = 'Wizard'
                        game_framework.change_mode(play_mode, characterjob)
                        clear_canvas()

                    # 3. Archer 선택 영역 확인
                    elif CHARACTER_POSITIONS['Archer'][0] <= mouse_x <= CHARACTER_POSITIONS['Archer'][1]:
                        characterjob = 'Archer'
                        game_framework.change_mode(play_mode, characterjob)
                        clear_canvas()
def pause(): pass
def resume(): pass