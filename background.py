from pico2d import *
import Character

from pico2d import *
import Character


class Ground:
    def __init__(self, character):
        self.image = load_image('background/background.png')
        self.character = character

        # 🌟 추가: 배경 이미지 너비와 화면 너비를 저장합니다.
        self.bg_width = self.image.w  # 로드된 이미지의 실제 너비
        self.screen_width = 1024  # 캔버스 너비 (코드에서 사용된 값)
        self.screen_height = 800  # 캔버스 높이 (코드에서 사용된 값)

    def update(self):
        pass

    def draw(self):
        # 1. 캐릭터 위치를 기반으로 배경 이미지의 원본 중심 x 좌표를 계산합니다.
        # 이 값은 아직 제한되지 않은 상태의 화면 좌표입니다.
        # (self.character.x - 400) : 캐릭터가 월드에서 이동한 거리 (카메라 오프셋)
        raw_screen_x = (self.screen_width // 2) - (self.character.x - 400)

        # 2. 배경 이미지의 너비가 화면 너비보다 작거나 같을 경우, 배경을 중앙에 고정합니다.
        if self.bg_width <= self.screen_width:
            final_screen_x = self.screen_width // 2
        else:
            # 3. 배경 스크롤의 최소/최대 화면 좌표를 계산하여 클램핑(Clamp)합니다.
            half_bg_width = self.bg_width / 2.0

            # 최소 screen_x (Min): 배경 이미지의 오른쪽 끝이 화면 오른쪽 끝(1024)에 닿을 때
            # 이 값보다 작아지면 화면 우측에 빈 공간이 생깁니다.
            min_screen_x = self.screen_width - half_bg_width

            # 최대 screen_x (Max): 배경 이미지의 왼쪽 끝이 화면 왼쪽 끝(0)에 닿을 때
            # 이 값보다 커지면 화면 좌측에 빈 공간이 생깁니다.
            max_screen_x = half_bg_width

            # 4. 계산된 raw_screen_x를 min_screen_x와 max_screen_x 범위 내로 제한합니다.
            final_screen_x = max(min_screen_x, raw_screen_x)
            final_screen_x = min(max_screen_x, final_screen_x)

        # 5. 제한된 좌표로 배경을 그립니다.
        self.image.draw(final_screen_x, self.screen_height // 2.0)


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