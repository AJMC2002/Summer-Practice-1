import pygame
from copy import deepcopy


class Button(pygame.sprite.Sprite):
    def __init__(self, img, size, x, y):
        super(Button, self).__init__()
        self.image = pygame.image.load(img)
        self.size = size
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                action = True
                self.clicked = True
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
        surface.blit(self.image, self.rect)
        return action


class ConwaysGame:
    def __init__(self, matrix=[]):
        with open("assets/instructions.txt", encoding="utf-8") as instructions:
            print(instructions.read())

        if matrix:
            self.TILE = 20
            self.W, self.H = len(matrix[0]), len(matrix)
            self.RES = self.WIDTH, self.HEIGHT = self.TILE * self.W, self.TILE * self.H
            self.DEFAULT_FIELD = matrix
        else:
            self.RES = self.WIDTH, self.HEIGHT = 1200, 800
            self.TILE = 30
            self.W, self.H = self.WIDTH // self.TILE, self.HEIGHT // self.TILE
            self.DEFAULT_FIELD = [[0 for _ in range(self.W)] for _ in range(self.H)]

        self.FPS = 12

        pygame.init()
        self.surface = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()
        self.curr_field = deepcopy(self.DEFAULT_FIELD)
        self.next_field = deepcopy(self.DEFAULT_FIELD)
        self.btn_play = Button("assets/play.png", (60, 60), self.WIDTH - 180, 30)
        self.btn_pause = Button("assets/pause.png", (60, 60), self.WIDTH - 180, 30)
        self.btn_reset = Button("assets/reset.png", (60, 60), self.WIDTH - 90, 30)
        self.run()
        pygame.quit()

    def isAlive(self, i, j):
        count = 0
        for sub_i in range(i - 1, i + 2):
            for sub_j in range(j - 1, j + 2):
                if sub_i != i or sub_j != j:
                    if self.curr_field[sub_i][sub_j]:
                        count += 1
        if self.curr_field[i][j]:
            if count == 2 or count == 3:
                return 1
            return 0
        else:
            if count == 3:
                return 1
            return 0

    def drawGrid(self):
        for x in range(self.TILE, self.WIDTH, self.TILE):
            pygame.draw.line(
                self.surface,
                pygame.Color("purple"),
                (x, self.TILE),
                (x, self.HEIGHT - self.TILE),
            )
        for y in range(self.TILE, self.HEIGHT, self.TILE):
            pygame.draw.line(
                self.surface,
                pygame.Color("mediumpurple"),
                (self.TILE, y),
                (self.WIDTH - self.TILE, y),
            )
        for j in range(1, self.W - 1):
            for i in range(1, self.H - 1):
                if self.curr_field[i][j]:
                    pygame.draw.rect(
                        self.surface,
                        pygame.Color("violet"),
                        (
                            j * self.TILE + 2,
                            i * self.TILE + 2,
                            self.TILE - 2,
                            self.TILE - 2,
                        ),
                    )
                self.next_field[i][j] = self.isAlive(i, j)

    def drawBtnBox(self):
        pygame.draw.rect(
            self.surface,
            pygame.Color("black"),
            (self.WIDTH - 210, 0, 210, 120),
            border_bottom_left_radius=15,
        )

    def isOnGrid(self, pos):
        x, y = pos
        i, j = -1, -1
        if not (x >= self.WIDTH - 210 and y <= 120):
            j = x // self.TILE
            i = y // self.TILE
        return i, j

    def run(self):
        running = True
        paused = True
        dragging = False
        while running:
            self.surface.fill(pygame.Color("black"))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not (paused)
                    if event.key == pygame.K_ESCAPE:
                        self.curr_field = deepcopy(self.DEFAULT_FIELD)
                        paused = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    i, j = self.isOnGrid(event.pos)
                    if i != -1 and j != -1:
                        if event.button == 1:
                            self.curr_field[i][j] = 1
                            dragging = True
                        elif event.button == 3:
                            self.curr_field[i][j] = 0
                            dragging = True
                elif event.type == pygame.MOUSEMOTION:
                    i, j = self.isOnGrid(event.pos)
                    if i != -1 and j != -1 and dragging:
                        if pygame.mouse.get_pressed()[0]:
                            self.curr_field[i][j] = 1
                        elif pygame.mouse.get_pressed()[2]:
                            self.curr_field[i][j] = 0
                    else:
                        dragging = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False

            self.drawGrid()
            self.drawBtnBox()

            if paused or dragging:
                if self.btn_play.draw(self.surface):
                    paused = False
            else:
                if self.btn_pause.draw(self.surface):
                    paused = True
                self.curr_field = deepcopy(self.next_field)

            if self.btn_reset.draw(self.surface):
                self.curr_field = deepcopy(self.DEFAULT_FIELD)
                paused = True

            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    ConwaysGame()
