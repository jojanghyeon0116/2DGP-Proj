from pico2d import *



class Ground:
    def __init__(self):
        self.image = load_image('background/background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(1024 // 2, 800 // 2)


class Platform:
    def __init__(self):
        self.image = load_image('background/background2.png')
        self.x = 200
        self.y = 300

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 100, 100)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 40, self.y - 25, self.x + 40, self.y + 25

    def handle_collision(self, group, other):
        pass