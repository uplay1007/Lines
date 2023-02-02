import os
import sys
import pygame
from board import CBoard
from spinbox import spinBox

pygame.init()
size = 1025, 625
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 20
clock = pygame.time.Clock()
left, top = 400, 10
_circle_cache = {}


# два метода для оюводки текста
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def render_text(text, font, gfcolor=pygame.Color('white'), ocolor=(0, 0, 0), opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


# загрузка изображения
def load_image(name, size1=60, size2=60, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = pygame.transform.scale(image, (size1, size2))
    return image


# начальное окно
def start_screen():
    intro_text = ["Ширина поля:", "Длина поля:", "Кол-во цветов шариков:",
                  "Кол-во шариков, необходимое для уничтожения линии:", "Кол-во объектов, появляющихся в цикле:",
                  "Частота появления бомб(%):"]
    fon = load_image('bubbles.jfif', 1200, 800)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    spinBox1 = spinBox((180, 140), 3, 40)
    spinBox2 = spinBox((180, 193), 3, 40)
    spinBox3 = spinBox((290, 245), 2, 8)
    spinBox4 = spinBox((600, 302), 2)
    spinBox5 = spinBox((470, 356), 2)
    spinBox6 = spinBox((320, 412), 0, 100, 5)
    spinBox1.state = 10
    spinBox2.state = 10
    spinBox3.state = 3
    spinBox4.state = 4
    spinBox5.state = 4
    spinBox6.state = 30
    pygame.draw.rect(screen, (102, 179, 255), (120, 570, 295, 50))
    screen.blit(render_text("НАЧАТЬ ИГРУ", font), (120, 570))
    pygame.draw.rect(screen, (102, 179, 255), (470, 570, 370, 50))
    screen.blit(render_text("ВЫЙТИ ИЗ ИГРЫ", font), (470, 570))
    screen.blit(render_text("Добро пожаловать в игру Lines", font), (30, 10))
    font = pygame.font.Font(None, 40)
    screen.blit(render_text("Настройки игры:", font), (30, 80))
    font = pygame.font.Font(None, 30)
    text_coord = 120
    for line in intro_text:
        string_rendered = render_text(line, font)
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return spinBox1.state, spinBox2.state, spinBox3.state, spinBox4.state, spinBox5.state, \
                           spinBox6.state
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                spinBox1(event.pos)
                spinBox2(event.pos)
                spinBox3(event.pos)
                spinBox4(event.pos)
                spinBox5(event.pos)
                spinBox6(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and 120 <= event.pos[0] <= 415 \
                    and 570 <= event.pos[1] <= 620:
                return spinBox1.state, spinBox2.state, spinBox3.state, spinBox4.state, spinBox5.state, \
                       spinBox6.state
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and 470 <= event.pos[0] <= 840 \
                    and 570 <= event.pos[1] <= 620:
                pygame.quit()
                sys.exit()
        spinBox1.draw(screen)
        spinBox2.draw(screen)
        spinBox3.draw(screen)
        spinBox4.draw(screen)
        spinBox5.draw(screen)
        spinBox6.draw(screen)
        pygame.display.flip()


# цикл для смены окон: начального и игрового
while 1:
    font = pygame.font.Font(None, 50)
    fon = load_image('bubbles.jfif', 1200, 800)
    w, h, num_of_colors, balls_for_row, add_obj, ratio = start_screen()
    colors = [0, 1, 2, 3, 4, 5, 6, 7]
    cell_size = 600 / max(w, h)
    booms = [load_image(f'im_{i}.png') for i in range(1, 13)]
    bomb = load_image('bomb64.png', cell_size, cell_size)
    ball_colors = [load_image(f'ball{i}.svg', cell_size, cell_size) for i in range(1, 9)]
    arrows = [load_image('left_right.png', cell_size // 2, cell_size // 2),
              load_image('up_down.png', cell_size // 2, cell_size // 2),
              load_image('udrl.png', cell_size // 2, cell_size // 2),
              load_image('maximize.png', cell_size // 2, cell_size // 2)]
    board = CBoard(screen, balls_for_row, add_obj, booms, bomb, arrows, ball_colors,
                   colors[:num_of_colors], ratio, w, h, left, top, cell_size)
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and 10 <= event.pos[0] <= 240 \
                    and 450 <= event.pos[1] <= 485:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and 10 <= event.pos[0] <= 310 \
                    and 495 <= event.pos[1] <= 535:
                pygame.quit()
                sys.exit()
        screen.blit(fon, (0, 0))
        board.render()
        pygame.draw.rect(screen, (102, 179, 255), (10, 60, 250, 40))
        pygame.draw.rect(screen, (102, 179, 255), (10, 450, 230, 35))
        screen.blit(render_text("НОВАЯ ИГРА", font), (15, 450))
        pygame.draw.rect(screen, (102, 179, 255), (10, 495, 300, 40))
        screen.blit(render_text("ВЫЙТИ ИЗ ИГРЫ", font), (10, 495))
        screen.blit(render_text(f"{board.scores}", font), (15, 65))
        screen.blit(render_text("ОЧКИ", font), (10, 15))
        pygame.display.flip()
