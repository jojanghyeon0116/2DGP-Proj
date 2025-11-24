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