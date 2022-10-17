from math import sin, cos, radians
import pygame


class Point:
    def __init__(self, n):
        self.n = n
        self.x = int(200 * cos(radians(self.n))) + width // 2
        self.y = int(200 * sin(radians(self.n))) + height // 2
        self.coords = (self.x, self.y)

    def render(self):
        pygame.draw.circle(screen, pygame.Color("white"), (self.x, self.y), 2)


class Circle:
    def __init__(self, coeff, mode):
        self.mode = mode
        self.coeff = coeff / 100
        self.color = pygame.Color(0, 0, 0)
        self.color.hsva = (360 * (coeff - coeffLo) // (coeffHi - coeffLo), 50, 90, 100)

    def renderCoeff(self):
        font = pygame.font.Font(None, 30)
        if self.mode:
            color = pygame.Color("green")
        else:
            color = pygame.Color("red")
        text = font.render(f"{self.coeff}", True, color)
        screen.blit(text, (0, 0))

    def render(self):
        self.renderCoeff()
        for n in range(1, 361):
            start = Point(n)
            end = Point(n * self.coeff)
            pygame.draw.line(screen, self.color, start.coords, end.coords, 1)


pygame.init()
pygame.display.set_caption("Таблица умножения")

size = width, height = 500, 500
screen = pygame.display.set_mode(size)
FPS = 30
clock = pygame.time.Clock()
running = True
paused = False
coeffLo = 200
coeff = coeffLo
coeffHi = 300
coeffDiff = 1

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if coeffLo < coeff < coeffHi:
                    paused = not paused or False
                if not paused:
                    coeffDiff *= -1
    if not paused:
        screen.fill(pygame.Color("black"))
        Circle(coeff, coeffDiff > 0).render()
        screen.blit(screen, (0, 0))
        coeff += coeffDiff
        if coeff < coeffLo or coeff > coeffHi:
            coeff -= coeffDiff
        pygame.display.flip()

pygame.quit()
