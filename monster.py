import random
import game_framework
from pico2d import load_image

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Monster:
    image = None
    def __init__(self, characters_obj):
        self.x, self.y = random.randint(50, 750), 400
        self.frame = 0
        self.attacking = False
        self.walking = False
        self.direction = 0
        self.target = characters_obj
        self.max_frame = 7
        if self.image is None:
            self.image = load_image('Skeleton/Idle.png')
        pass

    def update(self):
        self.frame = (self.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 7
        distance_x = self.target.x - self.x
        if distance_x > 0:
            self.direction = 1
        elif distance_x < 0:
            self.direction = -1

        if abs(distance_x) < 100 and not self.walking and not self.attacking:
            self.walking = True
            self.image = load_image('Skeleton/Run.png')
        elif abs(distance_x) >= 100 and self.walking:
            self.walking = False
            self.image = load_image('Skeleton/Idle.png')

        if abs(distance_x) < 100 and self.walking:
            self.x += self.direction * RUN_SPEED_PPS * game_framework.frame_time

        if abs(distance_x) < 50 and not self.attacking:
            self.attacking = True
            self.walking = False
            self.image = load_image('Skeleton/Attack_1.png')
        elif abs(distance_x) >= 50 and self.attacking:
            self.attacking = False
            self.image = load_image('Skeleton/Run.png')
        pass

    def draw(self):
        if self.direction == 1:
            self.image.clip_draw(int(self.frame) * 128, 0, 128, 128, self.x, self.y)
        elif self.direction == -1:
            self.image.clip_composite_draw(int(self.frame) * 128, 0, 128, 128, 0, 'h', self.x, self.y, 128, 128)
        pass
