from pico2d import *
import Character


class Ground:
    def __init__(self, character):
        self.image = load_image('background/background.png')
        self.character = character
    def update(self):
        pass

    def draw(self):
        screen_x = (1024 // 2) - (self.character.x - 400)
        self.image.draw(screen_x, 800 // 2.0)


class Platform:
    def __init__(self, character, x, y):
        self.image = load_image('background/background2.png')
        self.character = character  # 🌟 캐릭터 참조 저장
        self.world_x = x  # 🌟 월드 좌표를 저장
        self.world_y = y

    def update(self):
        pass

    def draw(self):
        screen_x = self.world_x - (self.character.x - 400)
        self.image.draw(screen_x, self.world_y, 100, 100)
        draw_rectangle(*self.get_bb())

    def get_bb(self, screen_x=None):
        if screen_x is None:  # 화면 BB를 구할 때만 계산 (Draw에서 사용)
            screen_x = self.world_x - (self.character.x - 400)
            # y 좌표는 변하지 않는다고 가정
        screen_y = self.world_y

        return screen_x - 40, screen_y - 25, screen_x + 40, screen_y + 25

    def handle_collision(self, group, other):
        pass