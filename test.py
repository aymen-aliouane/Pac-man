import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

running = True

while running:

    pygame.draw.rect(
        screen,
        (0, 120, 255),
        (300, 250, 200, 80)
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # pygame.display.flip()

pygame.quit()