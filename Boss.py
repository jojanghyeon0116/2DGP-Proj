from pico2d import *

import common
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 2.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

class Boss:
    image = None

    def __init__(self):
        self.image = load_image('boss/boss_sprite.png')
        self.frame_x = 0
        self.frame_y = 0
        self.max_frame = 22
        self.type = 0
        self.frame = 0
        self.x = 400
        self.y = 380
        self.direction = 0
    def update(self):
        distance = self.x - common.character.x
        if abs(distance) < 200:
            if abs(distance) < 100:
                self.type = 2
            else:
                self.type = 1
                self.x += self.direction * RUN_SPEED_PPS * game_framework.frame_time
            if distance < 0:
                self.direction = 1
            elif distance > 0:
                self.direction = -1
        else:
            self.type = 0

        if self.type == 0:
            self.frame_x = (self.frame_x + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 5
            self.frame_y = 640
        elif self.type == 1:
            self.frame_x = (self.frame_x + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 9
            self.frame_y = 480
        elif self.type == 2:
            self.frame_x = (self.frame_x + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 15
            self.frame_y = 320
        elif self.type == 3:
            self.frame_x = (self.frame_x + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 5
    def draw(self):
        if self.direction == 0 or self.direction == -1:
            self.image.clip_draw(int(self.frame_x) * 288, self.frame_y, 288, 160, self.x, self.y, 500, 500)
        else:
            self.image.clip_composite_draw(int(self.frame_x) * 288, self.frame_y, 288, 160, 0,'h',self.x, self.y, 500, 500)
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - 50, self.y - 250, self.x + 50, self.y

    def handle_collision(self, group, other):
        if group == 'character:boss':
            pass

