from pico2d import load_image
class skill_1:
    def __init__(self, x = 400, y = 300, velocity = 1, job = 'Swordsman'):
        pass

    def update(self):
        pass

    def draw(self):
        pass

class skill_2:
    def __init__(self, x = 400, y = 300, velocity = 1, job = 'Swordsman'):
        pass

    def update(self):
        pass

    def draw(self):
        pass

class skill_3:
    def __init__(self, x = 400, y = 300, velocity = 1, job = 'Swordsman'):
        pass

    def update(self):
        pass

    def draw(self):
        pass



class skill_effect:
    image = None
    def __init__(self, characters_obj, char_job, skill_point):
        self.x, self.y = 0, 0
        self.frame = 0
        self.move_count = 0
        self.image = None
        self.characters = characters_obj  # Character 객체 저장
        self.characterjob = char_job
        self.skill_p = skill_point

    def start_effect(self, target_x, target_y):
        self.x = target_x
        self.y = target_y

    def update(self):
        #if self.skill_p == 1 and self.image is None:
            #self.image = load_image(f'{self.characterjob}/skill1.png')
        #elif self.skill_p == 2 and self.image is None:
           # self.image = load_image(f'{self.characterjob}/skill2.png')
        #elif self.skill_p == 3 and self.image is None:
            #self.image = load_image(f'{self.characterjob}/skill3.png')
        if self.skill_p == 1:
            if self.characterjob == 'Swordsman':
                skill_offset = 40
                target_x = self.characters.x + (skill_offset if self.characters.direction == 0 else -skill_offset)
                target_y = self.characters.y - 20

                self.start_effect(target_x, target_y)
                self.frame = (self.frame + 1) % 3
                self.move_count += self.characters.direction_x * 5
                self.characters.x += self.characters.direction_x * 5
            elif self.characterjob == 'Wizard':
                self.frame = (self.frame + 1) % 3
                self.x += 10
            elif self.characterjob == 'Archer':
                self.frame = (self.frame + 1) % 4
                self.x += 10
        if self.move_count >= 30:
            self.skill_p = 0
            self.move_count = 0
            self.frame = 0
            self.characters.direction_x = 0
            self.characters.image = load_image(f'{self.characterjob}/Idle.png')

        if self.skill_p == 2:
            if self.characterjob == 'Swordsman':
                skill_offset = 40
                target_y = self.characters.y + skill_offset
                target_x = self.characters.x

                self.start_effect(target_x, target_y)
                self.frame = self.frame + 1
                if self.frame >= 5:
                    self.Skill_x = False
                    self.frame = 0
            elif self.characterjob == 'Wizard':
                self.frame = (self.frame + 1) % 3
                self.x += 10
            elif self.characterjob == 'Archer':
                self.frame = (self.frame + 1) % 6
                self.x += 10
        if self.skill_p == 3:
            if self.characterjob == 'Swordsman':
                self.frame = (self.frame + 1) % 4
                self.x += 10
            elif self.characterjob == 'Wizard':
                self.frame = (self.frame + 1) % 3
                self.x += 10
            elif self.characterjob == 'Archer':
                self.frame = (self.frame + 1) % 6
                self.x += 10
        pass

    def draw(self):
        if self.image is None:
            return
        if self.skill_p == 1:
            if self.characterjob == 'Swordsman':
                self.image.clip_draw(self.frame * 34, 0, 34, 128, self.x, self.y)
            elif self.characterjob == 'Wizard':
                self.image.clip_draw(self.frame * 34, 0, 34, 36, self.x, self.y, 30,30)
            elif self.characterjob == 'Archer':
                self.image.clip_draw(self.frame * 33, 0, 33, 32, self.x, self.y, 50,50)

        elif self.skill_p == 2:
            if self.characterjob == 'Swordsman':
                self.image.clip_draw(0, self.frame * 200, 250, 200, self.x, self.y, 75,75)
            elif self.characterjob == 'Wizard':
                self.image.clip_draw(self.frame * 341 ,0, 341, 284, self.x, self.y, 50,50)
            elif self.characterjob == 'Archer':
                self.image.clip_draw(self.frame * 170 ,0, 170, 290, self.x, self.y, 100,100)

        elif self.skill_p == 3:
            if self.characterjob == 'Swordsman':
                self.image.clip_draw(self.frame * 34, 0, 34, 35, self.x, self.y)
            elif self.characterjob == 'Wizard':
                self.image.clip_draw(self.frame * 341 ,0, 341, 284, self.x, self.y, 70,70)
            elif self.characterjob == 'Archer':
                self.image.clip_draw(self.frame * 170 ,0, 170, 200, self.x, self.y, 70,70)
