import pygame
import random

colors = [
    (0, 0, 0),  # Steinchen:
    (0, 240, 240),  # I
    (0, 0, 240),  # J
    (240, 160, 0),  # L
    (240, 240, 0),  # Block
    (0, 240, 0),  # S
    (160, 0, 240),  # T
    (240, 0, 0)  # Z
]


class Figure:
    x = 0
    y = 0

    Figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # J
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # L
        [[1, 2, 5, 6]],  # Block
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # S
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T
        [[4, 5, 9, 10], [2, 6, 5, 9]]  # Z
    ]

    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.type = random.randint(0, len(self.Figures)-1)
        self.color = colors[self.type+1]
        self.rotation = 0

    def image(self):
        return self.Figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation+1) % len(self.Figures[self.type])


class Tetris:
    height = 0
    width = 0
    field = []
    score = 0
    state = "start"
    Figure = None

    def __init__(self, _height, _width):
        self.height = _height
        self.width = _width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(_height):
            new_line = []
            for j in range(_width):
                new_line.append(0)
            self.field.append(new_line)
        self.new_figure()

    def new_figure(self):
        self.Figure = Figure(3, 0)

    def drop(self):
        self.Figure.y += 1
        if self.intersect():
            self.Figure.y -= 1
            self.freeze()

    def side(self, dx):
        old_x = self.Figure.x
        edge = False
        for i in range(4):
            for j in range(4):
                p = i*4+j
                if p in self.Figure.image():
                    if j + self.Figure.x + dx > self.width-1 or j + self.Figure.x + dx < 0:
                        edge = True
        if not edge:
            self.Figure.x += dx
        if self.intersect():
            self.Figure.x = old_x

    def down(self):
        while not self.intersect():
            self.Figure.y += 1
        self.Figure.y -= 1
        self.freeze()

    def left(self):
        self.side(-1)

    def right(self):
        self.side(+1)

    def rotate(self):
        old_rotation = self.Figure.rotation
        self.Figure.rotate()
        if self.intersect():
            self.Figure.rotation = old_rotation

    def intersect(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                p = i*4+j
                if p in self.Figure.image():
                    if i + self.Figure.y > self.height - 1 or i + self.Figure.y < 0 or self.field[i + self.Figure.y][j + self.Figure.x] > 0:
                        intersection = True
        return intersection

    def freeze(self):
        for i in range(4):
            for j in range(4):
                p = i*4+j
                if p in self.Figure.image():
                    self.field[i + self.Figure.y][j +
                                                  self.Figure.x] = self.Figure.type+1
        self.break_lines()
        self.new_figure()
        if self.intersect():
            self.state == "Game Over"

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeroes = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeroes += 1
            if zeroes == 0:
                lines += 1
                for l in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[l][j] = self.field[l-1][j]
        self.score += lines ** 2


pygame.init()
screen = pygame.display.set_mode((350, 550))
pygame.display.set_caption("Tetris")

done = False
fps = 2
clock = pygame.time.Clock()
counter = 0
zoom = 25

game = Tetris(20, 10)
pressing_down = False
pressing_left = False
pressing_right = False

BLUE = (0, 1, 254)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

while not done:
    if game.state == "start":
        game.drop()

    for event in pygame.event.get():
        if event.type == pygame.quit:
            done = True
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                pressing_left = True
            if event.key == pygame.K_RIGHT:
                pressing_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
            if event.key == pygame.K_LEFT:
                pressing_left = False
            if event.key == pygame.K_RIGHT:
                pressing_right = False

        if pressing_down:
            game.down()
        if pressing_left:
            game.left()
        if pressing_right:
            game.right()

    screen.fill(color=WHITE)
    for i in range(game.height):
        for j in range(game.width):
            if game.field[i][j] == 0:
                color = GREY
                border = 1
            else:
                color = colors[game.field[i][j]]
                border = 0
            pygame.draw.rect(
                screen, color, [25+j*zoom, 25+i*zoom, zoom, zoom], border)
    if game.Figure is not None:
        for i in range(4):
            for j in range(4):
                p = i*4+j
                if p in game.Figure.image():
                    pygame.draw.rect(screen, game.Figure.color, [
                                     25+(j+game.Figure.x)*zoom, 25+(i+game.Figure.y)*zoom, zoom, zoom])

    gameover_font = pygame.font.SysFont('Verdana', 65, True, False)
    text_gameover = gameover_font.render(
        "Spiel vorbei!\n Drücke 'ESC'", True, (254, 187, 1))

    if game.state == "gameover":
        screen.blit(text_gameover, [30, 250])

    score_font = pygame.font.SysFont('Verdana', 15, True, False)
    text_score = score_font.render(
        "Score: " + str(game.score), True, (0, 0, 0))
    screen.blit(text_score, [10, 0])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
