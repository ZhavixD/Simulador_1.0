import pygame
import constantes
import random
import os
from elements import Tree, SmallStone
from pygame import Surface

class WorldChunk:
    ''' Representa un chunk del mundo '''
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width  = width
        self.height = height
        
        # Crear semilla unica basada en las coordenadas del chunk
        chunk_seed = hash(f"{x},{y}")
        
        # Guardar la semilla para uso futuro
        old_state = random.getstate()
        
        # Establecer la semilla del chunk
        random.seed(chunk_seed)
        
        # Generar elementos del chunk (árboles, piedras, etc.)
        self.trees = [
            Tree(
                self.x + random.randint(0, width  - constantes.TREE),
                self.y + random.randint(0, height - constantes.TREE)
            ) for _ in range(5)
        ]
        
        self.small_stones = [
            SmallStone(
                self.x + random.randint(0, width  - constantes.SMALL_STONE),
                self.y + random.randint(0, height - constantes.SMALL_STONE)
            ) for _ in range(10)
        ]
        
        
        
        # Restaurar el estado anterior de random
        random.setstate(old_state)
        

class World:
    
    def __init__(self, width, height):
        
        self.chunk_size = constantes.ANCHO
        
        self.active_chunks = {}  # Diccionario para almacenar chunks activos 
        
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
        
    
    def get_chunk(self, x, y):
        ''' Devuelve el chunk correspondiente a las coordenadas (x, y) '''
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        return (chunk_x, chunk_y)   
    
    
    def generate_chunk(self, chunk_x, chunk_y):
        ''' Genera un nuevo chunk en las coordenadas dadas '''
        key = (chunk_x, chunk_y)
        if key not in self.active_chunks:
            x = chunk_x * self.chunk_size
            y = chunk_y * self.chunk_size
            self.active_chunks[key] = WorldChunk(x, y, self.chunk_size, self.chunk_size)
            
            
    def update_chunks(self, player_x, player_y):
        '''Actualiza los chunks basado en la posicion del jugador'''
        current_chunk = self.get_chunk_key(player_x, player_y)
        
        # Generar chunks adyacentes
        for dx in [-2,-1, 0, 1, 2]:
            for dy in [-2,-1, 0, 1, 2]:
                chunk_x = current_chunk[0] + dx
                chunk_y = current_chunk[1] + dy
                self.generate_chunk(chunk_x, chunk_y)
                
        # Eliminar chunks lejanos
        chunks_to_remove = []
        for chunk_key in self.active_chunks:
            distance_x = abs(chunk_key[0] - current_chunk[0])
            distance_y = abs(chunk_key[1] - current_chunk[1])
            if distance_x > 2 or distance_y > 2: # Aumentado el rango de eliminacion
                chunks_to_remove.append(chunk_key)
                
        
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
        