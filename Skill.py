from pico2d import load_image

import game_world
from game_world import *
class skill_1:
    def __init__(self, x = 400, y = 300, velocity = 1, job = 'Swordsman'):
        self.job = job
        self.image = load_image(f'{self.job}/skill1.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
    def update(self):
        self.x += self.velocity * 5
        if self.job == 'Swordsman':
            self.frame = (self.frame + 1) % 3
        elif self.job == 'Wizard':
            self.frame = (self.frame + 1) % 3
            self.x += 10
        elif self.job == 'Archer':
            self.frame = (self.frame + 1) % 4
            self.x += 10
        if self.x < 25 or self.x > 800 - 25:
            game_world.remove_object(self)

    def draw(self):
        if self.job == 'Swordsman':
            self.image.clip_draw(self.frame * 34, 0, 34, 128, self.x, self.y)
        elif self.job == 'Wizard':
            self.image.clip_draw(self.frame * 34, 0, 34, 36, self.x, self.y, 30, 30)
        elif self.job == 'Archer':
            self.image.clip_draw(self.frame * 33, 0, 33, 32, self.x, self.y, 50, 50)

class skill_2:
    def __init__(self, x = 400, y = 300, velocity = 1, job = 'Swordsman'):
        self.job = job
        self.image = load_image(f'{self.job}/skill2.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0

    def update(self):
        if self.job == 'Swordsman':
            self.frame = self.frame + 1
            if self.frame >= 5:
                game_world.remove_object(self)
        elif self.job == 'Wizard':
            self.frame = (self.frame + 1) % 3
            self.x += self.velocity * 5
        elif self.job == 'Archer':
            self.frame = (self.frame + 1) % 6
            self.x += self.velocity * 5
        if self.x < 25 or self.x > 800 - 25:
            game_world.remove_object(self)

    def draw(self):
        if self.job == 'Swordsman':
            self.image.clip_draw(0, self.frame * 200, 250, 200, self.x, self.y, 75, 75)
        elif self.job == 'Wizard':
            self.image.clip_draw(self.frame * 341, 0, 341, 284, self.x, self.y, 50, 50)
        elif self.job == 'Archer':
            self.image.clip_draw(self.frame * 170, 0, 170, 290, self.x, self.y, 100, 100)

class skill_3:
    def __init__(self, x = 400, y = 300, velocity = 1, job = 'Swordsman'):
        self.job = job
        self.image = load_image(f'{self.job}/skill3.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0

    def update(self):
        self.x += self.velocity * 5
        if self.job == 'Swordsman':
            self.frame = (self.frame + 1) % 4
        elif self.job == 'Wizard':
            self.frame = (self.frame + 1) % 3
        elif self.job == 'Archer':
            self.frame = (self.frame + 1) % 6

    def draw(self):
        if self.job == 'Swordsman':
            self.image.clip_draw(self.frame * 34, 0, 34, 35, self.x, self.y)
        elif self.job == 'Wizard':
            self.image.clip_draw(self.frame * 341, 0, 341, 284, self.x, self.y, 70, 70)
        elif self.job == 'Archer':
            self.image.clip_draw(self.frame * 170, 0, 170, 200, self.x, self.y, 70, 70)



