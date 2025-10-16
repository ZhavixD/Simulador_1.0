import constantes
import pygame
import os

class Tree:
    
    def __init__(self, x, y):
        
        self.x = x
        
        self.y = y
        
        self.wood  = 5  # Cantidad de madera que da el árbol

        tree_path  = os.path.join('assets', 'images', 'objects', 'tree.png')

        self.image = pygame.image.load(tree_path).convert_alpha() # Cargar la imagen del árbol

        self.image = pygame.transform.scale(self.image, (constantes.TREE, constantes.TREE)) # Escalar la imagen al tamaño deseado

        self.size  = self.image.get_width() # Usar el ancho de la imagen como tamaño del árbol


    def draw(self, screen, camera_x, camera_y):

        screen_x = self.x - camera_x
        
        screen_y = self.y - camera_y
        
        # Solo dibujar si esta en pantalla
        if (screen_x + self.size >= 0 and screen_x <= constantes.ANCHO and 
            screen_y + self.size >= 0 and screen_y <= constantes.ALTO):
            
            screen.blit(self.image, (screen_x, screen_y))
        
    
    def chop(self):
        
        if self.wood > 0:
            
            self.wood -= 1
            
            return True
        
        return False
    
    def is_depleted(self):
        
        return self.wood <= 0


class SmallStone: 
    def __init__(self, x, y):
        
        self.x = x
        
        self.y = y
        
        self.stone = 1  # Cantidad de piedra que da la piedra pequeña
        
        small_stone_path = os.path.join('assets', 'images', 'objects', 'small_stone.png')

        self.image = pygame.image.load(small_stone_path).convert_alpha() # Cargar la imagen de la piedra pequeña

        self.image = pygame.transform.scale(self.image, (constantes.SMALL_STONE, constantes.SMALL_STONE)) # Escalar la imagen al tamaño deseado

        self.size  = self.image.get_width() # Usar el ancho de la imagen como tamaño de la piedra pequeña

        
    def draw(self, screen, camera_x, camera_y):
        # Claclar la posicion en pantalla relativa a la camara
        screen_x = self.x - camera_x
        
        screen_y = self.y - camera_y
        
        # Solo dibujar si esta en pantalla
        if (screen_x + self.size >= 0 and screen_x <= constantes.ANCHO and 
            
            screen_y + self.size >= 0 and screen_y <= constantes.ALTO):
            
            screen.blit(self.image, (screen_x, screen_y))
            
        
    def collect(self):
        
        if self.stone > 0:
            
            self.stone -= 1
            
            return True
        
        return False
    
    def is_depleted(self):
        
        return self.stone <= 0