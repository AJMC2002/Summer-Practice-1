import pygame

pygame.init()
pygame.display.set_caption("Chess Board")

W, N = map(int, input().split())
size = W, W
screen = pygame.display.set_mode(size)

side = W // N


def draw_board():
    screen.fill(pygame.Color("white"))
    for row in range(N):
        for col in range(row % 2, N, 2):
            pygame.draw.rect(
                screen, pygame.Color("black"), (col * side, row * side, side, side)
            )


while pygame.event.wait().type != pygame.QUIT:
    draw_board()
    pygame.display.flip()
    pygame.display.update()

pygame.quit()
