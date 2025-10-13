import pygame
import constantes
import os

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = {"wood": 0, "stone": 0}
        image_path = os.path.join("assets", "images", "character", "prota.png")
        self.image = pygame.image.load(image_path).convert_alpha() # Cargar la imagen del personaje
        self.image = pygame.transform.scale(self.image, (constantes.PERSONAJE_SIZE, constantes.PERSONAJE_SIZE)) # Escalar la imagen al tamaño deseado
        self.size  = self.image.get_width() # Usar el ancho de la imagen como tamaño del personaje
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y)) # Dibujar la imagen del personaje en la pantalla
        
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, constantes.ANCHO - self.size))
        self.y = max(0, min(self.y, constantes.ALTO - self.size))