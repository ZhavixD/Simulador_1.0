import pygame
import constantes
import os
from constantes import *

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = {"wood": 0, "stone": 0}
        
        # Cargar la hoja de animaciones
        image_path = os.path.join('assets', 'images', 'characters', 'Player.png')
        self.sheet = pygame.image.load(image_path).convert_alpha()
        
        # Animation properties
        self.frame_size = FRAME_SIZE
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = ANIMATION_DELAY
        self.current_state   = IDLE_DOWN
        self.moving      = False
        self.facing_left = False
        self.is_running  = False
        
        # Load all animations frames
        self.animations = self.load_animation()
        
        self.item_images = {
            "wood": self.load_items_image("wood.png"),
            "stone": self.load_items_image("small_stone.png")        
        }
        
        self.energy  = constantes.MAX_ENERGY
        self.food    = constantes.MAX_FOOD
        self.thirst  = constantes.MAX_THIRST
        self.stamina = constantes.MAX_STAMINA
        
        
    def load_animation(self):
        animations = {}
        for state in range(6): # 6 estados
            frames = []
            for frame in range(BASIC_FRAMES): # 6 frames por estado
                surface = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
                surface.blit(self.sheet, (0,0), 
                            (frame * self.frame_size, 
                             state * self.frame_size, 
                            self.frame_size,
                            self.frame_size))
                
                if constantes.PLAYER != self.frame_size:
                    surface = pygame.transform.scale(surface, (constantes.PLAYER, constantes.PLAYER))
                frames.append(surface)
            animations[state] = frames
        return animations
    
    
    def update_animation(self):
        current_time = pygame.time.get_ticks()
        # Ajustar la velocidad de la animación segun si esta corriendo o caminando
        animation_speed = RUNNING_ANIMATION_DELAY if self.is_running else ANIMATION_DELAY
        if current_time - self.animation_timer > animation_speed:
            self.animation_timer = current_time
            self.animation_frame = (self.animation_frame + 1) % 6
            
    
        
    def load_items_image(self, filename):
        path = os.path.join('assets', 'images', 'objects', filename)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (40, 40))
        
    def draw(self, screen, camera_x, camera_y):
        # Calcular la posición del personaje en la pantalla
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        
        current_frame = self.animations[self.current_state][self.animation_frame] # Obtener el frame actual de la animación
        if self.facing_left:
            current_frame = pygame.transform.flip(current_frame, True, False) # Voltear horizontalmente si mira a la izquierda
        screen.blit(current_frame, (screen_x, screen_y)) # Dibujar el frame en la posición del personaje
    
    # Movimiento y colisiones ================================================================
    def move(self, dx, dy, world):
        self.moving = (dx != 0 or dy != 0)
        
        if self.moving:
            # Ajustar velocidad segun si corre o camina
            speed_multiplier = RUN_SPEED if self.is_running and self.is_running and self.stamina > 0 else WALK_SPEED   
            dx *= speed_multiplier / WALK_SPEED
            dy *= speed_multiplier / WALK_SPEED
            
            if dy > 0:
                self.current_state = WALK_DOWN
                self.facing_left   = False
            elif dy < 0:
                self.current_state = WALK_UP
                self.facing_left   = False
            elif dx > 0:
                self.current_state = WALK_RIGHT
                self.facing_left   = False
            elif dx < 0:
                self.current_state = WALK_RIGHT
                self.facing_left   = True 
        else:
            if self.current_state == WALK_DOWN:
                self.current_state = IDLE_DOWN
            elif self.current_state == WALK_UP:
                self.current_state = IDLE_UP
            elif self.current_state == WALK_RIGHT:
                self.current_state = IDLE_RIGHT

        
        new_x = self.x + dx
        new_y = self.y + dy
