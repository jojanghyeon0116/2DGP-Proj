from pico2d import *
from sdl2 import *
import game_framework
import game_world
from state_machine import StateMachine
from Skill import skill_1, skill_2, skill_3

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

def space_down(e): # e is space down ?
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def ctrl_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LCTRL

def c_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_c

def x_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_x

def z_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_z

def hit(e):
    return e[0] == 'HIT'

def dead(e):
    return e[0] == 'DEAD'

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

action_finish = lambda e: e[0] == 'FINISH'

class Idle:

    def __init__(self, character):
        self.character = character
        if self.character.job == 'Swordsman':
            self.max_frame = 8
        elif self.character.job == 'Archer':
            self.max_frame = 6
        elif self.character.job == 'Wizard':
            self.max_frame = 6
    def enter(self, e):
        self.character.frame = 0  # 프레임 초기화
        self.character.image = load_image(f'{self.character.job}/Idle.png')


    def exit(self, e):
        if z_down(e):
            self.character.Skill_3()
        elif x_down(e):
            self.character.Skill_2()
        elif c_down(e):
            self.character.Skill_1()


    def do(self):
        if self.character.job == 'Swordsman':
            self.character.frame = (self.character.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 8
        elif self.character.job == 'Archer':
            self.character.frame = (self.character.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 6
        elif self.character.job == 'Wizard':
            self.character.frame = (self.character.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 6

    def draw(self):
        if self.character.direction_x == 1 or self.character.direction_x == 0: # right
            self.character.image.clip_draw(int(self.character.frame) * 128, 0, 128, 128, self.character.x, self.character.y)
        elif self.character.direction_x == -1: # direction_x == -1: # left
            self.character.image.clip_composite_draw(int(self.character.frame) * 128, 0, 128, 128, 0, 'h', self.character.x,self.character.y, 128, 128)

class run:
    def __init__(self, character):
        self.character = character
        self.max_frame = 8
        self.max_distance = 0
        self.dash = False
    def enter(self, e):
        self.character.frame = 0  # 프레임 초기화
        if right_down(e):
            self.character.direction_x = 1
            self.character.move = True
        elif left_down(e):
            self.character.direction_x = -1
            self.character.move = True
        elif c_down(e):
            self.dash = True
        self.character.frame = 0  # 🌟 프레임 리셋
        self.character.image = load_image(f'{self.character.job}/Run.png')  # 이미지 재설정 (init 대신 enter에서 처리 권장)
        self.max_distance = 0

    def exit(self, e):
        if z_down(e):
            self.character.Skill_3()
        elif x_down(e):
            self.character.Skill_2()
        elif c_down(e):
            self.character.Skill_1()
            if self.character.job == 'Swordsman':
                self.dash = True

    def do(self):
        self.character.frame = (self.character.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.character.x += self.character.direction_x * RUN_SPEED_PPS * game_framework.frame_time * self.character.speed
        if self.dash:
            self.max_distance += self.character.direction_x * RUN_SPEED_PPS * game_framework.frame_time
            if abs(self.max_distance) > 100:
                self.max_distance = 0
                self.dash = False
                self.character.state_machine.handle_state_event(('FINISH', None))

    def draw(self):
        if self.character.direction_x == 1:  # right
            self.character.image.clip_draw(int(self.character.frame) * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(int(self.character.frame) * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)

class jump:
    def __init__(self, character):
        self.character = character
        self.max_frame = 8
    def enter(self, e):
        if self.character.state_machine.cur_state != self:
            self.character.frame = 0
            self.character.image = load_image(f'{self.character.job}/Jump.png')
            self.character.direction_y = 1  # 상승 시작
            self.character.jump_peak_y = (self.character.y - 64) + self.character.max_jump_height + 64
        previous_state = self.character.state_machine.cur_state
        if right_down(e):
            self.character.direction_x = 1
        elif left_down(e):
            self.character.direction_x = -1
        elif e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE:
            if previous_state == self.character.IDLE:
                self.character.direction_x = 0
            pass

    def exit(self, e):
        pass

    def do(self):
        self.character.frame = (self.character.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.character.y += self.character.direction_y * RUN_SPEED_PPS * game_framework.frame_time
        if self.character.direction_x != 0:
            self.character.x += self.character.direction_x * RUN_SPEED_PPS * game_framework.frame_time * self.character.speed


    def draw(self):
        if self.character.direction_x == 1 or self.character.direction_x == 0:  # right
            self.character.image.clip_draw(int(self.character.frame) * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(int(self.character.frame) * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)


class attack:
    def __init__(self, character):
        self.character = character
        if self.character.job == 'Swordsman':
            self.max_frame = 4
        elif self.character.job == 'Archer':
            self.max_frame = 14
        elif self.character.job == 'Wizard':
            self.max_frame = 4

    def enter(self, e):
        self.character.frame = 0
        self.character.image = load_image(f'{self.character.job}/Attack.png')
        if ctrl_down(e):
            if self.character.job == 'Swordsman':
                hitbox = AttackHitbox(self.character.x, self.character.y, self.character.direction_x or 1, self.character.attack_damage)
                game_world.add_object(hitbox, 1)  # Layer 1에 Hitbox 추가
                game_world.add_collision_pair('hitbox:monster', hitbox, None)
            if self.character.job == 'Archer' or self.character.job == 'Wizard':
                projectile = Projectile(self.character)
                game_world.add_object(projectile, 1)
                game_world.add_collision_pair('projectile:monster', projectile, None)

    def exit(self, e):
        pass

    def do(self):
        # 프레임을 먼저 증가시키고
        self.character.frame = (self.character.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time)
        # 최대 프레임에 도달하면 상태 전환
        if self.character.frame >= self.max_frame:
            self.character.state_machine.handle_state_event(('FINISH', None))
    def draw(self):
        if self.character.direction_x == 1:  # right
            self.character.image.clip_draw(int(self.character.frame) * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(int(self.character.frame) * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)

class hurt:
    def __init__(self, character):
        self.character = character
        if self.character.job == 'Swordsman':
            self.max_frame = 3
        elif self.character.job == 'Archer':
            self.max_frame = 3
        elif self.character.job == 'Wizard':
            self.max_frame = 4
    def enter(self, e):
        self.character.frame = 0
        self.character.image = load_image(f'{self.character.job}/Hurt.png')

    def exit(self, e):
        pass
    def do(self):
        self.character.frame = self.character.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time
        self.character.x += self.character.knockback_distance * RUN_SPEED_PPS * game_framework.frame_time
        if self.character.frame >= self.max_frame:
            self.character.state_machine.handle_state_event(('FINISH', None))

    def draw(self):
        if self.character.knockback_distance == -1:  # right
            self.character.image.clip_draw(int(self.character.frame) * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(int(self.character.frame) * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)

class dead:
    def __init__(self, character):
        self.character = character
        if self.character.job == 'Swordsman':
            self.max_frame = 3
        elif self.character.job == 'Archer':
            self.max_frame = 3
        elif self.character.job == 'Wizard':
            self.max_frame = 4
    def enter(self, e):
        self.character.frame = 0
        self.character.image = load_image(f'{self.character.job}/Dead.png')

    def exit(self, e):
        game_framework.quit()

    def do(self):
        self.character.frame = self.character.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time
        # 최대 프레임에 도달하면 상태 전환
        if self.character.frame >= self.max_frame:
            game_framework.quit()
    def draw(self):
        if self.character.direction_x == 1:  # right
            self.character.image.clip_draw(int(self.character.frame) * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(int(self.character.frame) * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)

class AttackHitbox:
    def __init__(self, x, y, direction_x, damage):
        self.x, self.y = x + 50 * (direction_x or 1), y
        self.direction_x = direction_x
        self.lifetime = 0.15  # 판정 유지 시간 (0.15초)
        self.damage_dealt = False # 🚩 피해를 한 번만 주도록 플래그 추가
        self.damage = damage

    def update(self):
        self.lifetime -= game_framework.frame_time
        if self.lifetime <= 0:
            game_world.remove_object(self)

    def draw(self):
        # 디버깅용: 충돌 박스 확인 (주석 처리 가능)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 40, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        pass

class Projectile:
    def __init__(self, character):
        self.character = character
        self.x, self.y = self.character.x, self.character.y - 30
        self.direction_x = self.character.direction_x
        self.damage = self.character.attack_damage
        self.speed = 10 # 투사체 속도
        if self.character.job == 'Archer':
            self.image = load_image(f'{self.character.job}/Arrow.png')
        elif self.character.job == 'Wizard':
            self.image = load_image(f'{self.character.job}/projectile.png')

    def update(self):
        self.x += self.direction_x * self.speed * game_framework.frame_time * self.speed
        if self.x < 0 or self.x > 1024:
            game_world.remove_object(self)

    def draw(self):
        if self.direction_x == 1:  # right
            if self.character.job == 'Archer':
                self.image.clip_draw(0, 0, 48, 48, self.x, self.y, 48, 48)
            elif self.character.job == 'Wizard':
                self.image.clip_draw(0, 0, 1024, 1024, self.x, self.y, 48, 48)
        else:  # direction_x == -1: # left
            if self.character.job == 'Archer':
                self.image.clip_composite_draw(0, 0, 48, 48, 0, 'h', self.x, self.y, 48, 48)
            elif self.character.job == 'Wizard':
                self.image.clip_composite_draw(0, 0, 1024, 1024, 0, 'h', self.x, self.y, 48, 48)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.character.job == 'Archer':
            return self.x - 24, self.y - 12, self.x + 24, self.y + 12
        elif self.character.job == 'Wizard':
            return self.x - 24, self.y - 24, self.x + 24 , self.y + 24

    def handle_collision(self, group, other):
        if group == 'projectile:monster':
            game_world.remove_object(self)



class Character:
    image = None
    def __init__(self, job, x = 400,y = 220):
        self.job = job
        self.x, self.y = x, y
        self.min_y = y
        self.frame = 0
        self.direction_x = 0
        self.direction_y = 0
        self.direction = 0
        self.hp = 110
        self.money = 0
        self.exp = 0
        self.speed = 1
        self.invincible_time = 0.0
        self.max_invincible_time = 0.5
        self.max_jump_height = 180
        self.jump_peak_y = 0
        self.knockback_distance = 0
        self.attack_damage = 10
        self.can_enter_portal = None
        self.IDLE = Idle(self)
        self.ATTACK = attack(self)
        self.JUMP = jump(self)
        self.HURT = hurt(self)
        self.DEAD = dead(self)
        self.RUN = run(self)
        if self.job == 'Swordsman':
            self.state_machine = StateMachine(
                self.IDLE,
                {
                    self.IDLE: {right_down: self.RUN, left_down: self.RUN, ctrl_down: self.ATTACK,
                                space_down: self.JUMP, c_down: self.RUN, x_down: self.ATTACK, z_down: self.ATTACK, hit : self.HURT},
                    self.RUN: {space_down: self.JUMP, right_up: self.IDLE, left_up: self.IDLE, ctrl_down: self.ATTACK, action_finish: self.IDLE, hit : self.HURT},
                    self.JUMP: {right_down: self.JUMP, left_down: self.JUMP, action_finish: self.IDLE, hit : self.HURT},
                    self.ATTACK: {action_finish: self.IDLE, hit : self.HURT},
                    self.HURT: {action_finish: self.IDLE, hit : self.HURT},
                    self.DEAD: {}
                }
            )
        else:
            self.state_machine = StateMachine(
                self.IDLE,
                {
                    self.IDLE: {right_down : self.RUN, left_down: self.RUN, ctrl_down: self.ATTACK,
                                space_down: self.JUMP, c_down: self.ATTACK, x_down: self.ATTACK, z_down: self.ATTACK, hit : self.HURT},
                    self.RUN: {space_down: self.JUMP, right_up: self.IDLE, left_up: self.IDLE, ctrl_down: self.ATTACK,action_finish: self.IDLE, hit : self.HURT},
                    self.JUMP: {right_down: self.JUMP, left_down: self.JUMP, action_finish: self.IDLE, hit : self.HURT},
                    self.ATTACK: {action_finish : self.IDLE, hit : self.HURT},
                    self.HURT: {action_finish : self.IDLE, hit : self.HURT},
                    self.DEAD: {}
                }
            )
        pass
    def update(self):
        self.state_machine.update()
        if self.invincible_time > 0:
            self.invincible_time -= game_framework.frame_time
            if self.invincible_time < 0:
                self.invincible_time = 0  # 무적 시간 종료

        if self.direction_y != 0:
            self.y += self.direction_y * RUN_SPEED_PPS * game_framework.frame_time

                # 2. 최고점 도달 확인 (점프 상한선)
        if self.y >= self.jump_peak_y and self.direction_y == 1:
            self.direction_y = -1  # 하강 시작

                # 3. 지면(y=220) 착지 처리
        if self.y < self.min_y:
            self.y = self.min_y
            self.direction_y = 0

                # 지면에 닿았을 때 JUMP 상태를 IDLE로 전환
            if self.state_machine.cur_state == self.JUMP:
                self.state_machine.handle_state_event(('FINISH', None))
        if self.direction_y == 0 and self.y > self.min_y:
            self.direction_y = -1  # 하강 시작

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 32, self.y - 64, self.x + 32 , self.y + 10

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        if up_down(('INPUT', event)) and self.can_enter_portal is not None:
            next_mode = self.can_enter_portal.next_stage_mode
            if next_mode:
                game_framework.change_mode(next_mode, self.job)
                return  # 이벤트 처리 완료
    def Skill_1(self):
        skill1 = skill_1(self.x, self.y, self.direction_x, self.job, self.speed)
        game_world.add_object(skill1, 1)
        game_world.add_collision_pair('skill:monster', skill1, None)
    def Skill_2(self):
        skill2 = skill_2(self.x, self.y, self.direction_x, self.job)
        game_world.add_object(skill2, 1)
        game_world.add_collision_pair('skill:monster', skill2, None)
    def Skill_3(self):
        skill3 = skill_3(self.x, self.y, self.direction_x, self.job)
        game_world.add_object(skill3, 1)
        game_world.add_collision_pair('skill:monster', skill3, None)

    def handle_collision(self, group, other):
        if group == 'character:monster':
            is_dashing = self.state_machine.cur_state == self.RUN and self.RUN.dash
            if is_dashing:
                # 몬스터와 충돌 시 돌진 중단 및 IDLE 상태로 전환
                self.RUN.dash = False
                self.RUN.max_distance = 0
                self.direction_x = 0
                self.state_machine.handle_state_event(('FINISH', None))

            if self.invincible_time > 0:
                return

            self.hp -= 10
            print(f'Character HP: {self.hp}')

            self.invincible_time = self.max_invincible_time
            self.knockback_distance = other.direction
            if self.hp > 0 and other.attacking:
                self.state_machine.handle_state_event(('HIT', None))
            elif self.hp <= 0 and other.attacking:
                # 1. DEAD 상태로 강제 전환 (StateMachine 객체 교체)
                self.state_machine.cur_state = self.DEAD

                # 2. DEAD.enter(None) 호출 (애니메이션 초기화)
                self.DEAD.enter(None)
        elif group == 'character:platform':
            # 캐릭터의 바닥 좌표 계산: 캐릭터 중심 Y (self.y) - 64
            char_bottom = self.y - 64

            # other (Platform)의 BB 가져오기
            platform_left, platform_bottom, platform_right, platform_top = other.get_bb()

            # 1. 수평 범위 확인
            char_left, _, char_right, _ = self.get_bb()
            if char_right > platform_left and char_left < platform_right:

                # 2. 상단 충돌 조건 (하강 중이고, 캐릭터 바닥이 블록 상단에 가까이 닿았을 때)
                # platform_top 바로 위에 착지할 만큼 가까운지 확인
                if self.direction_y <= 0 and char_bottom <= platform_top and char_bottom > platform_top - 10:

                    # 🌟 정확한 착지 위치 설정 🌟
                    # 새로운 Y 좌표 = 블록 상단 + 캐릭터 바닥에서 중심까지의 거리 (64)
                    new_y = platform_top + 64

                    self.y = new_y
                    self.direction_y = 0  # 🌟 수직 속도를 0으로 멈춤 (블록 위에 고정)

                    # 🌟 착지 애니메이션 전환
                    if self.state_machine.cur_state == self.JUMP:
                        self.state_machine.handle_state_event(('FINISH', None))

                    return  # 충돌 처리 완료
        elif group == 'character:back_ground':
            ground_left, ground_bottom, ground_right, ground_top = other.get_bb()
            if self.x - 32 < ground_left:
                self.x = ground_left + 32
            elif self.x + 32> ground_right:
                self.x = ground_right - 32
        elif group == 'character:portal':
            self.can_enter_portal = other

