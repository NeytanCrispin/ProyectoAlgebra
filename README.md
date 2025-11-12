# Editor de Imágenes - Estructura Modular

## 📁 Estructura del Proyecto

```
.
├── main_editor.py          # Archivo principal (punto de entrada)
├── config.py               # Configuraciones y constantes
├── image_handler.py        # Lógica de manejo de imágenes
├── ui_components.py        # Componentes de interfaz gráfica
└── algebra lineal.py       # Versión monolítica (original)
```

---

## 📄 Descripción de cada módulo

### 1. **config.py** 🔧
**Propósito:** Centralizar todas las configuraciones y constantes

**Contiene:**
- Configuración de ventana (tamaño, título, etc.)
- Colores de la interfaz
- Formatos de imagen soportados
- Dimensiones del canvas
- Mensajes de la aplicación
- Límites del historial

**Uso:** `import config` y acceder a constantes como `config.WINDOW_WIDTH`

---

### 2. **image_handler.py** 🖼️
**Propósito:** Gestionar todas las operaciones con imágenes (carga, edición, guardado)

**Clases:**
- `ImageHandler`: Maneja imágenes y sus modificaciones

**Métodos principales:**
- `cargar_imagen(ruta)` - Carga una imagen
- `guardar_imagen(ruta)` - Guarda la imagen modificada
- `modificar_pixel(x, y, r, g, b)` - Cambia el color de un píxel
- `deshacer()` - Deshace el último cambio
- `restaurar_original()` - Vuelve a la imagen original
- `obtener_color_pixel(x, y)` - Obtiene el color de un píxel

**Ventajas:**
- Separación de lógica de negocio
- Fácil de testear
- Reutilizable en otras aplicaciones

---

### 3. **ui_components.py** 🎨
**Propósito:** Definir componentes visuales reutilizables

**Clases:**
- `FrameControles` - Botones principales (Cargar, Guardar, Deshacer, Restaurar)
- `LabelInfo` - Muestra información de la imagen
- `CanvasImagen` - Canvas donde se muestra la imagen
- `LabelCoordenadas` - Muestra coordenadas del mouse
- `FrameEdicion` - Panel para editar píxeles (X, Y, RGB)

**Ventajas:**
- Componentes reutilizables
- Fácil de personalizar
- Código más limpio

---

### 4. **main_editor.py** 🚀
**Propósito:** Orquestar todos los módulos y manejar eventos

**Clase principal:**
- `EditorImagenes` - Coordina toda la aplicación

**Métodos principales:**
- Métodos de carga y guardado
- Métodos de edición (aplicar cambio, deshacer, restaurar)
- Métodos de interacción (clicks, movimiento del mouse)

**Flujo:**
1. Inicializa los componentes de UI
2. Crea instancia de ImageHandler
3. Conecta eventos con callbacks

---

### 5. **algebra lineal.py** 📝
**Propósito:** Versión monolítica original (referencia)

**Estado:** Funcional pero no modular

---

## 🔄 Cómo fluye la información

```
Usuario → Canvas
  ↓
  Evento (click, movimiento)
  ↓
main_editor.py (maneja evento)
  ↓
ui_components.py (actualiza UI) + image_handler.py (procesa datos)
  ↓
config.py (proporciona constantes)
  ↓
Canvas actualizado
```

---

## 🛠️ Cómo usar cada módulo

### Ejecutar la aplicación:
```python
python main_editor.py
```

### Usar solo ImageHandler en otro programa:
```python
from image_handler import ImageHandler

handler = ImageHandler()
exito, mensaje = handler.cargar_imagen("imagen.jpg")
handler.modificar_pixel(100, 100, 255, 0, 0)  # Píxel rojo
exito, msg = handler.guardar_imagen("salida.jpg")
```

### Cambiar configuración:
- Edita `config.py`
- Cambios se aplican automáticamente en toda la app

---

## ✨ Ventajas de la estructura modular

| Aspecto | Ventaja |
|--------|---------|
| **Mantenibilidad** | Fácil encontrar y modificar código específico |
| **Testing** | Cada módulo se puede testear por separado |
| **Reutilización** | ImageHandler se puede usar en otros proyectos |
| **Escalabilidad** | Fácil agregar nuevas funcionalidades |
| **Claridad** | Responsabilidades bien definidas |
| **Colaboración** | Equipos pueden trabajar en módulos diferentes |

---

## 🔧 Cómo hacer modificaciones

### Quiero cambiar colores:
→ Edita `config.py` (sección COLORES)

### Quiero agregar funcionalidad de imagen:
→ Agrega método a la clase `ImageHandler` en `image_handler.py`

### Quiero cambiar la interfaz:
→ Edita `ui_components.py`

### Quiero cambiar la lógica de eventos:
→ Edita métodos en `main_editor.py`

---

## 📊 Estadísticas del código

| Módulo | Líneas | Responsabilidad |
|--------|--------|-----------------|
| config.py | ~50 | Configuración |
| image_handler.py | ~150 | Lógica de imágenes |
| ui_components.py | ~200 | Interfaz visual |
| main_editor.py | ~150 | Orquestación |
| **Total modular** | ~550 | - |
| algebra lineal.py | ~350 | Monolítico |

---

## 🚀 Próximas mejoras sugeridas

1. **Tests unitarios** - Testear cada módulo
2. **Filtros de imagen** - Agregar métodos a ImageHandler
3. **Historial visual** - Mostrar thumbnails de cambios
4. **Temas** - Permitir cambiar temas de colores
5. **Configuración de usuario** - Guardar preferencias
6. **Documentación automática** - Generar docs con Sphinx

---

**¡Ahora el código es modular, fácil de mantener y muy flexible!** 🎉
