"""
Archivo de configuración del Editor de Imágenes
Aquí están todas las constantes y configuraciones
"""

# ========== CONFIGURACIÓN DE VENTANA ==========
WINDOW_TITLE = "🎨 Editor de Imágenes Profesional"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW_RESIZABLE = False

# ========== COLORES ==========
COLOR_BG_TOP = "#2c3e50"
COLOR_BG_CANVAS = "#ecf0f1"
COLOR_BORDER_CANVAS = "#95a5a6"
COLOR_TEXT_INFO = "#34495e"
COLOR_TEXT_COORDS = "#7f8c8d"
COLOR_RED = "#e74c3c"
COLOR_GREEN = "#27ae60"
COLOR_BLUE = "#3498db"

# ========== FORMATOS DE IMAGEN ==========
IMAGE_FORMATS = [
    ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif"),
    ("PNG", "*.png"),
    ("JPEG", "*.jpg *.jpeg"),
    ("Todos los archivos", "*.*")
]

SAVE_FORMATS = [
    ("PNG", "*.png"),
    ("JPEG", "*.jpg"),
    ("BMP", "*.bmp"),
    ("Todos los archivos", "*.*")
]

DEFAULT_SAVE_EXTENSION = ".png"

# ========== CANVAS ==========
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
CANVAS_CENTER_X = 200
CANVAS_CENTER_Y = 200

# ========== HISTORIAL ==========
MAX_HISTORIAL = 10

# ========== MENSAJES ==========
MSG_NO_IMAGE = "No hay imagen cargada"
MSG_NO_IMAGE_WARNING = "No hay imagen cargada"
MSG_NO_IMAGE_TO_SAVE = "No hay imagen para guardar"
MSG_NO_UNDO = "No hay más acciones para deshacer"
MSG_RESTORED = "Imagen restaurada al original"
MSG_PIXEL_CHANGED = "Píxel ({}, {}) cambiado a RGB({}, {}, {})"
MSG_ERROR_OUT_OF_RANGE = "Coordenadas fuera de rango. Máximo: X={}, Y={}"
MSG_ERROR_RGB_RANGE = "Los valores RGB deben estar entre 0 y 255"
MSG_SAVED_SUCCESS = "Imagen guardada exitosamente en:\n{}"

# ========== SELECCIÓN MÚLTIPLE ==========
MSG_SELECCION_INICIADA = "Arrastra para seleccionar un área"
MSG_SELECCION_COMPLETADA = "✅ Selección completada. Usa 'Aplicar a Selección' para cambiar color"
MSG_NO_SELECCION = "⚠️ Selecciona una área primero"
MSG_PIXELES_CAMBIADOS = "✅ {} píxeles cambiados a RGB({}, {}, {})"
