from pico2d import load_image, draw_rectangle
import game_framework
import game_world


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 2.5  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class item:
    image = None
    camera_offset_x = 0
    screen_x = 0
    def __init__(self, item_type, x = 200, y = 350):
        self.x = x
        self.y = y
        self.type = item_type
        self.direction = 0.5
        self.max_move = 0
        if self.type == 0:
            self.image = load_image('item/item1.png')
        elif self.type == 1:
            self.image = load_image('item/item2.png')
        elif self.type == 2:
            self.image = load_image('item/item3.png')
        elif self.type == 3:
            self.image = load_image('item/item4.png')
        elif self.type == 4:
            self.image = load_image('item/item5.png')
    def update(self):
        self.y = self.y + RUN_SPEED_PPS * self.direction * game_framework.frame_time
        self.max_move += RUN_SPEED_PPS * self.direction * game_framework.frame_time
        if abs(self.max_move) >= 6.0:
            self.direction = -self.direction
            self.max_move = 0


    def draw(self):
        item.screen_x = self.x - item.camera_offset_x
        self.image.draw(item.screen_x, self.y, 32, 32)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return item.screen_x - 16, self.y - 16, item.screen_x + 16, self.y + 16

    def handle_collision(self, group, other):
        if group == 'character:item':
            if self.type == 0:
                other.hp += 20
                print(f'Hp : {other.hp}')
            elif self.type == 1:
                other.money += 100
                print(f'Money : {other.money}')
            elif self.type == 2:
                other.exp += 10
                print(f'Exp : {other.exp}')
            elif self.type == 3:
                other.attack_damage += 5
            elif self.type == 4:
                other.speed += 1
            game_world.remove_object(self)
