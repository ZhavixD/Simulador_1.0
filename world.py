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
        
        
    def draw(self, screen, grass_image, camera_x, camera_y):
        # Dibujar el pasto en este chunk con offset de camara
        chunk_sreen_x = self.x - camera_x
        chunk_sreen_y = self.y - camera_y
        
        
        # Calcular el rango de tiles de pasto visibles con un tile extra para evutar lubeas'
        start_x = max(0, camera_x - self.x - constantes.GRASS) // (constantes.GRASS)
        end_x   = min(self.width // constantes.GRASS + 1,
                    (camera_x + constantes.ANCHO - self.x + constantes.GRASS) // constantes.GRASS + 1)
        
        start_y = max(0, camera_y - self.y - constantes.GRASS) // (constantes.GRASS)
        end_y   = min(self.width // constantes.GRASS + 1,
                    (camera_y + constantes.ANCHO - self.y + constantes.GRASS) // constantes.GRASS + 1)
        
        for y in range(int(start_y), int (end_y)):
            for x in range(int(start_x), int(end_x)):
                screen_x = self.x + x * constantes.GRASS - camera_x
                screen_y = self.y + y * constantes.GRASS - camera_y
                screen.blit(grass_image, (screen_x, screen_y))
        
        # Remover elementos agotados
        self.trees = [tree for tree in self.trees if not tree.is_depleted()]
        self.small_stones = [tree for tree in self.small_stones if not tree.is_depleted()]
        
        # Dibujar elemntos solo si estan en pantalla
        for stone in self.small_stones:
            stone_screen_x = stone.x - camera_x
            stone_screen_y = stone.y - camera_y
            if (stone_screen_x + stone.size >= 0 and stone_screen_x <= constantes.ANCHO and
                stone_screen_y + stone.size >= 0 and stone_screen_y <= constantes.ALTO):
                stone.draw(screen, camera_x, camera_y)
                
        for tree in self.trees:
            tree_screen_x  = tree.x - camera_x
            tree_screen_y = tree.y - camera_y
            if (tree_screen_x + tree.size >= 0 and tree_screen_x <= constantes.ANCHO and
                tree_screen_y + tree.size >= 0 and tree_screen_y <= constantes.ALTO):
                tree.draw(screen, camera_x, camera_y)
        
        
        
        

class World:
    
    def __init__(self, width, height):
        
        self.chunk_size = constantes.ANCHO
        
        self.active_chunks = {}  # Diccionario para almacenar chunks activos 
        
        self.view_width  = width
        
        self.view_height = height   
        
        grass_path = os.path.join('assets', 'images', 'objects', 'grass.png')
        
        self.grass_image = pygame.image.load(grass_path).convert() # Cargar la imagen del césped
        
        self.grass_image = pygame.transform.scale(self.grass_image, (constantes.GRASS, constantes.GRASS)) # Escalar la imagen al tamaño deseado
        
        # Sistema dia/noche
        self.current_time = constantes.MORNING_TIME  # Comienza a las 8:00
        
        self.day_overlay = pygame.Surface((width, height))
        
        self.day_overlay.fill(constantes.DAY_COLOR)
        
        self.day_overlay.set_alpha(0)  # Completamente transparente al inicio
        
        # Generar el chunk inicial y adyacentes
        self.generate_chunk(0, 0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                self.generate_chunk(dx, dy)
        
    
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
        current_chunk = self.get_chunk(player_x, player_y)
        
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
                
        for chunk_key in chunks_to_remove:
            del self.active_chunks[chunk_key]
                
        
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
        
    def draw(self, screen, camera_x, camera_y):
        
        # Dibujar los chunks activos
        for chunk in self.active_chunks.values():
            chunk.draw(screen, self.grass_image, camera_x, camera_y)
            
        # Aplicar el overlay de día/noche
        screen.blit(self.day_overlay, (0, 0))
            
    
    def draw_inventory(self, screen, character):
        
        font = pygame.font.Font(None, 20)
        instructions_text = font.render("Press 'I' to open inventory", True, constantes.WHITE)
        screen.blit(instructions_text, (10,10))
        
    
    @property
    def trees(self):
        ''' Devuelve todas las árboles en todos los chunks activos '''
        all_trees = []
        for chunk in self.active_chunks.values():
            all_trees.extend(chunk.trees)
        return all_trees
    
    @property
    def small_stones(self):
        ''' Devuelve todas las piedras en todos los chunks activos '''
        all_stones = []
        for chunk in self.active_chunks.values():
            all_stones.extend(chunk.small_stones)
        return all_stones