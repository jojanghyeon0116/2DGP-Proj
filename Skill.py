from pico2d import *
import game_world
from game_world import *
import game_framework


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class skill_1:
    def __init__(self, x = 400, y = 300, velocity = 1, job = 'Swordsman', speed = 1):
        self.job = job
        self.image = load_image(f'{self.job}/skill1.png')
        self.x, self.y, self.velocity = x, y - 20, velocity
        self.frame = 0
        self.damage = 30
        self.max_distance = 0
        self.active = True
        self.speed = speed
        if self.job == 'Swordsman':
            self.x = self.x + 50 * self.velocity
            self.max_frame = 3
        elif self.job == 'Wizard':
            self.max_frame = 3
        elif self.job == 'Archer':
            self.max_frame = 4
    def update(self):
        if self.job == 'Swordsman':
            self.frame = (self.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 3
            self.x += self.velocity * RUN_SPEED_PPS * game_framework.frame_time * self.speed
            self.max_distance += self.velocity * RUN_SPEED_PPS * game_framework.frame_time
            if abs(self.max_distance) >= 100:
                if self.active:
                    self.active = False
                    game_world.remove_object(self)
        elif self.job == 'Wizard':
            self.frame = (self.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 3
            self.x += self.velocity * RUN_SPEED_PPS * game_framework.frame_time
        elif self.job == 'Archer':
            self.frame = (self.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 4
            self.x += self.velocity * RUN_SPEED_PPS * game_framework.frame_time
        if self.x < 0 or self.x > 1024:
            if self.active:
                self.active = False
                game_world.remove_object(self)

    def draw(self):
        if self.job == 'Swordsman':
            if self.velocity > 0:
                self.image.clip_draw(int(self.frame) * 34, 0, 34, 128, self.x, self.y, 50, 100)
            elif self.velocity < 0:
                self.image.clip_composite_draw(int(self.frame) * 34, 0, 34, 128, 0, 'h', self.x, self.y, 50, 100)
        elif self.job == 'Wizard':
            if self.velocity > 0:
                self.image.clip_draw(int(self.frame) * 34, 0, 34, 36, self.x, self.y, 30, 30)
            elif self.velocity < 0:
                self.image.clip_composite_draw(int(self.frame) * 34, 0, 34, 36, 0, 'h', self.x, self.y, 30, 30)
        elif self.job == 'Archer':
            if self.velocity > 0:
                self.image.clip_draw(int(self.frame) * 33, 0, 33, 32, self.x, self.y, 50, 50)
            elif self.velocity < 0:
                self.image.clip_composite_draw(int(self.frame) * 33, 0, 33, 32, 0, 'h', self.x, self.y, 50, 50)
    def get_bb(self):
        return self.x - 16, self.y - 16, self.x + 16 , self.y + 16

    def handle_collision(self, group, other):
        if group == 'skill:monster':
            if self.active:
                self.active = False
                game_world.remove_object(self)

class skill_2:
    def __init__(self, x = 400, y = 300, velocity = 1, job = 'Swordsman'):
        self.job = job
        self.image = load_image(f'{self.job}/skill2.png')
        self.x, self.y, self.velocity = x, y - 20, velocity
        self.damage = 30
        self.active = True
        self.frame = 0
        if self.job == 'Swordsman':
            self.max_frame = 5
            self.y = y + 30
        elif self.job == 'Wizard':
            self.max_frame = 3
        elif self.job == 'Archer':
            self.max_frame = 6
    def update(self):
        if self.job == 'Swordsman':
            self.frame = self.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time
            if self.frame >= self.max_frame:
                if self.active:
                    self.active = False
                    game_world.remove_object(self)
        elif self.job == 'Wizard':
            self.frame = (self.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 3
            self.x += self.velocity * RUN_SPEED_PPS * game_framework.frame_time
        elif self.job == 'Archer':
            self.frame = (self.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 6
            self.x += self.velocity * RUN_SPEED_PPS * game_framework.frame_time
        if self.x < 0 or self.x > 1024:
            if self.active:
                self.active = False
                game_world.remove_object(self)

    def draw(self):
        if self.job == 'Swordsman':
            self.image.clip_draw(0, int(self.frame) * 200, 250, 200, self.x, self.y, 75, 75)
        elif self.job == 'Wizard':
            if self.velocity > 0:
                self.image.clip_draw(int(self.frame) * 341, 0, 341, 284, self.x, self.y, 50, 50)
            elif self.velocity < 0:
                self.image.clip_composite_draw(int(self.frame) * 341, 0, 341, 284, 0, 'h', self.x, self.y, 50, 50)
        elif self.job == 'Archer':
            if self.velocity > 0:
                self.image.clip_draw(int(self.frame) * 170, 0, 170, 290, self.x, self.y, 100, 100)
            elif self.velocity < 0:
                self.image.clip_composite_draw(int(self.frame) * 170, 0, 170, 290, 0, 'h', self.x, self.y, 100, 100)

    def get_bb(self):
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16

    def handle_collision(self, group, other):
        if group == 'skill:monster':
            if self.active:
                self.active = False
                game_world.remove_object(self)

class skill_3:
    def __init__(self, x = 400, y = 300, velocity = 1, job = 'Swordsman'):
        self.job = job
        self.image = load_image(f'{self.job}/skill3.png')
        self.x, self.y, self.velocity = x, y - 20, velocity
        self.frame = 0
        self.damage = 30
        self.active = True
        if self.job == 'Swordsman':
            self.max_frame = 4
        elif self.job == 'Wizard':
            self.max_frame = 3
        elif self.job == 'Archer':
            self.max_frame = 6
    def update(self):
        self.x += self.velocity * RUN_SPEED_PPS * game_framework.frame_time
        if self.job == 'Swordsman':
            self.frame = (self.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 4
        elif self.job == 'Wizard':
            self.frame = (self.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 3
        elif self.job == 'Archer':
            self.frame = (self.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 6
        if self.x < 0 or self.x > 1024:
            if self.active:
                self.active = False
                game_world.remove_object(self)
    def draw(self):
        if self.job == 'Swordsman':
            if self.velocity > 0:
                self.image.clip_draw(int(self.frame) * 34, 0, 34, 35, self.x, self.y, 40, 40)
            elif self.velocity < 0:
                self.image.clip_composite_draw(int(self.frame) * 34, 0, 34, 35, 0, 'h', self.x, self.y, 40, 40)
        elif self.job == 'Wizard':
            if self.velocity > 0:
                self.image.clip_draw(int(self.frame) * 341, 0, 341, 284, self.x, self.y, 70, 70)
            elif self.velocity < 0:
                self.image.clip_composite_draw(int(self.frame) * 341, 0, 341, 284, 0, 'h', self.x, self.y, 70, 70)
        elif self.job == 'Archer':
            if self.velocity > 0:
                self.image.clip_draw(int(self.frame) * 170, 0, 170, 200, self.x, self.y, 70, 70)
            elif self.velocity < 0:
                self.image.clip_composite_draw(int(self.frame) * 170, 0, 170, 200, 0, 'h', self.x, self.y, 70, 70)

    def get_bb(self):
        return self.x - 16, self.y - 16, self.x + 16, self.y + 16
    def handle_collision(self, group, other):
        if group == 'skill:monster':
            if self.active:
                self.active = False
                game_world.remove_object(self)



