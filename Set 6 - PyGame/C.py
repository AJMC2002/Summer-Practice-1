import pygame

pygame.init()
pygame.display.set_caption("Ctrl + Z")

screen = pygame.display.set_mode((400, 400))

running = True
drawing = False
x0, y0, w, h = 0, 0, 0, 0
rects = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if rects:
                    rects.pop()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            x1, y1 = event.pos
        elif drawing:
            if event.type == pygame.MOUSEMOTION:
                x2, y2 = event.pos
                x0, y0 = min(x1, x2), min(y1, y2)
                w, h = abs(x1 - x2), abs(y1 - y2)
            if event.type == pygame.MOUSEBUTTONUP:
                rects.append((x0, y0, w, h))
                x0, y0, w, h = 0, 0, 0, 0
                drawing = False

    screen.fill(pygame.Color("black"))
    for rect in rects:
        pygame.draw.rect(screen, pygame.Color("purple2"), rect, 3)
    if drawing:
        pygame.draw.rect(screen, pygame.Color("purple2"), (x0, y0, w, h), 3)
    screen.blit(screen, (0, 0))
    pygame.display.flip()

pygame.quit()
