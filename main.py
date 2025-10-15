from pico2d import *


characterjob = ' '

class Character:
    image = None
    def __init__(self):
        self.x, self.y = 400, 400
        self.frame = 0
        self.direction_x = 0
        self.direction_y = 0
        self.direction = 0
        if Character.image is None and characterjob == 'Swordsman':
            Character.image = load_image('Swordsman/Idle.png')
        elif Character.image is None and characterjob == 'Archer':
            Character.image = load_image('Archer/Idle.png')
        elif Character.image is None and characterjob == 'Wizard':
            Character.image = load_image('Wizard/Idle.png')

        pass
    def update(self):
        if characterjob == 'Swordsman':
            self.frame = (self.frame + 1) % 8
        elif characterjob == 'Archer':
            if self.direction_x == 0:
                self.frame = (self.frame + 1) % 6
            else:
                self.frame = (self.frame + 1) % 8
        elif characterjob == 'Wizard':
            if self.direction_x == 0:
                self.frame = (self.frame + 1) % 6
            else:
                self.frame = (self.frame + 1) % 8
        self.x += self.direction_x * 5

        pass

    def draw(self):
        if self.direction_x == 1:
            self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y)
        elif self.direction_x == -1:
            self.image.clip_composite_draw(self.frame * 128, 0, 128, 128, 0, 'h', self.x, self.y, 128, 128)
        else:  # 정지 상태 (마지막 이동 방향에 따라)
            self.image.clip_draw(self.frame * 128, 0, 128, 128, self.x, self.y)
        pass


def show_character_selection():
    global characterjob
    global character_select
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_KEYDOWN and event.key == SDLK_1:
            characterjob = 'Swordsman'
            character_select = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            characterjob = 'Archer'
            character_select = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            characterjob = 'Wizard'
            character_select = False
    pass

def handle_events():
    global running
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                if (characters.direction_x == 0):
                    characters.image = load_image(f'{characterjob}/Run.png')
                characters.direction_x = 1
            elif event.key == SDLK_LEFT:
                if (characters.direction_x == 0):
                    characters.image = load_image(f'{characterjob}/Run.png')
                characters.direction_x = -1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                if(characters.direction_x == 1):
                    characters.image = load_image(f'{characterjob}/Idle.png')
                characters.direction_x = 0
            elif event.key == SDLK_LEFT:
                if(characters.direction_x == -1):
                    characters.image = load_image(f'{characterjob}/Idle.png')
                characters.direction_x = 0



def reset_world():
    global world
    global characters
    world = []

    characters = Character()
    world.append(characters)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

running = True
character_select = True
open_canvas()
while character_select:
    show_character_selection()
reset_world()
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.1)
close_canvas()
