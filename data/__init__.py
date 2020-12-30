import pygame

if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        image = pygame.Surface([100, 100])
        image.fill(pygame.Color("red"))
        screen.blit(image, (10, 10))
        pygame.display.flip()
pygame.quit()