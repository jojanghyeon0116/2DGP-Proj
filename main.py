from pico2d import *

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
characterjob = ' '

class Character:
    image = None
    def __init__(self):
        self.x, self.y = 400, 400
        self.frame = 0
        self.direction_x = 0
        self.direction_y = 0
        self.direction = 0
        self.move = False
        self.jumping = False  # 점프 중인지 여부
        self.hurt = False
        self.attacking = False
        self.hp = 100
        if Character.image is None and characterjob == 'Swordsman':
            Character.image = load_image('Swordsman/Idle.png')
        elif Character.image is None and characterjob == 'Archer':
            Character.image = load_image('Archer/Idle.png')
        elif Character.image is None and characterjob == 'Wizard':
            Character.image = load_image('Wizard/Idle.png')

        pass
    def update(self):
        if self.attacking:
            # 캐릭터별 공격 프레임 수
            attack_frames = {'Swordsman': 4, 'Archer': 14, 'Wizard': 4}  # 예시 프레임 수, 실제 이미지에 맞게 조정 필요
            max_frames = attack_frames.get(characterjob, 4)  # 기본값 4

            self.frame = (self.frame + 1)
            if self.frame >= max_frames:
                self.attacking = False  # 공격 애니메이션 종료
                self.frame = 0
                self.image = load_image(f'{characterjob}/Idle.png')  # 대기 상태로 복귀

            # 공격 중에는 이동/점프/피격 애니메이션 업데이트를 스킵
            return
        if self.hp <= 0:
            characters.image = load_image(f'{characterjob}/Dead.png')
        if characterjob == 'Swordsman':
            if self.hurt or self.hp <= 0:
                self.frame = (self.frame + 1) % 3
            else:
                self.frame = (self.frame + 1) % 8
        elif characterjob == 'Archer':
            if not characters.move and not self.hurt:
                self.frame = (self.frame + 1) % 6
            elif self.hurt or self.hp <= 0:
                self.frame = (self.frame + 1) % 3
            else:
                self.frame = (self.frame + 1) % 8
        elif characterjob == 'Wizard':
            if not characters.move and not self.hurt:
                self.frame = (self.frame + 1) % 6
            elif self.hurt or self.hp <= 0:
                self.frame = (self.frame + 1) % 4
            else:
                self.frame = (self.frame + 1) % 8
        self.x += self.direction_x * 10
        if self.jumping:
            self.y += self.direction_y * 10
            if self.y >= 440:  # 최고점 도달
                self.direction_y = -1  # 하강 시작
            if self.y <= 400:  # 바닥 도달
                self.jumping = False
                self.y = 400
                self.direction_y = 0
                self.image = load_image(f'{characterjob}/Idle.png')
                self.move = False
        pass

    def draw(self):
        if self.direction_x == 1:
            self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y)
        elif self.direction_x == -1:
            self.image.clip_composite_draw(self.frame * 128, 0, 128, 128, 0, 'h', self.x, self.y, 128, 128)
        else:  # 정지 상태 (마지막 이동 방향에 따라)
            self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y)
        pass

