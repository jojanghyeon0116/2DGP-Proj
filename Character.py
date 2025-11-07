from pico2d import load_image

class Idle:

    def __init__(self, character):
        self.character = character
        self.character.image = load_image(f'{self.character.job}/Idle.png')
    def enter(self, e):
        pass

    def exit(self, e):
        pass


    def do(self):
        if self.character.job == 'Swordsman':
            self.character.frame = (self.character.frame + 1) % 8
        elif self.character.job == 'Archer':
            self.character.frame = (self.character.frame + 1) % 6
        elif self.character.job == 'Wizard':
            self.character.frame = (self.character.frame + 1) % 6

    def draw(self):
        if self.character.direction_x == 1: # right
            self.character.image.clip_draw(self.character.frame * 128, 0, 128, 128, self.character.x, self.character.y)
        else: # direction_x == -1: # left
            self.character.image.clip_draw(self.character.frame * 128, 0, 128, 128, self.character.x, self.character.y)

class run:
    def __init__(self, character):
        self.character = character
        self.character.image = load_image(f'{self.character.job}/Run.png')

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.character.frame = (self.character.frame + 1) % 8
    def draw(self):
        if self.character.direction_x == 1:  # right
            self.character.image.clip_draw(self.character.frame * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(self.character.frame * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)

class jump:
    def __init__(self, character):
        self.character = character
        self.character.image = load_image(f'{self.character.job}/Jump.png')

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.character.frame = (self.character.frame + 1) % 8
        self.character.y += self.character.direction_y * 10
        if self.character.y >= 440:  # 최고점 도달
            self.character.direction_y = -1  # 하강 시작
        if self.character.y <= 400:  # 바닥 도달
            self.character.y = 400
            self.character.direction_y = 0
            self.character.image = load_image(f'{self.character.job}/Idle.png')
            self.character.jumping = False  # 점프 종료
    def draw(self):
        if self.character.direction_x == 1:  # right
            self.character.image.clip_draw(self.character.frame * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(self.character.frame * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)


class attack:
    def __init__(self, character):
        self.character = character
        self.character.image = load_image(f'{self.character.job}/Attack.png')

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        if self.character.job == 'Swordsman':
            self.character.frame = (self.character.frame + 1) % 4
        elif self.character.job == 'Archer':
            self.character.frame = (self.character.frame + 1) % 14
        elif self.character.job == 'Wizard':
            self.character.frame = (self.character.frame + 1) % 4
    def draw(self):
        if self.character.direction_x == 1:  # right
            self.character.image.clip_draw(self.character.frame * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(self.character.frame * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)

class hurt:
    def __init__(self, character):
        self.character = character
        self.character.image = load_image(f'{self.character.job}/Hurt.png')

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        if self.character.job == 'Swordsman':
            self.character.frame = (self.character.frame + 1) % 3
        elif self.character.job == 'Archer':
            self.character.frame = (self.character.frame + 1) % 3
        elif self.character.job == 'Wizard':
            self.character.frame = (self.character.frame + 1) % 4
    def draw(self):
        if self.character.direction_x == 1:  # right
            self.character.image.clip_draw(self.character.frame * 128, 0, 128, 128, self.character.x, self.character.y)
        else:  # direction_x == -1: # left
            self.character.image.clip_composite_draw(self.character.frame * 128, 0, 128, 128, 0, 'h', self.character.x, self.character.y, 128, 128)

class Character:
    image = None
    def __init__(self, job):
        self.job = job
        self.x, self.y = 400, 400
        self.frame = 0
        self.direction_x = 0
        self.direction_y = 0
        self.direction = 0
        self.move = False
        self.jumping = False  # 점프 중인지 여부
        self.hurt = False
        self.attacking = False
        self.hp = 100
        self.cur_state = Idle(self)

        pass
    def update(self):
        if self.move:
            self.cur_state = run(self)
        elif self.jumping:
            self.cur_state = jump(self)
        elif self.attacking:
            self.cur_state = attack(self)
        elif self.hurt:
            self.cur_state = hurt(self)
        else:
            self.cur_state = Idle(self)
        self.cur_state.do()
        if self.attacking:
            # 캐릭터별 공격 프레임 수
            attack_frames = {'Swordsman': 4, 'Archer': 14, 'Wizard': 4}  # 예시 프레임 수, 실제 이미지에 맞게 조정 필요
            max_frames = attack_frames.get(self.job, 4)  # 기본값 4

            self.frame = (self.frame + 1)
            if self.frame >= max_frames:
                self.attacking = False  # 공격 애니메이션 종료
                self.frame = 0
                self.image = load_image(f'{self.job}/Idle.png')  # 대기 상태로 복귀

            # 공격 중에는 이동/점프/피격 애니메이션 업데이트를 스킵
            return
        if self.hp <= 0:
            self.image = load_image(f'{self.job}/Dead.png')
        if self.job == 'Swordsman':
            if self.hurt or self.hp <= 0:
                self.frame = (self.frame + 1) % 3
            # else:
            #     self.frame = (self.frame + 1) % 8
        elif self.job == 'Archer':
            if not self.move and not self.hurt:
                self.frame = (self.frame + 1) % 6
            elif self.hurt or self.hp <= 0:
                self.frame = (self.frame + 1) % 3
            else:
                self.frame = (self.frame + 1) % 8
        elif self.job == 'Wizard':
            if not self.move and not self.hurt:
                self.frame = (self.frame + 1) % 6
            elif self.hurt or self.hp <= 0:
                self.frame = (self.frame + 1) % 4
            else:
                self.frame = (self.frame + 1) % 8

        self.x += self.direction_x * 10
        pass

    def draw(self):
        self.cur_state.draw()
        # if self.direction_x == 1:
        #     self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y)
        # elif self.direction_x == -1:
        #     self.image.clip_composite_draw(self.frame * 128, 0, 128, 128, 0, 'h', self.x, self.y, 128, 128)
        # else:  # 정지 상태 (마지막 이동 방향에 따라)
        #     self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y)
        # pass
