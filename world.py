import pygame
import constantes
import random
import os
from elements import Tree, SmallStone
from pygame import surface

class World:
    
    def __init__(self, width, height):
        
        self.width  = width
        
        self.height = height
        
        self.trees  = [Tree(random.randint(0, width - constantes.TREE), random.randint(0, constantes.TREE)) for _ in range(10)]
        
        self.small_stones = [SmallStone(random.randint(0, width - constantes.SMALL_STONE), random.randint(0, height - constantes.SMALL_STONE)) for _ in range(20)]
        
        
        grass_path = os.path.join('assets', 'images', 'objects', 'grass.png')
        
        self.grass_image = pygame.image.load(grass_path).convert() # Cargar la imagen del césped
        
        self.grass_image = pygame.transform.scale(self.grass_image, (constantes.GRASS, constantes.GRASS)) # Escalar la imagen al tamaño deseado
        
        # Sistema dia/noche
        self.current_time = constantes.MORNING_TIME  # Comienza a las 8:00
        
        self.day_overlay = pygame.Surface((width, height))
        
        self.day_overlay.fill(constantes.DAY_COLOR)
        
        self.day_overlay.set_alpha(0)  # Completamente transparente al inicio
        
        
    def update_time(self,dt):
        
        self.current_time = (self.current_time + dt) % constantes.DAY_LENGTH
        
        alpha = 0
        
        # Calcular el nivel de oscuridad basado en la hora del día
        
        if constantes.MORNING_TIME <= self.current_time < constantes.DUSK_TIME:
            
            # Durante el día (8:00 a 18:00)
            
            self.day_overlay.fill(constantes.DAY_COLOR)
            
            alpha = 0
            
        elif constantes.DAWN_TIME <= self.current_time < constantes.MORNING_TIME:
            
            # Amanecer (6:00 a 8:00)
            
            self.day_overlay.fill(constantes.NIGHT_COLOR) 
            
            morning_progress = (self.current_time - constantes.DAWN_TIME) / (constantes.MORNING_TIME - constantes.DAWN_TIME)
            
            alpha = int(constantes.MAX_DARKNESS * (1 - morning_progress))
            
        elif constantes.DUSK_TIME <= self.current_time < constantes.MIDNIGHT:
            
            # Atardecer (18:00 a 24:00)
            
            self.day_overlay.fill(constantes.NIGHT_COLOR)
            
            night_progress = (self.current_time - constantes.DUSK_TIME) / (constantes.MIDNIGHT - constantes.DUSK_TIME)
            
            alpha = int(constantes.MAX_DARKNESS * night_progress)
            
        else:
            
            # Noche (0:00 a 6:00)
            
            self.day_overlay.fill(constantes.NIGHT_COLOR)
            
            alpha = constantes.MAX_DARKNESS
        
        self.day_overlay.set_alpha(alpha)
        
    def draw(self, screen):
        
        for y in range(0, self.height, constantes.GRASS): # Dibujar césped en todo el mundo
            
            for x in range(0, self.width, constantes.GRASS):
                
                screen.blit(self.grass_image, (x, y)) # Dibujar la imagen del césped

        for tree in self.trees:
            
            tree.draw(screen)
            
        for stone in self.small_stones:
            
            stone.draw(screen)
            
        # Aplicar el overlay de día/noche
        screen.blit(self.day_overlay, (0, 0))
            
    
    def draw_inventory(self, screen, character):
        
        font = pygame.font.Font(None, 20)
        instructions_text = font.render("Press 'I' to open inventory", True, constantes.WHITE)
        screen.blit(instructions_text, (10,10))
        