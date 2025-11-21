from pico2d import *
import game_framework


class HealthBar:
    def __init__(self, character):
        self.character = character
        self.max_hp = character.hp

        self.fill_image = load_image('UI/health_bar_fill.png')  # 채워진 게이지 이미지

        self.x = 200
        self.y = get_canvas_height() - 50
        self.width = 300
        self.height = 20

        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        pass

    def draw(self):
        current_ratio = self.character.hp / self.max_hp

        text_content = f'{int(self.character.hp)} / {int(self.max_hp)}'
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