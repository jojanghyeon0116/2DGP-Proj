from pico2d import load_image

class Ground:
    def __init__(self):
        self.image = load_image('background/background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(1024 // 2, 800 // 2)

