from pico2d import load_image
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 2.5  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Item:
    image = None
    def __init__(self, item_type):
        self.x = 600
        self.y = 300
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
        self.image.draw(self.x, self.y)
        pass
