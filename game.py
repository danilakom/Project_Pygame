import pygame
import sys
import os
import time
from random import randint, choice


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.display.set_caption('rpg')
size = width, height = 1262, 654
screen = pygame.display.set_mode(size)
font = pygame.font.Font('18690.ttf', 36)


def load_image(name):
    fullname = os.path.join('textures', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


pygame.display.set_icon(load_image('icon.png'))

male_images = {'u': load_image('male_u_t.png'), 'd': load_image('male_d_t.png'), 'r': load_image('male_r_t.png'), 'l': load_image('male_l_t.png'), 'dead': load_image('male_dead.png'), 'su': load_image('m_stay_u.png'), 'sd': load_image('m_stay_d.png'), 'sl': load_image('m_stay_l.png'), 'sr': load_image('m_stay_r.png')}
female_images = {'u': load_image('female_u.png'), 'd': load_image('female_d.png'), 'r': load_image('female_r.png'), 'l': load_image('female_l.png'), 'dead': load_image('female_dead.png'), 'su': load_image('f_stay_u.png'), 'sd': load_image('f_stay_d.png'), 'sl': load_image('f_stay_l.png'), 'sr': load_image('f_stay_r.png')}
locations = {'out': load_image('loc.png'), 'home': load_image('home.png')}
fon = load_image('fon.png')
brakes_out = [(207, 52, 147, 284), (354, 121, 52, 215), (406, 45, 111, 273), (460, 28, 26, 17), (517, 45, 59, 264), (576, 45, 104, 273), (680, 136, 87, 182), (767, 136, 48, 91), (815, 34, 137, 375), (366, 369, 37, 34), (411, 363, 35, 46), (88, 227, 45, 45), (0, 0, 134, 90)]
brakes_in = [(300, 492, 400, 34), (414, 484, 51, 8), (300, 416, 11, 76), (300, 293, 30, 123), (330, 293, 370, 33), (689, 385, 11, 107), (657, 326, 43, 59), (600, 326, 29, 11), (330, 326, 106, 36), (497, 386, 8, 47), (505, 407, 89, 26), (533, 433, 27, 6), (589, 386, 7, 26), (535, 344, 24, 63), (528, 399, 7, 8), (559, 399, 6, 8)]
farms = [(0, 590, 1000, 280), (0, 554, 727, 36), (765, 498, 235, 92), (0, 91, 206, 137), (134, 448, 44, 106), (225, 446, 44, 108), (590, 497, 137, 57), (952, 0, 48, 498), (0, 228, 45, 215), (354, 45, 52, 75), (134, 0, 326, 44), (134, 44, 72, 47), (487, 0, 465, 34), (680, 34, 134, 102), (487, 34, 193, 10), (460, 0, 27, 28)]
enemies = {'skeleton': load_image('skeleton.png'), 'skull': load_image('skull.png'), 'slime': load_image('slime.png'), 'ghost': load_image('ghost.png'), 'spider': load_image('spider.png'), 'mid_boss': load_image('med_boss.png'), 'main_boss': load_image('main_boss.png')}
back = load_image('battle.png')
hp = {'p': load_image('p_health.png'), 'e': load_image('e_health.png'), 'd': load_image('d.png'), 'm': load_image('m.png')}


player = None

player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
HP_group = pygame.sprite.Group()
enemy_ter = pygame.sprite.Group()
breaks_out = pygame.sprite.Group()
breaks_in = pygame.sprite.Group()
number_of_murders = pygame.sprite.Group()


class Anime_Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, group, dir, x, y):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.x, self.y = x, y
        self.rect = self.rect.move(x, y)
        self.dir = dir
        self.col = columns
        if x == 726 and y == 429:
            self.loc = 'out'
        else:
            self.loc = 'in'
        self.k = 0
        self.random()

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, next=False):
        if next:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if self.dir == 'u':
            self.y -= 1
            self.rect.y -= 1
        if self.dir == 'd':
            self.y += 1
            self.rect.y += 1
        if self.dir == 'l':
            self.x -= 1
            self.rect.x -= 1
        if self.dir == 'r':
            self.x += 1
            self.rect.x += 1
        if self.loc == 'out':
            a = pygame.sprite.spritecollideany(self, breaks_out)
        else:
            a = pygame.sprite.spritecollideany(self, breaks_in)
        if (a and a.rect.y <= self.y + self.rect.h <= a.rect.y + a.rect.h) or self.x < 0 or self.x + self.rect.width > width or self.y < 0 or self.y + self.rect.height > height:
            if self.dir == 'u':
                self.y += 1
                self.rect.y += 1
            if self.dir == 'd':
                self.y -= 1
                self.rect.y -= 1
            if self.dir == 'l':
                self.x += 1
                self.rect.x += 1
            if self.dir == 'r':
                self.x -= 1
                self.rect.x -= 1
        if pygame.sprite.spritecollideany(self, enemy_ter):
            self.k += 1
            if self.k == self.count:
                self.k = 0
                self.random()
                enemy = choice(list(enemies.keys())[:5])
                if enemy == 'skeleton':
                    hpp = 20
                elif enemy == 'skull':
                    hpp = 20
                elif enemy == 'slime':
                    hpp = 10
                elif enemy == 'spider':
                    hpp = 30
                elif enemy == 'mid_boss':
                    hpp = 50
                elif enemy == 'main_boss':
                    hpp = 100
                elif enemy == 'ghost':
                    hpp = 20
                if start_battle(enemies[enemy], player['sd'], hpp, enemy):
                    murders.plus()
                else:
                    # TODO убийство
                    pass
                global anim
                global k
                anim = False
                k = 0
        else:
            self.k = 0
    
    def change(self, sheet, dir, columns, rows):
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.dir = dir
        self.rect = self.rect.move(self.x, self.y)

    def get_dir(self):
        return self.dir
    
    def get_col(self):
        return self.col
    
    def near_door(self):
        if self.loc == 'out':
            if 516 <= self.x <= 575 and 279 <= self.y <= 298:
                return True
        else:
            if 414 <= self.x <= 464 and self.y + self.rect.height >= 470:
                return True
        return False
    
    def random(self):
        self.count = randint(100, 400)
    
    def change_pos(self, x, y):
        if x == 536 and y == 321:
            self.loc = 'out'
        else:
            self.loc = 'in'
        self.x, self.y = x, y
        self.rect = self.rect.move(x, y)


