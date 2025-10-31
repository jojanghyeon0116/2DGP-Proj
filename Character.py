from pico2d import load_image


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
        if Character.image is None and self.job == 'Swordsman':
            Character.image = load_image('Swordsman/Idle.png')
        elif Character.image is None and self.job == 'Archer':
            Character.image = load_image('Archer/Idle.png')
        elif Character.image is None and self.job == 'Wizard':
            Character.image = load_image('Wizard/Idle.png')

        pass
    def update(self):
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
            else:
                self.frame = (self.frame + 1) % 8
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
        if self.jumping:
            self.y += self.direction_y * 10
            if self.y >= 440:  # 최고점 도달
                self.direction_y = -1  # 하강 시작
            if self.y <= 400:  # 바닥 도달
                self.jumping = False
                self.y = 400
                self.direction_y = 0
                self.image = load_image(f'{self.job}/Idle.png')
                self.move = False
        pass

    def draw(self):
        if self.direction_x == 1:
            self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y)
        elif self.direction_x == -1:
            self.image.clip_composite_draw(self.frame * 128, 0, 128, 128, 0, 'h', self.x, self.y, 128, 128)
        else:  # 정지 상태 (마지막 이동 방향에 따라)
            self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y)
        pass
