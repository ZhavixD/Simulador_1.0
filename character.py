import pygame
import constantes
import os

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = {"wood": 0, "stone": 0}
        image_path = os.path.join('assets', 'images', 'characters', 'prota.png')
        self.image = pygame.image.load(image_path).convert_alpha() # Cargar la imagen del personaje
        self.image = pygame.transform.scale(self.image, (constantes.PLAYER, constantes.PLAYER)) # Escalar la imagen al tamaño deseado
        self.size  = self.image.get_width() # Usar el ancho de la imagen como tamaño del personaje
        
        self.item_images = {
            "wood": self.load_items_image("wood.png"),
            "stone": self.load_items_image("small_stone.png")        
        }
        
        self.energy = constantes.MAX_ENERGY
        self.food   = constantes.MAX_FOOD
        self.thirst = constantes.MAX_THIRST
        
    def load_items_image(self, filename):
        path = os.path.join('assets', 'images', 'objects', filename)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (40, 40))
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y)) # Dibujar la imagen del personaje en la pantalla
        self.draw_status_bars(screen)
        
    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy
        
        for tree in world.trees:
            if self.check_collision(new_x, new_y, tree):
                return  # Colisión con un árbol, no mover
        
        self.x = new_x
        self.y = new_y
        self.x = max(0, min(self.x, constantes.ANCHO - self.size))
        self.y = max(0, min(self.y, constantes.ALTO - self.size))
        
        # Cuando se mueve pierde energia
        self.update_energy(-0.1)
        
        
    def check_collision(self, x, y, obj):
        return (x < obj.x + obj.size*0.75 and
                x + self.size*0.75 > obj.x and
                y < obj.y + obj.size*0.75 and
                y + self.size*0.75 > obj.y)
    
    
    def is_near(self, obj):
        return (abs(self.x - obj.x) <= max(self.size, obj.size) + 5 and
                abs(self.y - obj.y) <= max(self.size, obj.size) + 5)
        
        
    def interact(self, world):
        for tree in world.trees:
            if self.is_near(tree):
                if tree.chop():
                    self.inventory['wood'] += 1
                    if tree.wood == 0:
                        world.trees.remove(tree)
                return
            
        for stone in world.small_stones:
            if self.is_near(stone):
                self.inventory['stone'] += stone.stone
                world.small_stones.remove(stone)
                return
            

    def draw_inventory(self, screen):
        background = pygame.Surface((constantes.ANCHO, constantes.ALTO), pygame.SRCALPHA)
        background.fill((0, 0, 0, 128)) # Fondo semitransparente
        screen.blit(background, (0, 0)) # Dibujar el fondo de inventario  
        
        font = pygame.font.Font(None, 36)
        title = font.render("Inventory", True, constantes.WHITE)
        screen.blit(title, (constantes.ANCHO // 2 - title.get_width() // 2, 20)) # Título centrado
        
        item_font = pygame.font.Font(None, 24)
        y_offset = 80
        for item, quantity in self.inventory.items():
            if quantity > 0:
                screen.blit(self.item_images[item], (constantes.ANCHO // 2 - 60, y_offset))
                
                text = item_font.render(f"{item.capitalize()}: {quantity}", True, constantes.WHITE)
                screen.blit(text, (constantes.ANCHO // 2 + 10, y_offset + 15))
                y_offset += 60
                
        
        close_text = item_font.render("Press 'I' to close inventory", True, constantes.WHITE)
        screen.blit(close_text, (constantes.ANCHO // 2 - close_text.get_width() // 2, constantes.ALTO - 40))


    def update_energy(self, amount):
        self.energy = max(0, min(self.energy + amount, constantes.MAX_ENERGY))
        
        
    def update_food(self, amount):
        self.food = max(0, min(self.food + amount, constantes.MAX_FOOD))
        
    
    def update_thirst(self, amount):
        self.thirst = max(0, min(self.thirst + amount, constantes.MAX_THIRST))
        
        
    def draw_status_bars(self, screen):
        bar_width = 100
        bar_height = 10
        x_offset = 10
        y_offset = 10
        
        # Barra de energía
        pygame.draw.rect(screen, constantes.BAR_BACKGROUND, 
                        (x_offset, y_offset, bar_width, bar_height))
        
        pygame.draw.rect(screen, constantes.ENERGY_COLOR, 
                        (x_offset, y_offset, bar_width * (self.energy / constantes.MAX_ENERGY), bar_height))
        
        # Barra de comida
        y_offset += 15  
        pygame.draw.rect(screen, constantes.BAR_BACKGROUND, 
                        (x_offset, y_offset + 20, bar_width, bar_height))
        
        pygame.draw.rect(screen, constantes.FOOD_COLOR, 
                        (x_offset, y_offset + 20, bar_width * (self.food / constantes.MAX_FOOD), bar_height))
        
        # Barra de sed
        y_offset += 15
        pygame.draw.rect(screen, constantes.BAR_BACKGROUND, 
                        (x_offset, y_offset + 40, bar_width, bar_height))
        
        pygame.draw.rect(screen, constantes.THIRST_COLOR, 
                        (x_offset, y_offset + 40, bar_width * (self.thirst / constantes.MAX_THIRST), bar_height))
        

    def update_status(self):
        self.update_food(-1)   # La comida disminuye con el tiempo
        self.update_thirst(-2)  # La sed disminuye con el tiempo
        
        if self.food < constantes.MAX_FOOD * 0.2 or self.thirst < constantes.MAX_THIRST * 0.2:
            self.update_energy(-0.5)  # Pierde energía más rápido si tiene poca comida o sed
        else:
            self.update_energy(0.1)  # Pierde energía lentamente con el tiempo