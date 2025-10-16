import pygame
import constantes
import os

class InventoryItem:
    def __init__(self, name, image_path, quantity = 1):
        self.name = name
        self.quantity = quantity
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constantes.SLOT_SIZE - 10, constantes.SLOT_SIZE - 10))
        self.dragging = False
        self. drag_offset = (0, 0)
        
        
class Inventory:
    def __init__(self):
        self.hotbar = [None] * constantes.HOTBAR_SLOTS
        self.inventory = [[None for _ in range(constantes.INVENTORY_COLS)] for _ in range(constantes.INVENTORY_ROWS)]
        self.dragged_item = None
        self.font = pygame.font.Font(None, 24)
        
        # Cargar las imagenes de los items
        self.item_images = {
            'wood': os.path.join('assets', 'images', 'objects', 'wood.png'),
            'stone': os.path.join('assets', 'images', 'objects', 'small_stone.png')
        } 
    
    
    def add_item(self, item_name, quantity = 1):
        # Primero intentar apilar en el hotbar
        for i, slot in enumerate(self.hotbar):
            if slot and slot.name == item_name:
                slot.quantity += quantity
                return True
            
        # Luego intentar apilar en el inventario principal
        for row in range(constantes.INVENTORY_ROWS):
            for col in range(constantes.INVENTORY_COLS):
                if self.inventory[row][col] and self.inventory[row][col].name == item_name:
                    self.inventory[row][col].quantity += quantity
                    return True
                
        # Buscar slot vacio en el hotbar
        for i, slot in enumerate (self.hotbar):
            if slot is None:
                self.hotbar[i] = InventoryItem(item_name, self.item_images[item_name], quantity)
                return True
            
        # Buscar slot vacio en el inventario principal
        for row in range(constantes.INVENTORY_ROWS):
            for col in range(constantes.INVENTORY_COLS):
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = InventoryItem(item_name, self.item_images[item_name], quantity)
                    return True
        return False
    
    def draw(self, screen, show_inventory = False):
        # Dibujar hotbar (siempre visible abajo)
        self._draw_hotbar(screen)
        
        # Dibujar inventario principal si esta abierto
        if show_inventory:
            # Fondo transparente
            background = pygame.Surface((constantes.ANCHO, constantes.ALTO), pygame.SRCALPHA)
            background.fill((0, 0, 0, 128)) # Fondo semitransparente
            screen.blit(background, (0, 0)) # Dibujar el fondo de inventario
            
            self._draw_main_inventory(screen)
            
        # Dibujar item siendo arrastrado al final para que apareza encima de todo
        if self.dragged_item:
            mouse_pos = pygame.mouse.get_pos()
            screen.blit(self.dragged_item.image, 
                        (mouse_pos[0] - self.dragged_item.drag_offset[0],
                        mouse_pos [1] - self.dragged_item.drag_offset[1]))
            
            if self.dragged_item.quantity > 1:
                text = self.font.render(str(self.dragged_item.quantity), True, constantes.WHITE)
                text_rect = text.get_rect()
                text_rect.bottomright = (mouse_pos[0] + self.dragged_item.image.get_width() // 2 - 5,
                                         mouse_pos[1] + self.dragged_item.image.get_height() // 2 - 5)
                screen.blit(text, text_rect)
                
                
    def _draw_hotbar(self, screen):
        for i in range (constantes.HOTBAR_SLOTS):
            x = constantes.HOTBAR_X + (i * constantes.SLOT_SIZE)
            y = constantes.HOTBAR_Y
            
            # Dibujar fondo del slot
            pygame.draw.rect(screen, constantes.SLOT_BORDER,
                            (x, y, constantes.SLOT_SIZE, constantes.SLOT_SIZE))
            
            pygame.draw.rect(screen, constantes.SLOT_COLOR,
                            (x + 2, y + 2, constantes.SLOT_SIZE - 4, constantes.SLOT_SIZE - 4))
            
            # Dibujar item si existe
            if self.hotbar[i]:
                self._draw_item(screen, self.hotbar[i], x, y)
                
                
    def _draw_main_inventory(self, screen):
        for row in range(constantes.INVENTORY_ROWS):
            for col in range(constantes.INVENTORY_COLS):
                x = constantes.INVENTORY_X + (col * constantes.SLOT_SIZE)
                y = constantes.INVENTORY_Y + (row * constantes.SLOT_SIZE)
                
                # Dibujar fondo del slot
                pygame.draw.rect(screen, constantes.SLOT_BORDER,
                                (x, y, constantes.SLOT_SIZE, constantes.SLOT_SIZE))
                
                pygame.draw.rect(screen, constantes.SLOT_COLOR,
                                (x + 2, y + 2, constantes.SLOT_SIZE - 4, constantes.SLOT_SIZE - 4))
                
                # Dibujar item si existe
                if self.inventory[row][col]:
                    self._draw_item(screen, self.inventory[row][col], x, y)
                    
    
    def _draw_item(self, screen, item, x, y):
        # Centrar el item en el slot
        item_x = x + constantes.SLOT_SIZE - item.image.get_width() // 2
        item_y = y + constantes.SLOT_SIZE - item.image.get_height() // 2
        
        screen.blit(item.image, (item_x, item_y))
        
        # Dibujar cantidad
        if item.quantity > 1:
            text = self.font.render(str(item.quantity), True, constantes.WHITE)
            text_rect = text.get_rect()
            text_rect.bottomright = (x + constantes.SLOT_SIZE - 5, y + constantes.SLOT_SIZE - 5)
            screen.blit(text, text_rect)
            
            
    def handle_click(self, pos, button, show_inventory = False):
        mouse_x, mouse_y = pos

        # Verificar click en hotbar
        if constantes.HOTBAR_Y <= mouse_y <= constantes.HOTBAR_Y + constantes.SLOT_SIZE:
            slot_index = (mouse_x - constantes.HOTBAR_X) // constantes.SLOT_SIZE
            if 0 <= slot_index < constantes.HOTBAR_SLOTS:
                self._handle_slot_click(button, self.hotbar, slot_index,
                                        constantes.HOTBAR_X + (slot_index * constantes.SLOT_SIZE),
                                        constantes.HOTBAR_Y)
                return True
            
        # Verificar click en inventario principal si esta abierto
        if show_inventory and constantes.INVENTORY_Y <= mouse_y <= constantes.INVENTORY_Y + (
                constantes.INVENTORY_ROWS * constantes.SLOT_SIZE):
            row = (mouse_y - constantes.INVENTORY_Y) // constantes.SLOT_SIZE
            col = (mouse_x - constantes.INVENTORY_X) // constantes.SLOT_SIZE
            if (0 <= row < constantes.INVENTORY_ROWS and 0 <= col < constantes.INVENTORY_COLS):
                self._handle_grid_slot_click(button, row, col,
                                            constantes.INVENTORY_X + (col * constantes.SLOT_SIZE),
                                            constantes.INVENTORY_Y + (row * constantes.SLOT_SIZE))
                return True
        
        # Click fuera del inventario
        if self.dragged_item and button == 1:
            self._return_dragged_item()
            
        return False
    
    
    def _handle_slot_click(self, button, slot_list, index, slot_x, slot_y):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos
        
        if button == 1: # Click izquierdo
            if self.dragged_item:
                # Soltar item
                if slot_list[index] is None:
                    slot_list[index] = self.dragged_item
                else:
                    # Intercambiar items
                    slot_list[index], self.dragged_item = self.dragged_item, slot_list[index]
                    return
                
                self.dragged_item = None
            elif slot_list[index]:
                # Comenzar a arrastrar item
                self.dragged_item = slot_list[index]
                slot_list[index] = None
                # Calcular offset para el arrastre centrado
                item_rect = self.dragged_item.image.get_rect()
                item_rect.x = slot_x
                item_rect.y = slot_y
                self.dragged_item.drag_offset =(mouse_x - item_rect.centerx, 
                                                mouse_y - item_rect.centery) 
    
    def _handle_grid_slot_click(self, button, row, col, slot_x, slot_y):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x, mouse_y = mouse_pos
        
        if button == 1: # Click izquierdo
            if self.dragged_item:
                # Soltar item
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = self.dragged_item
                else:
                    # Intercambiar items
                    self.inventory[row][col], self.dragged_item = self.dragged_item, self.inventory[row][col]
                    return
                
                self.dragged_item = None
            elif self.inventory[row][col]:
                # Comenzar a arrastrar item
                self.dragged_item = self.inventory[row][col]
                self.inventory[row][col] = None
                # Calcular offset para el arrastre centrado
                item_rect = self.dragged_item.image.get_rect()
                item_rect.x = slot_x
                item_rect.y = slot_y
                self.dragged_item.drag_offset =(mouse_x - item_rect.centerx,  
                                                mouse_y - item_rect.centery) 
                
    
    def _return_dragged_item(self):
        # Intentar devolver al hotbar primero
        for i, slot in enumerate(self.hotbar):
            if slot is None:
                self.hotbar[i] = self.dragged_item
                self.dragged_item = None
                return
        
        # Luego intentar devolver al inventario principal
        for row in range(constantes.INVENTORY_ROWS):
            for col in range(constantes.INVENTORY_COLS):
                if self.inventory[row][col] is None:
                    self.inventory[row][col] = self.dragged_item
                    self.dragged_item = None
                    return
        