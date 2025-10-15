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
    show_inventory = False
    
    status_update_timer = 0 # Temporizador para actualizar estado cada segundo

    while True:
        dt = clock.tick(60)  # Controla los FPS
        
        # Manejo de eventos ================================================================
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    character.interact(world)
                    
                if event.key == pygame.K_i:
                    show_inventory = not show_inventory
                    
                if event.key == pygame.K_f:
                    character.update_food(5)
                    
                if event.key == pygame.K_t:
                    character.update_thirst(5)
                    
        #=================================================================================
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character.move(-5, 0, world)
            
        if keys[pygame.K_RIGHT]:
            character.move(5, 0, world)
            
        if keys[pygame.K_UP]:
            character.move(0, -5, world)
            
        if keys[pygame.K_DOWN]:
            character.move(0, 5, world)
        
        status_update_timer += dt
        if status_update_timer >= constantes.STATUS_UPDATE_INTERVAL:
            character.update_status()   # La comida disminuye con el tiempo
            status_update_timer = 0
            
        if character.energy <= 0 or character.food <= 0 or character.thirst <= 0:
            print("Game over")
            pygame.quit()
            sys.exit()
            
        world.draw(screen)
        character.draw(screen)
        if show_inventory:
            character.draw_inventory(screen)
        
        font = pygame.font.SysFont(None, 24)
        energy_text = font.render(f"Energy: {int(character.energy)}", True, constantes.WHITE)
        food_text   = font.render(f"Food: {int(character.food)}", True, constantes.WHITE)
        thirst_text = font.render(f"Thirst: {int(character.thirst)}", True, constantes.WHITE)
        
        screen.blit(energy_text, (10, (constantes.ALTO - 70)))
        screen.blit(food_text,   (10, (constantes.ALTO - 45)))
        screen.blit(thirst_text, (10, (constantes.ALTO - 20)))
        
        pygame.display.flip()

                

if __name__ == "__main__":
    main()
