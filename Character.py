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
        self.character.frame = 0  # 프레임 초기화
        self.character.image = load_image(f'{self.character.job}/Jump.png')
        self.character.direction_y = 1
        pass

    def exit(self, e):
        pass

    def do(self):
        self.character.frame = (self.character.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.character.y += self.character.direction_y * RUN_SPEED_PPS * game_framework.frame_time
        if self.character.y >= 440:  # 최고점 도달
            self.character.direction_y = -1  # 하강 시작
        if self.character.y <= 400:  # 바닥 도달
            self.character.y = 400
            self.character.direction_y = 0
            self.character.state_machine.handle_state_event(('FINISH', None))
    def draw(self):
        if self.character.direction_x == 1:  # right
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

                from monster import Monster
                for obj in game_world.world[1]:
                    if isinstance(obj, Monster):
                        game_world.add_collision_pair('hitbox:monster', hitbox, obj)
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
        self.character.x += -self.character.direction_x * RUN_SPEED_PPS * game_framework.frame_time
        if self.character.frame >= self.max_frame:
            self.character.state_machine.handle_state_event(('FINISH', None))

    def draw(self):
        if self.character.direction_x == 1:  # right
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
        # 이 객체는 몬스터에게 피해를 입히는 역할만 하므로, 몬스터가 처리합니다.
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
        if self.x < 0 or self.x > 800:
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
    def __init__(self, job):
        self.job = job
        self.x, self.y = 400, 400
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
        self.attack_damage = 10
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
                    self.JUMP: {action_finish: self.IDLE, hit : self.HURT},
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
                    self.JUMP: {action_finish : self.IDLE, hit : self.HURT},
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
    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 32, self.y - 64, self.x + 32 , self.y + 10

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

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
            if self.invincible_time > 0:
                return

            self.hp -= 10
            print(f'Character HP: {self.hp}')

            self.invincible_time = self.max_invincible_time


            if self.hp > 0 and other.attacking:
                self.state_machine.handle_state_event(('HIT', None))
            elif self.hp <= 0 and other.attacking:
                # 1. DEAD 상태로 강제 전환 (StateMachine 객체 교체)
                self.state_machine.cur_state = self.DEAD

                # 2. DEAD.enter(None) 호출 (애니메이션 초기화)
                self.DEAD.enter(None)