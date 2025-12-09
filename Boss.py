from pico2d import *


class Boss:
    image = None

    def __init__(self):
        self.image = load_image('boss/boss_sprite.png')

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 640, 288, 160, 400, 380, 500, 500)

    def get_bb(self):
        pass

    def handle_collision(self):
        pass

