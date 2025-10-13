# py -m venv .venv
# source .venv/Scripts/activate
# pip freeze > requirements.txt
#---------------------------------------------------------
import pygame
import sys
import constantes
from character import Character
from world import World
#---------------------------------------------------------

# Inicializar el juego
pygame.init()


screen = pygame.display.set_mode((constantes.ANCHO, constantes.ALTO))
pygame.display.set_caption("Simulador vida salvaje")


def main():
    clock = pygame.time.Clock()
    world = World(constantes.ANCHO, constantes.ALTO)
    character = Character(constantes.ANCHO // 2, constantes.ALTO // 2) # Aparece en medio del mundo

    while True:
        for event in pygame.event.get(): #hola
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character.move(-5, 0)
            
        if keys[pygame.K_RIGHT]:
            character.move(5, 0)
            
        if keys[pygame.K_UP]:
            character.move(0, -5)
            
        if keys[pygame.K_DOWN]:
            character.move(0, 5)
        
        world.draw(screen)
        character.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
                

if __name__ == "__main__":
    main()
