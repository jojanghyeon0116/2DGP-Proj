from pico2d import *
import common
import game_framework
import game_world

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 2.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class attack_range:
    # 히트박스의 크기 설정
    ATTACK_WIDTH = 150
    ATTACK_HEIGHT = 250

    def __init__(self, x, y, direction):
        self.x, self.y = x, y
        self.direction = direction
        self.offset_x = 120 * self.direction

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        left = self.x + self.offset_x - (self.ATTACK_WIDTH / 2)
        right = self.x + self.offset_x + (self.ATTACK_WIDTH / 2)
        bottom = self.y - 250
        top = self.y  # 보스 몸통의 중앙 높이

        return left, bottom, right, top

    def handle_collision(self, group, other):
        pass


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

        self.attack_object = None

    def update(self):
        if self.type == 2:
            if self.attack_object is None and self.frame_x > 0:
                self.attack_object = attack_range(self.x, self.y, self.direction)
                game_world.add_object(self.attack_object, 0)

            # 공격 애니메이션이 끝났을 때 공격 객체 제거 (예: 16프레임 이후)
            if int(self.frame_x) >= 15:
                if self.attack_object is not None:
                    game_world.remove_object(self.attack_object)
                    self.attack_object = None
                    self.type = 0
                    self.frame_x = 0

        distance = self.x - common.character.x

        if self.type != 2:
            if abs(distance) < 200:
                if abs(distance) < 100:
                    self.type = 2
                    self.frame_x = 0
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
        if self.type == 1:
            self.frame_x = (self.frame_x + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 9
            self.frame_y = 480
        elif self.type == 2:
            self.frame_x = self.frame_x + self.max_frame * ACTION_PER_TIME * game_framework.frame_time
            self.frame_y = 320
        elif self.type == 3:
            self.frame_x = (self.frame_x + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 5
            self.frame_y = 160

    def draw(self):
        current_frame = int(self.frame_x)

        if self.direction == 0 or self.direction == -1:
            self.image.clip_draw(current_frame * 288, self.frame_y, 288, 160, self.x, self.y, 500, 500)
        else:
            self.image.clip_composite_draw(current_frame * 288, self.frame_y, 288, 160, 0, 'h', self.x, self.y, 500,
                                           500)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 250, self.x + 50, self.y

    def handle_collision(self, group, other):
        if group == 'character:boss':
            pass