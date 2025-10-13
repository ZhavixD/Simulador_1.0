import pygame
import constantes

class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.wood = 5  # Cantidad de madera que da el árbol
        
    def draw(self, screen):
        pygame.draw.rect(screen, constantes.BROWN, (self.x, self.y, self.size, self.size))