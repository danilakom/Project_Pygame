import pygame
import sys
import os


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.display.set_caption('rpg')
size = width, height = 1262, 654
screen = pygame.display.set_mode(size)


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
enemies = {'skeleton': load_image('skeleton.png'), 'skull': load_image('skull.png'), 'slime': load_image('slime.png'), 'ghost': load_image('ghost.png'), 'spider': load_image('spider.png'), 'mid_boss': load_image('med_boss.png'), 'main_boss': load_image('main_boss.png')}

player = None

player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
breaks_out = pygame.sprite.Group()
breaks_in = pygame.sprite.Group()


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
    font = pygame.font.SysFont('arial', 30)
    text_coord = 220

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 330
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

running = True
anim = False
loc = 'out'

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
    pygame.display.flip()
pygame.quit()
