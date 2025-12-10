from pico2d import *
import common
import game_framework
import game_world
import Game_clear

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 2.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


class attack_range:
    ATTACK_WIDTH = 150
    ATTACK_HEIGHT = 250
    def __init__(self, x, y, direction):
        self.x, self.y = x, y
        self.direction = direction
        self.offset_x = 120 * self.direction
        self.damage = False
        game_world.add_collision_pair('character:attack', None, self)
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
        if group == 'character:attack':
            if not self.damage:
                other.hp -= 50
                self.damage = True


class Boss:
    image = None
    hp_fill_image = None
    hp_back_image = None
    HP_BAR_WIDTH = 500
    HP_BAR_HEIGHT = 20
    Skill_cooldown = 3.0
    def __init__(self):
        self.image = load_image('boss/boss_sprite.png')
        self.frame_x = 0
        self.frame_y = 0
        self.max_frame = 22
        self.type = 0
        self.frame = 0
        self.x = 600
        self.y = 380
        self.direction = 1
        self.hp = 500
        self.max_hp = 500
        self.attack_object = None
        self.game_clear = False
        if Boss.hp_fill_image is None:
            Boss.hp_fill_image = load_image('UI/health_bar_fill.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.skill = None
        self.skill_timer = 0.0
        self.is_using_skill = False
    def update(self):
        if not self.game_clear and not self.is_using_skill and self.type == 0:
            self.skill_timer += game_framework.frame_time

            if self.skill_timer >= self.Skill_cooldown:
                self.is_using_skill = True
                self.type = 5
                self.frame_x = 0
                self.skill_timer = 0.0
        if not self.game_clear:
            if self.type == 2:
                if self.attack_object is None and self.frame_x >= 10:
                    self.attack_object = attack_range(self.x, self.y, self.direction)
                    game_world.add_object(self.attack_object, 0)

                if int(self.frame_x) >= 11:
                    if self.attack_object is not None:
                        game_world.remove_object(self.attack_object)
                        self.attack_object = None
                        self.type = 0
                        self.frame_x = 0
            if self.attack_object is not None and self.type != 2:
                game_world.remove_object(self.attack_object)
                self.attack_object = None
            distance = self.x - common.character.x
            if self.type != 2 and self.type != 3 and self.type != 5:
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
            self.frame_x = self.frame_x + self.max_frame * ACTION_PER_TIME * game_framework.frame_time
            self.frame_y = 160
            if int(self.frame_x) >= 5:
                self.type = 0
                self.frame_x = 0
        elif self.type == 4:
            self.frame_x = self.frame_x + self.max_frame * ACTION_PER_TIME * game_framework.frame_time
            self.frame_y = 0
            if int(self.frame_x) >= 22:
                game_world.remove_object(self)
                game_framework.push_mode(Game_clear)
        elif self.type == 5:
            self.frame_x = self.frame_x + self.max_frame * ACTION_PER_TIME * game_framework.frame_time
            self.frame_y = 320
            if int(self.frame_x) >= 10 and self.skill is None:
                self.skill = fire_skill(self.x, self.y, self.direction)
                game_world.add_object(self.skill, 1)
                game_world.add_collision_pair('character:boss_skill', None, self.skill)
            if int(self.frame_x) >= 11:
                self.type = 0
                self.frame_x = 0
                self.is_using_skill = False
                self.skill = None
    def draw(self):
        current_frame = int(self.frame_x)

        if self.direction == 0 or self.direction == -1:
            self.image.clip_draw(current_frame * 288, self.frame_y, 288, 160, self.x, self.y, 500, 500)
        else:
            self.image.clip_composite_draw(current_frame * 288, self.frame_y, 288, 160, 0, 'h', self.x, self.y, 500,
                                           500)
        draw_rectangle(*self.get_bb())
        if self.hp > 0:
            hp_bar_center_x = 512
            hp_bar_center_y = 700
            hp_ratio = self.hp / self.max_hp

            pico2d.draw_rectangle(
                hp_bar_center_x - self.HP_BAR_WIDTH / 2,
                hp_bar_center_y - self.HP_BAR_HEIGHT / 2,
                hp_bar_center_x + self.HP_BAR_WIDTH / 2,
                hp_bar_center_y + self.HP_BAR_HEIGHT / 2
            )

            fill_width = self.HP_BAR_WIDTH * hp_ratio
            fill_x = hp_bar_center_x - (self.HP_BAR_WIDTH - fill_width) / 2

            self.hp_fill_image.clip_draw(
                0, 0, self.hp_fill_image.w, self.hp_fill_image.h,
                fill_x, hp_bar_center_y,
                fill_width, self.HP_BAR_HEIGHT
            )
            self.font.draw(hp_bar_center_x - 50, hp_bar_center_y, f'{self.hp} / {self.max_hp}', (255, 255, 255))
            self.font.draw(hp_bar_center_x - 25, hp_bar_center_y + 20, f'Boss', (255, 255, 255))
    def get_bb(self):
        return self.x - 50, self.y - 250, self.x + 50, self.y

    def handle_collision(self, group, other):
        if group == 'boss:skill' or group == 'boss:hitbox':
            game_world.remove_object(other)
            self.type = 3
            self.frame_x = 0
            self.hp -= other.damage
            if self.hp <= 0:
                self.type = 4
                self.frame_x = 0
                self.game_clear = True

class fire_skill:
    image = None
    def __init__(self, x, y, direction):
        self.x, self.y = x + 50, 180
        self.direction = direction
        self.damage = False
        self.frame_x = 0
        self.max_frame = 8
        if fire_skill.image is None:
            self.image = load_image('boss/boss_skill.png')

    def update(self):
        self.frame_x = (self.frame_x + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.x += self.direction * RUN_SPEED_PPS * game_framework.frame_time * 2
        if self.x > 1024 or self.x < 0:
            game_world.remove_object(self)
            return
    def draw(self):
        self.image.clip_draw(int(self.frame_x) * 128, 0, 128, 1024, self.x, self.y, 100, 200)
        draw_rectangle(*self.get_bb())
    def get_bb(self):
        return self.x - 25, self.y - 50, self.x + 25, self.y + 15

    def handle_collision(self, group, other):
        if group == 'character:boss_skill':
            other.hp -= 10
            game_world.remove_object(self)