import pygame
import os
from random import randint

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.display.set_caption('battle')
size = width, height = 900, 736
screen = pygame.display.set_mode(size)
font = pygame.font.Font('18690.ttf', 36)


def load_image(name):
    fullname = os.path.join('textures', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


back = load_image('battle.png')
screen.blit(back, (0, 0))
hp = {'p': load_image('p_health.png'), 'e': load_image('e_health.png'), 'd': load_image('d_health.png')}
enemy = load_image('skull.png')
player = load_image('m_stay_d.png')
HP_group = pygame.sprite.Group()
persons = pygame.sprite.Group()


class Battle:
    def __init__(self, enemy, e_hp, player):
        super().__init__()
        self.e_hp = e_hp
        self.p_hp = 20
        self.e = enemy
        self.p = player
        self.skills = {((357, 398), (687, 728)): 'sword', ((405, 446), (687, 728)): 'block', ((402, 443), (687, 728)): 'wind', ((500, 541), (687, 728)): 'fire'}
        x, y = 162, 686
        self.p_x, self.p_y = x, y
        for _ in range(102):
            HP(hp['p'], x, y)
            x -= 1
        
        x, y = 724, 6
        self.e_x, self.e_y = x, y
        for _ in range(102):
            HP(hp['e'], x, y)
            x -= 1

    def get_skill(self, x, y):
        for x_r, y_r in self.skills.keys():
            if x in range(x_r[0], x_r[1]) and y in range(y_r[0], y_r[1]):
                skill = self.skills[(x_r, y_r)]
        a = True
        if skill:   
            if skill == 'sword':
                p_atk = 5
                e_atk = randint(0, 10)
            elif skill == 'block':
                e_atk = 0
                p_atk = 0
                a = False
            elif skill == 'wind':
                p_atk = randint(5, 10)
                e_atk = randint(0, 10)
            else:
                p_atk = randint(10, 15)
                e_atk = randint(0, 10)
            self.e_hp -= p_atk
            self.p_hp -= e_atk

            if a:
                self.shake()
                self.attack()
            if self.e_hp <= 0:
                return True
            if self.p_hp <= 0:
                return False

    def shake(self):
        def show():
            screen.blit(back, (0, 0))
            persons.draw(screen)
            pygame.display.flip()
            pygame.time.delay(100)

        self.e.rect.x -= 5
        self.p.rect.x -= 5
        show()

        self.e.rect.x += 10
        self.p.rect.x += 10
        show()

        self.e.rect.x -= 5
        self.p.rect.x -= 5
        show()
    
    def attack(self):
        while self.p_hp < -1:
            self.p_hp += 1
        while self.e_hp < -1:
            self.e_hp += 1
        p_perc = self.p_hp / 102
        e_perc = self.e_hp / 102
        p_x = int(102 * p_perc) + 61
        e_x = int(102 * e_perc) + 623
        for _ in range(self.p_x - p_x):
            HP(hp['d'], self.p_x, self.p_y)
            self.p_x -= 1
        
        for _ in range(self.e_x - e_x):
            HP(hp['d'], self.e_x, self.e_y)
            self.e_x -= 1


class HP(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__(HP_group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(persons)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(649, 34)


class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(persons)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(97, 638)


running = True
fon = True
do = True
enemy = Enemy(enemy)
player = Player(player)
battle = Battle(enemy, 30, player)
while running:
    if fon:
        screen.blit(back, (0, 0))
    else:
        if win:
            text = ['Поздравляю с победой!']
        else:
            text = ['Увы вы проиграли.']
        text_coord = 100
        for line in text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 290
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        do = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if do:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    win = battle.get_skill(*event.pos)
                    if win is True or win is False:
                        fon = False
    HP_group.draw(screen)
    persons.draw(screen)
    pygame.display.flip()
pygame.quit()
