import pico2d


class Monster:
    image = None

    def __init__(self):
        self.image = load_image('boss/spritesheets')
        pass

    def update(self):
        pass
    def draw(self):
        pass

    def get_bb(self):
        pass

    def handle_collision(self):
        pass

