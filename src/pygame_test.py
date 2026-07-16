#!/usr/bin/env python3


if __name__ == "__main__":
    import pygame

    pygame.init()
    
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Test")
    
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
    
        screen.fill((30, 30, 30))
        pygame.display.flip()
    
    pygame.quit()
