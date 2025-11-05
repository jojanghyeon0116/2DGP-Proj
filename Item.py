from pico2d import load_image

class item:
    image = None
    def __init__(self, item_type):
        self.x = 600
        self.y = 300
        self.type = item_type
        if self.type == 0:
            self.image = load_image('item/item1.png')
    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        pass
