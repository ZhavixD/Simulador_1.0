# tamanos
ANCHO, ALTO = 800, 600
PLAYER = 40
GRASS  = 64
TREE   = 64 
SMALL_STONE = 20


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

# Colores para barras de estado
ENERGY_COLOR   = (255, 215, 0)  # Dorado
FOOD_COLOR     = (34, 139, 34)  # Verde bosque
THIRST_COLOR   = (30, 144, 255) # Azul dodger
BAR_BACKGROUND = (100, 100, 100)   # Fondo gris oscuro

# INTERVALO DE TIEMPO
STATUS_UPDATE_INTERVAL = 1000  # en milisegundos

# SISTEMA dia/noche
DAY_LENGTH   = 24000 # Druracion del dia completo en ms (24 segundos)
DAWN_TIME    = 6000  # Amanecer a las 6:00
MORNING_TIME = 8000  # Mañana completa a l;as 8:00
DUSK_TIME    = 18000 # Atardecer a las 18:00
MIDNIGHT     = 24000 # Medianoche (00:00)
MAX_DARKNESS = 180   # Nivel maximo de oscuridad (0-255)

# Col ores para iluminaciön
NIGHT_COLOR     = (20, 20, 50)    # Color azul oscuro para la noche
DAY_COLOR       = (255, 255, 255) # Color blanco para eI dia
DAWN_DUSK_COLOR = (255, 193, 137) # Color anaranjado para amanecer/atardecer