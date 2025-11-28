from pico2d import *
import game_framework


class HealthBar:
    def __init__(self, character):
        self.character = character

        self.fill_image = load_image('UI/health_bar_fill.png')  # 채워진 게이지 이미지

        self.x = 200
        self.y = get_canvas_height() - 50
        self.width = 300
        self.height = 20

        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        pass

    def draw(self):
        max_hp_value = self.character.max_hp
        current_ratio = self.character.hp / max_hp_value

        # 🌟 텍스트 표시에도 max_hp_value 사용
        text_content = f'{int(self.character.hp)} / {int(max_hp_value)}'
        text_color = (255, 255, 255)

        current_fill_width = int(self.width * current_ratio)


        sx = 0
        sy = 0
        sw = int(self.fill_image.w * current_ratio)
        sh = self.fill_image.h

        self.fill_image.clip_draw_to_origin(
            sx, sy, sw, sh,
            0, 750,
            current_fill_width, self.height
        )
        self.font.draw(100, 760, text_content, text_color)

class Skill_icon1:
    def __init__(self, character):
        self.character = character
        self.image = load_image(f'{self.character.job}/Skill_icon1.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 50, 50, 50)

class Skill_icon2:
    def __init__(self, character):
        self.character = character
        self.image = load_image(f'{self.character.job}/Skill_icon2.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(500, 50, 50, 50)

class Skill_icon3:
    def __init__(self, character):
        self.character = character
        self.image = load_image(f'{self.character.job}/Skill_icon3.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(600, 50, 50, 50)

class MoneyDisplay:
    def __init__(self, character):
        self.character = character
        self.font = load_font('ENCR10B.TTF', 16)
        self.x = 80  # 좌측 하단에 가까운 X 위치
        self.y = 50   # 좌측 하단에 가까운 Y 위치

        self.image = load_image('item/item2.png')

    def update(self):
        pass

    def draw(self):
        # 텍스트 내용: 현재 돈(money)
        text_content = f'{self.character.money}'
        text_color = (255, 255, 0) # 돈은 눈에 잘 띄게 노란색으로 설정
        self.image.draw(50, 50, 32, 32)
        self.font.draw(self.x, self.y, text_content, text_color)

class Level:
    def __init__(self, character):
        self.character = character
        self.background_image = load_image('UI/exp_bar_background.png')
        self.fill_image = load_image('UI/exp_bar.png')
        self.x = 30
        self.y = 20
        self.width = 300
        self.height = 20

        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        pass

    def draw(self):
        text_content = f'Lv : {self.character.level}'
        text_color = (255, 255, 255)
        self.font.draw(self.x, self.y, text_content, text_color)

        max_exp_value = self.character.max_exp # 최대 경험치
        current_ratio = self.character.exp / max_exp_value # 현재 경험치 비율

        self.background_image.draw_to_origin(self.x - 20, self.y, self.width, self.height)

        current_fill_width = int(self.width * current_ratio)

        self.fill_image.clip_draw_to_origin(
            0, 0,
            int(self.fill_image.w * current_ratio), self.fill_image.h,
            self.x - 20, self.y,
            current_fill_width, self.height
        )

        text_content = f'EXP: {int(self.character.exp)} / {int(max_exp_value)}'
        text_color = (255, 255, 255)
        self.font.draw(self.x + 80, self.y, text_content, text_color)