# =========================================================================================        
        for tree in world.trees:
            if self.check_collision(new_x, new_y, tree):
                self.moving = False
                return  # Colisión con un árbol, no mover
        
        self.x = new_x
        self.y = new_y
        
        self.update_animation()
        
        # Cuando se mueve pierde energia
        if self.moving:
            if self.is_running and self.stamina > 0:
                self.update_stamina(-STAMINA_DECREASE_RATE)
                self.update_energy(-MOVEMENT_ENERGY_COST * 2)
            else:
                self.update_energy(-MOVEMENT_ENERGY_COST)
                if not self.moving:
                    self.update_stamina(STAMINA_INCREASE_RATE)
        
        
    def check_collision(self, x, y, obj):
        return (x < obj.x + obj.size*0.75 and
                x + constantes.PLAYER*0.75 > obj.x and
                y < obj.y + obj.size*0.75 and
                y + constantes.PLAYER*0.75 > obj.y)
    
    
    def is_near(self, obj):
        return (abs(self.x - obj.x) <= max(constantes.PLAYER, obj.size) + 5 and
                abs(self.y - obj.y) <= max(constantes.PLAYER, obj.size) + 5)
        
        
    def interact(self, world):
        for tree in world.trees:
            if self.is_near(tree):
                if tree.chop():
                    self.inventory['wood'] += 1
                return
            
        for stone in world.small_stones:
            if self.is_near(stone): 
                if stone.collect():
                    
                    self.inventory['stone'] += 1
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

    def update_stamina(self, amount):
        self.stamina = max(0, min(self.stamina + amount, constantes.MAX_STAMINA))   
        
    def draw_status_bars(self, screen):
        bar_width  = 100
        bar_height = 10
        y_offset   = 10
        x_offset   = 10
        
        # Barra de energía
        pygame.draw.rect(screen, constantes.BAR_BACKGROUND, 
                        (x_offset, y_offset, bar_width, bar_height))
        
        pygame.draw.rect(screen, constantes.ENERGY_COLOR, 
                        (x_offset, y_offset, bar_width * (self.energy / constantes.MAX_ENERGY), bar_height))
        
        # Barra de comida
        y_offset += 15  
        pygame.draw.rect(screen, constantes.BAR_BACKGROUND,
                        (x_offset, y_offset, bar_width, bar_height))
        
        pygame.draw.rect(screen, constantes.FOOD_COLOR, 
                        (x_offset, y_offset, bar_width * (self.food / constantes.MAX_FOOD), bar_height))
        
        # Barra de sed
        y_offset += 15
        pygame.draw.rect(screen, constantes.BAR_BACKGROUND,
                        (x_offset, y_offset, bar_width, bar_height))
        
        pygame.draw.rect(screen, constantes.THIRST_COLOR, 
                        (x_offset, y_offset, bar_width * (self.thirst / constantes.MAX_THIRST), bar_height))
        
        # Barra de estamina
        y_offset += 15
        pygame.draw.rect(screen, constantes.BAR_BACKGROUND, 
                        (x_offset, y_offset, bar_width, bar_height))
        
        pygame.draw.rect(screen, constantes.STAMINA_COLOR, 
                        (x_offset, y_offset, bar_width * (self.stamina / constantes.MAX_STAMINA), bar_height))
        

    def update_status(self):
        # Aplicar muiltiplicadores si esta corriendo
        food_rate   = FOOD_DECREASE_RATE   * (RUN_FOOD_DECREASE_MULTIPLIER if self.is_running else 1)
        thirst_rate = THIRST_DECREASE_RATE * (RUN_THIRST_DECREASE_MULTIPLIER if self.is_running else 1)
        
        self.update_food(-constantes.FOOD_DECREASE_RATE)   # La comida disminuye con el tiempo
        self.update_thirst(- constantes.THIRST_DECREASE_RATE)  # La sed disminuye con el tiempo
        
        if self.food < constantes.MAX_FOOD * 0.2 or self.thirst < constantes.MAX_THIRST * 0.2:
            self.update_energy(- constantes.ENERGY_DECREASE_RATE)  # Pierde energía más rápido si tiene poca comida o sed
        else:
            self.update_energy(constantes.ENERGY_INCREASE_RATE)