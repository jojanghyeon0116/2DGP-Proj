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
    IMAGE_IDLE = None
    IMAGE_RUN = None
    IMAGE_ATTACK = None
    IMAGE_HURT = None
    IMAGE_DEAD = None
    hp_fill_image = None
    hp_back_image = None
    HP_BAR_WIDTH = 80
    HP_BAR_HEIGHT = 10
    HP_BAR_OFFSET_Y = 15

    def __init__(self, characters_obj):
        self.x, self.y = 600, 220
        self.frame = 0
        self.attacking = False
        self.walking = False
        self.direction = 0
        self.target = characters_obj
        self.max_frame = 7
        self.hp = 100
        self.max_hp = 100
        self.hit = False
        self.knockback_timer = 0.0
        if Monster.hp_fill_image is None:
            Monster.hp_fill_image = load_image('UI/health_bar_fill.png')
        if Monster.IMAGE_IDLE is None:
            Monster.IMAGE_IDLE = load_image('Skeleton/Idle.png')
            Monster.IMAGE_RUN = load_image('Skeleton/Run.png')
            Monster.IMAGE_ATTACK = load_image('Skeleton/Attack_1.png')
            Monster.IMAGE_HURT = load_image('Skeleton/Hurt.png')
            Monster.IMAGE_DEAD = load_image('Skeleton/Dead.png')
            Monster.hp_fill_image = load_image('UI/health_bar_fill.png')
        self.image = Monster.IMAGE_IDLE
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
                return
        elif self.hit:
            self.x += self.direction * RUN_SPEED_PPS * game_framework.frame_time * 2

            if int(self.frame) >= 3:
                self.hit = False
                self.frame = 0
                self.attacking = False
                self.walking = False
                self.image = Monster.IMAGE_IDLE
                return
        else:
            if distance_x_screen > 0:
                self.direction = 1
            elif distance_x_screen < 0:
                self.direction = -1

            if abs(distance_x_screen) < 100:
                if abs(distance_x_screen) < 50 and not self.attacking:
                    self.attacking = True
                    self.walking = False
                    self.frame = 0
                    self.image = Monster.IMAGE_ATTACK
                elif abs(distance_x_screen) >= 50 and self.attacking:
                    self.attacking = False
                    if abs(distance_x_screen) >= 100:
                        self.walking = False
                        self.frame = 0
                        self.image = Monster.IMAGE_IDLE
                    else:
                        self.walking = True
                        self.frame = 0
                        self.image = Monster.IMAGE_RUN
                elif not self.walking and not self.attacking:
                    self.walking = True
                    self.frame = 0
                    self.image = Monster.IMAGE_RUN
                if self.walking:
                    self.x += self.direction * RUN_SPEED_PPS * game_framework.frame_time
            else:
                self.frame = 0
                self.walking = False
                self.attacking = False
                self.image = Monster.IMAGE_IDLE

    def draw(self):
        global camera_offset_x
        screen_x = self.x - camera_offset_x
        if self.direction == 1:
            self.image.clip_draw(int(self.frame) * 128, 0, 128, 128, screen_x, self.y)
        elif self.direction == -1:
            self.image.clip_composite_draw(int(self.frame) * 128, 0, 128, 128, 0, 'h', screen_x, self.y, 128, 128)

        draw_rectangle(screen_x - 32, self.y - 64, screen_x + 32, self.y + 10)

        if self.hp > 0 and self.hp < self.max_hp:
            hp_bar_center_x = screen_x
            hp_bar_center_y = self.y + self.HP_BAR_OFFSET_Y
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
    def get_bb(self, offset_x=None):
        global camera_offset_x
        screen_x = self.x - camera_offset_x
        return screen_x - 32, self.y - 64, screen_x + 32, self.y + 10

    def handle_collision(self, group, other):
        if group == 'character:monster':
            if self.attacking:
                other.handle_collision('character:monster', self)
        elif group == 'hitbox:monster':
            self.direction = other.direction_x
            if not other.damage_dealt:
                other.damage_dealt = True
                self.frame = 0
                self.hit = True
                self.knockback_timer = 0.2
                self.image = Monster.IMAGE_HURT
                self.hp -= other.damage
                if self.hp <= 0:
                    self.image = Monster.IMAGE_DEAD

        elif group == 'skill:monster':
            self.hit = True
            self.direction = other.velocity
            self.knockback_timer = 0.2
            self.frame = 0
            self.image = Monster.IMAGE_HURT
            self.hp -= other.damage
            if self.hp <= 0:
                self.image = Monster.IMAGE_DEAD
        elif group == 'projectile:monster':
            self.direction = other.direction_x
            self.hit = True
            self.knockback_timer = 0.2
            self.frame = 0
            self.image = Monster.IMAGE_HURT
            self.hp -= other.damage
            if self.hp <= 0:
                self.image = Monster.IMAGE_DEAD