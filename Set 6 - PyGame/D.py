from random import randint
import pygame


class Grid:
    def __init__(self, N):
        self.font = pygame.font.Font(None, 30)
        self.size = N + 2
        self.side = width // self.size
        self.field = [[[-1, 0] for _ in range(self.size)] for _ in range(self.size)]
        self.mines = [[randint(1, 10), randint(1, 10)] for _ in range(randint(1, 100))]

        for i, j in self.mines:
            self.field[i][j][0] = 0

        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                if [i, j] in self.mines:
                    sub_is = [i - 1, i, i + 1]
                    sub_js = [j - 1, j, j + 1]
                    for sub_i in sub_is:
                        for sub_j in sub_js:
                            self.field[sub_i][sub_j][1] += 1

    def click(self, pos):
        j, i = pos[0] // self.side, pos[1] // self.side
        self.field[i][j][0] *= -1

    def __draw_sq(self, screen, rect, i, j):
        cell = self.field[i][j]
        if cell[0]:
            pygame.draw.rect(screen, pygame.Color("white"), rect, 1)
            if cell[0] == 1:
                text = self.font.render(str(cell[1]), True, pygame.Color("white"))
                text_rect = text.get_rect(
                    center=((j + 0.5) * self.side, (i + 0.5) * self.side)
                )
                screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, pygame.Color("red"), rect)

    def render(self, screen):
        for i in range(1, self.size - 1):
            for j in range(1, self.size - 1):
                rect = (j * self.side, i * self.side, self.side, self.side)
                self.__draw_sq(screen, rect, i, j)


pygame.init()
pygame.display.set_caption("Полусапер")

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
running = True
grid = Grid(10)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            grid.click(event.pos)
    screen.fill(pygame.Color("black"))
    grid.render(screen)
    screen.blit(screen, (0, 0))
    pygame.display.flip()

pygame.quit()
