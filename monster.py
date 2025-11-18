import random
import game_framework
from pico2d import *
import game_world
import Item

camera_offset_x = 0

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Monster:
    image = None
    def __init__(self, characters_obj):
        self.x, self.y = 600, 220
        self.frame = 0
        self.attacking = False
        self.walking = False
        self.direction = 0
        self.target = characters_obj
        self.max_frame = 7
        self.hp = 100
        self.hit = False
        self.knockback_timer = 0.0
        if self.image is None:
            self.image = load_image('Skeleton/Idle.png')
        pass

    def update(self):
        global camera_offset_x
        self.frame = (self.frame + self.max_frame * ACTION_PER_TIME * game_framework.frame_time) % 7
        monster_screen_x = self.x - camera_offset_x
        character_screen_x = self.target.x
        distance_x_screen = character_screen_x - monster_screen_x
        distance_x_world = self.target.x - self.x
        if self.hp <= 0:
            if int(self.frame) >= 3:
                new_item = Item.item(1, self.x - 10, self.y - 30)
                game_world.add_object(new_item, 1)
                game_world.add_collision_pair('character:item', None, new_item)
                new_item = Item.item(2, self.x + 10, self.y - 30)
                game_world.add_object(new_item, 1)
                game_world.add_collision_pair('character:item', None, new_item)

                new_item = Item.item(random.randint(0,4), self.x, self.y - 30)
                game_world.add_object(new_item, 1)
                game_world.add_collision_pair('character:item', None, new_item)
                game_world.remove_object(self)
        if self.hit:
            self.x += -self.direction * RUN_SPEED_PPS * game_framework.frame_time * 2

            if self.frame >= 3:
                self.hit = False
                self.image = load_image('Skeleton/Idle.png')

        else:
            if distance_x_world > 0:
                self.direction = 1
            elif distance_x_world < 0:
                self.direction = -1

                # 🏃 추적 시작/멈춤 판단: 화면 상의 거리를 사용합니다.
            if abs(distance_x_screen) < 100 and not self.walking and not self.attacking:
                self.walking = True
                self.image = load_image('Skeleton/Run.png')
            elif abs(distance_x_screen) >= 100 and self.walking:
                self.walking = False
                self.image = load_image('Skeleton/Idle.png')

                # 🏃 몬스터 이동: 월드 좌표(self.x)를 변경하여 이동합니다.
                # 몬스터의 이동 방향은 distance_x_world를 따릅니다.
            if abs(distance_x_screen) < 100 and self.walking:
                self.x += self.direction * RUN_SPEED_PPS * game_framework.frame_time

                # ⚔️ 공격 시작 판단: 화면 상의 거리를 사용합니다.
            if abs(distance_x_screen) < 50 and not self.attacking:
                self.attacking = True
                self.walking = False
                self.image = load_image('Skeleton/Attack_1.png')
            elif abs(distance_x_screen) >= 50 and self.attacking:
                self.attacking = False
                # 공격 후 상태 전환
                if abs(distance_x_screen) >= 100:
                    self.walking = False
                    self.image = load_image('Skeleton/Idle.png')
                else:
                    self.walking = True
                    self.image = load_image('Skeleton/Run.png')

    def draw(self):
        global camera_offset_x
        screen_x = self.x - camera_offset_x
        if self.direction == 1:
            # 화면 좌표 (screen_x)를 사용
            self.image.clip_draw(int(self.frame) * 128, 0, 128, 128, screen_x, self.y)
        elif self.direction == -1:
            # 화면 좌표 (screen_x)를 사용
            self.image.clip_composite_draw(int(self.frame) * 128, 0, 128, 128, 0, 'h', screen_x, self.y, 128, 128)
        draw_rectangle(screen_x - 32, self.y - 64, screen_x + 32, self.y + 10)

    def get_bb(self, offset_x=None):
        return self.x - 32, self.y - 64, self.x + 32, self.y + 10

    def handle_collision(self, group, other):
        if group == 'character:monster':
            pass
        elif group == 'hitbox:monster':
            if not other.damage_dealt:
                other.damage_dealt = True
                self.frame = 0
                self.hit = True
                self.knockback_timer = 0.2
                self.image = load_image('Skeleton/Hurt.png')
                self.hp -= other.damage
                if self.hp <= 0:
                    self.image = load_image('Skeleton/Dead.png')
                try:
                    game_world.remove_object(other)
                except Exception as e:
                    pass
        elif group == 'skill:monster':
            self.hit = True
            self.knockback_timer = 0.2
            self.frame = 0
            self.image = load_image('Skeleton/Hurt.png')
            self.hp -= other.damage
            if self.hp <= 0:
                self.image = load_image('Skeleton/Dead.png')
        elif group == 'projectile:monster':
            self.hit = True
            self.knockback_timer = 0.2
            self.frame = 0
            self.image = load_image('Skeleton/Hurt.png')
            self.hp -= other.damage
            if self.hp <= 0:
                self.image = load_image('Skeleton/Dead.png')