class skill_effect:
    Skill_c = False
    Skill_x = False
    Skill_z = False
    image = None
    def __init__(self):
        self.x, self.y = 0, 0
        self.frame = 0
        self.move_count = 0
        self.image = None
        pass

    def start_effect(self, target_x, target_y):
        self.x = target_x
        self.y = target_y

    def update(self):
        if self.Skill_c:
            if characterjob == 'Swordsman':
                skill_offset = 40
                target_x = characters.x + (skill_offset if characters.direction == 0 else -skill_offset)
                target_y = characters.y - 20

                self.start_effect(target_x, target_y)
                self.frame = (self.frame + 1) % 3
                self.move_count += characters.direction_x * 5
                characters.x += characters.direction_x * 5
            elif characterjob == 'Wizard':
                self.frame = (self.frame + 1) % 3
                self.x += 10
            elif characterjob == 'Archer':
                self.frame = (self.frame + 1) % 4
                self.x += 10
        if self.move_count >= 30:
            self.Skill_c = False
            self.move_count = 0
            self.frame = 0
            characters.direction_x = 0
            characters.image = load_image(f'{characterjob}/Idle.png')

        if self.Skill_x:
            if characterjob == 'Swordsman':
                skill_offset = 40
                target_y = characters.y + skill_offset
                target_x = characters.x

                self.start_effect(target_x, target_y)
                self.frame = self.frame + 1
                if self.frame >= 5:
                    self.Skill_x = False
                    self.frame = 0
            elif characterjob == 'Wizard':
                self.frame = (self.frame + 1) % 3
                self.x += 10
            elif characterjob == 'Archer':
                self.frame = (self.frame + 1) % 6
                self.x += 10
        if self.Skill_z:
            if characterjob == 'Swordsman':
                self.frame = (self.frame + 1) % 4
                self.x += 10
            elif characterjob == 'Wizard':
                self.frame = (self.frame + 1) % 3
                self.x += 10
            elif characterjob == 'Archer':
                self.frame = (self.frame + 1) % 6
                self.x += 10
        pass

    def draw(self):
        if self.Skill_c:
            if characterjob == 'Swordsman':
                self.image.clip_draw(self.frame * 34, 0, 34, 128, self.x, self.y)
            elif characterjob == 'Wizard':
                self.image.clip_draw(self.frame * 34, 0, 34, 36, self.x, self.y, 30,30)
            elif characterjob == 'Archer':
                self.image.clip_draw(self.frame * 33, 0, 33, 32, self.x, self.y, 50,50)

        elif self.Skill_x:
            if characterjob == 'Swordsman':
                self.image.clip_draw(0, self.frame * 200, 250, 200, self.x, self.y, 75,75)
            elif characterjob == 'Wizard':
                self.image.clip_draw(self.frame * 341 ,0, 341, 284, self.x, self.y, 50,50)
            elif characterjob == 'Archer':
                self.image.clip_draw(self.frame * 170 ,0, 170, 290, self.x, self.y, 100,100)

        elif self.Skill_z:
            if characterjob == 'Swordsman':
                self.image.clip_draw(self.frame * 34, 0, 34, 35, self.x, self.y)
            elif characterjob == 'Wizard':
                self.image.clip_draw(self.frame * 341 ,0, 341, 284, self.x, self.y, 70,70)
            elif characterjob == 'Archer':
                self.image.clip_draw(self.frame * 170 ,0, 170, 200, self.x, self.y, 70,70)
        pass

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
                    if characters.direction_x == 0:
                        characters.image = load_image(f'{characterjob}/Run.png')
                    characters.direction_x = 1
                    characters.move = True
                elif event.key == SDLK_LEFT:
                    if characters.direction_x == 0:
                        characters.image = load_image(f'{characterjob}/Run.png')
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
                    skill_effect.Skill_c = True
                    skill_effect.Skill_z = False
                    skill_effect.Skill_y = False
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
                    skill_effect.image = load_image(f'{characterjob}/Skill2.png')
                    skill_effect.Skill_x = True
                    skill_effect.Skill_y = False
                    skill_effect.Skill_c = False
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
                    skill_effect.Skill_z = True
                    skill_effect.Skill_x = False
                    skill_effect.Skill_c = False
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

class monster:
    image = None
    def __init__(self):
        self.x, self.y = 500, 400
        self.frame = 0
        self.attacking = False
        if monster.image is None:
            monster.image = load_image('Skeleton/Idle.png')
        pass

    def update(self):
        self.frame = (self.frame + 1) % 7
        distance_x = characters.x - self.x

        if abs(distance_x) < 100:
            if distance_x > 0:
                self.x += 5
            elif distance_x < 0:
                self.x -= 5
        if abs(distance_x) < 50 and not self.attacking:
            self.attacking = True
            self.image = load_image('Skeleton/Attack_1.png')
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y)
        pass

def reset_world():
    global world
    global characters
    global skill_effect
    global monster
    world = []

    characters = Character()
    world.append(characters)
    skill_effect = skill_effect()
    world.append(skill_effect)
    monster = monster()
    world.append(monster)
    pass


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
