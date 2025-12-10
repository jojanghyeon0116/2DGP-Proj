from pico2d import *
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
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
    def update(self):
        if self.type == 0:
            self.frame_x = (self.frame_x + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 5
            self.frame_y = 640
    def draw(self):
        self.image.clip_draw(int(self.frame_x) * 288, self.frame_y, 288, 160, 400, 380, 500, 500)

    def get_bb(self):
        pass

    def handle_collision(self):
        pass

