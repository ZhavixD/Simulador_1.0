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


    def draw(self, screen):

        screen.blit(self.image, (self.x, self.y)) # Dibujar la imagen del árbol en la pantalla
        
    
    def chop(self):
        
        if self.wood > 0:
            
            self.wood -= 1
            
            return True
        
        return False


class SmallStone: 
    def __init__(self, x, y):
        
        self.x = x
        
        self.y = y
        
        self.stone = 1  # Cantidad de piedra que da la piedra pequeña
        
        small_stone_path = os.path.join('assets', 'images', 'objects', 'small_stone.png')

        self.image = pygame.image.load(small_stone_path).convert_alpha() # Cargar la imagen de la piedra pequeña

        self.image = pygame.transform.scale(self.image, (constantes.SMALL_STONE, constantes.SMALL_STONE)) # Escalar la imagen al tamaño deseado

        self.size  = self.image.get_width() # Usar el ancho de la imagen como tamaño de la piedra pequeña

        
    def draw(self, screen):

        screen.blit(self.image, (self.x, self.y)) # Dibujar la imagen de la piedra en la pantalla
