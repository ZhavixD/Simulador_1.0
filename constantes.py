# tamanos
ANCHO, ALTO = 1280, 720
PLAYER = 70
GRASS  = 64
TREE   = 64 
SMALL_STONE = 20

# ANIMACIONES
BASIC_FRAMES = 6
IDLE_DOWN  = 0
IDLE_RIGHT = 1
IDLE_UP    = 2
WALK_DOWN  = 3
WALK_RIGHT = 4
WALK_UP    = 5
FRAME_SIZE = 32
ANIMATION_DELAY = 100  # en milisegundos
RUNNING_ANIMATION_DELAY = 50

#colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
BROWN = (139, 69, 19)
GRAY  = (128, 128, 128)

# BARRAS DE ESTADO
MAX_ENERGY = 100
MAX_FOOD   = 100
MAX_THIRST = 100
MAX_STAMINA = 100

# Colores para barras de estado
ENERGY_COLOR   = (255, 215, 0)  # Dorado
FOOD_COLOR     = (210, 153, 34) # Marrón
THIRST_COLOR   = (30, 144, 255) # Azul dodger
STAMINA_COLOR  = (100, 226, 80) # Verde pastel
BAR_BACKGROUND = (100, 100, 100)   # Fondo gris oscuro

# INTERVALO DE TIEMPO
STATUS_UPDATE_INTERVAL = 1000  # en milisegundos

# SISTEMA dia/noche
DAY_LENGTH   = 240000 # Druracion del dia completo en ms (24 segundos)
DAWN_TIME    = 60000  # Amanecer a las 6:00
MORNING_TIME = 80000  # Mañana completa a l;as 8:00
DUSK_TIME    = 180000 # Atardecer a las 18:00
MIDNIGHT     = 240000 # Medianoche (00:00)
MAX_DARKNESS = 2100   # Nivel maximo de oscuridad (0-255)

# Col ores para iluminaciön
NIGHT_COLOR     = (20, 20, 50)    # Color azul oscuro para la noche
DAY_COLOR       = (255, 255, 255) # Color blanco para eI dia
DAWN_DUSK_COLOR = (255, 193, 137) # Color anaranjado para amanecer/atardecer

# Velocidades de dismision de estados
FOOD_DECREASE_RATE   = 0.1  # Velocidad de disminucion de comida
THIRST_DECREASE_RATE = 0.2  # Velocidad de disminucion de sed
ENERGY_DECREASE_RATE = 0.5 # Velocidad de disminucion de energia
ENERGY_INCREASE_RATE = 0.01 # Velocidad de aumento de energia
MOVEMENT_ENERGY_COST = 0.01 # Costo de movimiento

# Nuevas constantes para correr
WALK_SPEED = 5
RUN_SPEED  = 8
STAMINA_DECREASE_RATE = 0.05
STAMINA_INCREASE_RATE = 0.02
RUN_FOOD_DECREASE_MULTIPLIER = 2.0
RUN_THIRST_DECREASE_MULTIPLIER = 2.0

# Inventory constantes
SLOT_SIZE    = 64
HOTBAR_SLOTS = 8
INVENTORY_ROWS = 4
INVENTORY_COLS = 5
MARGIN = 10

# Hotbar position (siempre visible abajo)
HOTBAR_Y = ALTO - SLOT_SIZE - MARGIN
HOTBAR_X = (ANCHO - (SLOT_SIZE * HOTBAR_SLOTS)) // 2

# Main inventory position (siempre visible arriba)
INVENTORY_X = (ANCHO - (SLOT_SIZE * INVENTORY_COLS)) // 2
INVENTORY_Y = (ALTO  - (SLOT_SIZE * INVENTORY_ROWS)) // 2

# Colors for inventory 
SLOT_COLOR  = (139, 139, 139) # Gris oscuro
SLOT_BORDER = (100, 100, 100) # Gris claro
SLOT_HOVER  = (160, 160, 160) # Gris medio