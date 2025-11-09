from pico2d import load_image
from sdl2 import *

import game_world
from state_machine import StateMachine
from Skill import skill_1, skill_2, skill_3

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

action_finish = lambda e: e[0] == 'FINISH'

class Idle:

    def __init__(self, character):
        self.character = character
    def enter(self, e):
        self.character.frame = 0  # 프레임 초기화
        self.character.image = load_image(f'{self.character.job}/Idle.png')
        pass

    def exit(self, e):
        if z_down(e):
            self.character.Skill_3()
        elif x_down(e):
            self.character.Skill_2()
        elif c_down(e):
            self.character.Skill_1()


    def do(self):
        if self.character.job == 'Swordsman':
            self.character.frame = (self.character.frame + 1) % 8
        elif self.character.job == 'Archer':
            self.character.frame = (self.character.frame + 1) % 6
        elif self.character.job == 'Wizard':
            self.character.frame = (self.character.frame + 1) % 6

    def draw(self):
        if self.character.direction_x == 1: # right
            self.character.image.clip_draw(self.character.frame * 128, 0, 128, 128, self.character.x, self.character.y)
        else: # direction_x == -1: # left
            self.character.image.clip_composite_draw(self.character.frame * 128, 0, 128, 128, 0, 'h', self.character.x,self.character.y, 128, 128)

class run:
    def __init__(self, character):
        self.character = character

    def enter(self, e):
        self.character.frame = 0  # 프레임 초기화
        if right_down(e):
            self.character.direction_x = 1
            self.character.move = True
        elif left_down(e):
            self.character.direction_x = -1
            self.character.move = True
        self.character.frame = 0  # 🌟 프레임 리셋
        self.character.image = load_image(f'{self.character.job}/Run.png')  # 이미지 재설정 (init 대신 enter에서 처리 권장)

    def exit(self, e):
        if z_down(e):
            self.character.Skill_3()
        elif x_down(e):
            self.character.Skill_2()
        elif c_down(e):
            self.character.Skill_1()

    def do(self):
        self.character.frame = (self.character.frame + 1) % 8
        self.character.x += self.character.direction_x * 10
    def draw(self):
        if self.character.direction_x == 1:  # right
            self.character.image.clip_draw(self.character.frame * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(self.character.frame * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)

class jump:
    def __init__(self, character):
        self.character = character
    def enter(self, e):
        self.character.frame = 0  # 프레임 초기화
        self.character.image = load_image(f'{self.character.job}/Jump.png')
        self.character.direction_y = 1
        pass

    def exit(self, e):
        pass

    def do(self):
        self.character.frame = (self.character.frame + 1) % 8
        self.character.y += self.character.direction_y * 10
        if self.character.y >= 440:  # 최고점 도달
            self.character.direction_y = -1  # 하강 시작
        if self.character.y <= 400:  # 바닥 도달
            self.character.y = 400
            self.character.direction_y = 0
            self.character.state_machine.handle_state_event(('FINISH', None))
    def draw(self):
        if self.character.direction_x == 1:  # right
            self.character.image.clip_draw(self.character.frame * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(self.character.frame * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)


class attack:
    def __init__(self, character):
        self.character = character

    def enter(self, e):
        self.character.frame = 0  # 프레임 초기화
        self.character.image = load_image(f'{self.character.job}/Attack.png')
        pass

    def exit(self, e):
        pass

    def do(self):
        max_frame = 0
        if self.character.job == 'Swordsman':
            max_frame = 4
        elif self.character.job == 'Archer':
            max_frame = 14
        elif self.character.job == 'Wizard':
            max_frame = 4

        # 프레임을 먼저 증가시키고
        self.character.frame = (self.character.frame + 1)
        # 최대 프레임에 도달하면 상태 전환
        if self.character.frame >= max_frame:
            self.character.state_machine.handle_state_event(('FINISH', None))
    def draw(self):
        if self.character.direction_x == 1:  # right
            self.character.image.clip_draw(self.character.frame * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(self.character.frame * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)

class hurt:
    def __init__(self, character):
        self.character = character
    def enter(self, e):
        self.character.frame = 0
        self.character.image = load_image(f'{self.character.job}/Hurt.png')
        pass

    def exit(self, e):
        pass

    def do(self):
        max_frame = 0
        if self.character.job == 'Swordsman':
            max_frame = 3
        elif self.character.job == 'Archer':
            max_frame = 3
        elif self.character.job == 'Wizard':
            max_frame = 4
        self.character.frame = (self.character.frame + 1)
        # 최대 프레임에 도달하면 상태 전환
        if self.character.frame >= max_frame:
            self.character.state_machine.handle_state_event(('FINISH', None))
    def draw(self):
        if self.character.direction_x == 1:  # right
            self.character.image.clip_draw(self.character.frame * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(self.character.frame * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)

class dead:
    def __init__(self, character):
        self.character = character

    def enter(self, e):
        self.character.image = load_image(f'{self.character.job}/Dead.png')

    def exit(self, e):
        exit(1)

    def do(self):
        pass
    def draw(self):
        if self.character.direction_x == 1:  # right
            self.character.image.clip_draw(self.character.frame * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(self.character.frame * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)

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
                                space_down: self.JUMP, c_down: self.RUN, x_down: self.ATTACK, z_down: self.ATTACK},
                    self.RUN: {space_down: self.JUMP, right_up: self.IDLE, left_up: self.IDLE, ctrl_down: self.ATTACK},
                    self.JUMP: {action_finish: self.IDLE},
                    self.ATTACK: {action_finish: self.IDLE},
                    self.HURT: {action_finish: self.IDLE},
                }
            )
        else:
            self.state_machine = StateMachine(
                self.IDLE,
                {
                    self.IDLE: {right_down : self.RUN, left_down: self.RUN, ctrl_down: self.ATTACK, space_down: self.JUMP, c_down: self.ATTACK, x_down: self.ATTACK, z_down: self.ATTACK},
                    self.RUN: {space_down: self.JUMP, right_up: self.IDLE, left_up: self.IDLE, ctrl_down: self.ATTACK},
                    self.JUMP: {action_finish : self.IDLE},
                    self.ATTACK: {action_finish : self.IDLE},
                    self.HURT: {action_finish : self.IDLE},
                }
            )
        pass
    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def Skill_1(self):
        skill1 = skill_1(self.x, self.y, 1, self.job)
        game_world.add_object(skill1, 1)
    def Skill_2(self):
        skill2 = skill_2(self.x, self.y, 1, self.job)
        game_world.add_object(skill2, 1)
    def Skill_3(self):
        skill3 = skill_3(self.x, self.y, 1, self.job)
        game_world.add_object(skill3, 1)