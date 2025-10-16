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
    
    # Variables para la camara
    camera_x = 0
    camera_y = 0

    while True:
        dt = clock.tick(60)  # Controla los FPS
        
        # Manejo de eventos (TECLAS) ================================================================
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
            
            # Manejar eventos del mousepara el inventario
            if event.type == pygame.MOUSEBUTTONDOWN:
                character.inventory.handle_click(pygame.mouse.get_pos(), event.button, show_inventory)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                character.inventory.handle_click(pygame.mouse.get_pos(), event.button, show_inventory)
                    
        #=================================================================================
        dx = dy = 0
        # Movimiento del personaje  
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx = -5
            
        if keys[pygame.K_RIGHT]:
            dx = 5
            
        if keys[pygame.K_UP]:
            dy = -5
            
        if keys[pygame.K_DOWN]:
            dy = 5
            
        # Actualizar estado de corriendo
        character.is_running = keys[pygame.K_LSHIFT] and character.stamina > 0
        
        character.move(dx, dy, world)
            
        
        # La camara sigue al personaje
        camera_x = character.x - constantes.ANCHO // 2
        camera_y = character.y - constantes.ALTO // 2
        
        # Actualizar los chunks del mundo basado en la posicion del jugador
        world.update_chunks(character.x, character.y)
        
        # Actualizar el tiempo del mundo
        world.update_time(dt)
        
        status_update_timer += dt
        if status_update_timer >= constantes.STATUS_UPDATE_INTERVAL:
            character.update_status()   # La comida disminuye con el tiempo
            status_update_timer = 0
            
        if character.energy <= 0 or character.food <= 0 or character.thirst <= 0:
            print("Game over")
            pygame.quit()
            sys.exit()
            
        # Limpiar la pantalla
        screen.fill((0, 0, 0))
        
        # Dibujar mundo con offser de camara
        world.draw(screen, camera_x, camera_y)
        
        # Dibujar el personaje con offset de camara
        character.draw(screen, camera_x, camera_y)
        
        if show_inventory:
            character.draw_inventory(screen)
        
        # Dibujar inventario (hotbar siempre visible + inventario principal si esta abierto)
        character.draw_inventory(screen, show_inventory)
        
        
        # Dibujar el HUD
        font = pygame.font.SysFont(None, 24)
        energy_text  = font.render(f"Energy: {int(character.energy)}", True, constantes.WHITE)
        food_text    = font.render(f"Food: {int(character.food)}", True, constantes.WHITE)
        thirst_text  = font.render(f"Thirst: {int(character.thirst)}", True, constantes.WHITE)
        stamina_text = font.render(f"Stamina: {int(character.stamina)}", True, constantes.WHITE)
        
        # Indicador de tiempo
        time_of_day = (world.current_time / constantes.DAY_LENGTH) * 24  # Convertir a formato 24 horas
        time_text = font.render(f"Time: {int(time_of_day):02d}:00", True, constantes.WHITE)
        
        
        screen.blit(energy_text, (10, (constantes.ALTO - 90)))
        screen.blit(food_text,   (10, (constantes.ALTO - 65)))
        screen.blit(thirst_text, (10, (constantes.ALTO - 40)))
        screen.blit(time_text,   (10, (constantes.ALTO - 15)))
        
        
        pygame.display.flip()

                

if __name__ == "__main__":
    main()
