import pygame
import constantes
import random
from elements import Tree

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.trees = [Tree(random.randint(0, width-40), random.randint(0, height-40)) for _ in range(10)]
        
        
    def draw(self, screen):
        screen.fill(constantes.GREEN)
        
        for tree in self.trees:
            tree.draw(screen)