class Brake(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, group):
        super().__init__(group)
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)


class Farm(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__(enemy_ter)
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

class Battle:
    def __init__(self, enemy, e_hp, player, e):
        super().__init__()
        self.const_e_hp = e_hp
        self.e_hp = e_hp
        self.p_hp = 50
        self.mp = 100
        self.e = enemy
        self.p = player
        self.skills = {((408, 633), (609, 650)): 'sword', ((456, 498), (609, 650)): 'block', ((503, 634), (609, 650)): 'wind', ((551, 634), (609, 650)): 'fire'}
        self.enemy = e
        x, y = 549, 559
        self.p_x, self.p_y = x, y
        for _ in range(102):
            HP(hp['p'], x, y)
            x -= 1
        
        x, y = 549, 166
        self.e_x, self.e_y = x, y
        for _ in range(102):
            HP(hp['e'], x, y)
            x -= 1
        
        x, y = 549, 583
        self.m_x, self.m_y = x, y
        for _ in range(102):
            HP(hp['m'], x, y)
            x -= 1

    def get_skill(self, x, y):
        skill = None
        for x_r, y_r in self.skills.keys():
            if x in range(x_r[0], x_r[1]) and y in range(y_r[0], y_r[1]):
                skill = self.skills[(x_r, y_r)]
        a = True
        if skill:   
            if skill == 'sword' and self.mp >= 5:
                p_atk = 5
                e_atk = randint(0, 10)
                m = 5
                if self.enemy == 'ghost' or self.enemy == 'skeleton':
                    p_atk = 1
            elif skill == 'block' and self.mp >= 10:
                e_atk = 0
                p_atk = 0
                a = False
                m = 10
            elif skill == 'wind' and self.mp >= 20:
                p_atk = randint(5, 10)
                e_atk = randint(0, 10)
                m = 20
                if self.enemy == 'slime':
                    p_atk = 1
            elif skill == 'fire' and self.mp >= 30:
                p_atk = randint(10, 15)
                e_atk = randint(0, 10)
                m = 30
                if self.enemy == 'skull':
                    p_atk = 1
            else:
                a = False
                p_atk = 0
                e_atk = 0
                m = 0
            self.e_hp -= p_atk
            self.p_hp -= e_atk
            self.mp -= m

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
        while self.p_hp <= -1:
            self.p_hp += 1
        while self.e_hp <= -1:
            self.e_hp += 1
        while self.mp <= -1:
            self.mp += 1
        p_perc = self.p_hp / 50
        e_perc =  self.e_hp / self.const_e_hp
        m_perc = self.mp / 100
        if p_perc < 0:
            p_perc = 0
        if e_perc < 0:
            e_perc = 0
        if m_perc < 0:
            m_perc = 0
        p_x = int(p_perc * 102) + 448
        e_x = int(e_perc * 102) + 448
        m_x = int(m_perc * 102) + 448
        for _ in range(self.p_x - p_x):
            HP(hp['d'], self.p_x, self.p_y)
            self.p_x -= 1
        
        for _ in range(self.e_x - e_x):
            HP(hp['d'], self.e_x, self.e_y)
            self.e_x -= 1
        
        for _ in range(self.m_x - m_x):
            HP(hp['d'], self.m_x, self.m_y)
            self.m_x -= 1
    
    def plus(self):
        if self.mp < 100:
            self.mp += 1
            m_perc = self.mp / 102
            m_x = int(102 * m_perc) + 448
            for _ in range(m_x - self.m_x):
                HP(hp['m'], self.m_x, self.m_y)
                self.m_x += 1
        pygame.display.flip()


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
        self.rect = self.rect.move(488, 183)


class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(persons)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(488, 514)


class Murders(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(number_of_murders)
        self.image = pygame.Surface((119, 54))
        self.image.set_alpha(0)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(6, 0)
        self.count = 0
        self.font = pygame.font.Font('18690.ttf', 15)
        self.show()
    
    def show(self):
        text = f'Кол-во убийств: {self.count}'
        render = self.font.render(text, 1, pygame.Color('black'))
        self.image = pygame.Surface((119, 54))
        self.image.set_alpha(0)
        self.image = self.image.convert_alpha()
        self.image.blit(render, pygame.Rect(0, 27, 119, 54))
    
    def plus(self):
        self.count += 1
        if self.count == 10:
            if start_battle(enemies['mid_boss'], player['sd'], 50): murders.plus()
            else: pass
        elif self.count == 30:
            if start_battle(enemies['main_boss'], player['sd'], 100): murders.plus()
            else: pass
        self.show()


def change(w, h):
    size = width, height = w, h
    screen = pygame.display.set_mode(size)


def start_battle(enemy, player, hpp, e):
    fon = True
    do = True
    running = True
    a = True
    k = None
    global persons
    persons = pygame.sprite.Group()
    enemy = Enemy(enemy)
    player = Player(player)
    battle = Battle(enemy, hpp, player, e)
    timme = time.time()
    while running:
        if fon:
            screen.blit(back, (0, 0))
        else:
            if a:
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
                a = False
                k = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if do:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        win = battle.get_skill(*event.pos)
                        if win is True or win is False:
                            fon = False
        if time.time() - timme >= 0.5:
            timme = time.time()
            battle.plus()
        if k is not None:
            k += 1
        if k and k == 300:
            anim = False
            if win: return True
            else: return False
        HP_group.draw(screen)
        persons.draw(screen)
        pygame.display.flip()


FPS = 60
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ['Добро пожаловать в наше приключение!',
                  'Немного об управлении: ↑ или W - движение вверх,',
                  '↓ или S - движение вниз, → или D - движение вправо,',
                  '← или A - движение влево.',
                  'Нажмите 1, если хотите играть за персонажа мужского пола',
                  'Нажмите 2, если хотите играть за персонажа женского пола']

    screen.blit(fon, (0, 0))
    text_coord = 200

    for line in intro_text:
        string_rendered = font.render(line, 1000, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'm'
                if event.key == pygame.K_2:
                    return 'f' 
        pygame.display.flip()
        clock.tick(FPS)


if start_screen() == 'm':
    player = male_images
else:
    player = female_images

location = locations['out']
size = width, height = location.get_width(), location.get_height()
screen = pygame.display.set_mode(size)

for b in brakes_out:
    Brake(*b, breaks_out)

for b in brakes_in:
    Brake(*b, breaks_in)

for f in farms:
    Farm(*f)

running = True
anim = False
loc = 'out'
murders = Murders()

x, y = 726, 429
p = Anime_Player(player['u'], 3, 1, player_group, 'u', x, y)
k = 0

while running:
    if loc != 'in':
        n, m = 0, 0
    else:
        n, m = 300, 293
    screen.fill((0, 0, 0))
    screen.blit(location, (n, m))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                anim = True
                k = 0
                if p.get_dir() != 'u' or p.get_col() != 1:
                    p.change(player['u'], 'u', 3, 1)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                anim = True
                k = 0
                if p.get_dir() != 'd' or p.get_col() != 1:
                    p.change(player['d'], 'd', 3, 1)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                anim = True
                k = 0
                if p.get_dir() != 'l' or p.get_col() != 1:
                    p.change(player['l'], 'l', 3, 1)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                anim = True
                k = 0
                if p.get_dir() != 'r' or p.get_col() != 1:
                    p.change(player['r'], 'r', 3, 1)
            if event.key == pygame.K_e:
                if loc == 'out':
                    if p.near_door():
                        loc = 'in'
                        location = locations['home']
                        x, y = 428, 447
                        p.change_pos(x, y)
                else:
                    if p.near_door():
                        loc = 'out'
                        location = locations['out']
                        x, y = 536, 321
                        p.change_pos(x, y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                anim = False
                k = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                anim = False
                k = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                anim = False
                k = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                anim = False
                k = 0
    if anim:
        k += 1
        if k == 20:
            player_group.update(True)
            k = 0
        else:
            player_group.update()
    else:
        if p and p.get_dir() == 'u':
            p.change(player['su'], 'u', 1, 1)
        if p and p.get_dir() == 'd':
            p.change(player['sd'], 'd', 1, 1)
        if p and p.get_dir() == 'l':
            p.change(player['sl'], 'l', 1, 1)
        if p and p.get_dir() == 'r':
            p.change(player['sr'], 'r', 1, 1)
    player_group.draw(screen)
    number_of_murders.draw(screen)
    pygame.display.flip()
pygame.quit()
