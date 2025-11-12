"""
Módulo de manejo de imágenes
Gestiona la carga, modificación y guardado de imágenes
"""

import numpy as np
from PIL import Image
from pathlib import Path
import config


class ImageHandler:
    """Clase para manejar operaciones con imágenes"""
    
    def __init__(self):
        self.img_array = None          # Array de numpy con la imagen
        self.img_original = None       # Imagen original sin modificaciones
        self.historial = []            # Historial de cambios
    
    def cargar_imagen(self, ruta):
        """
        Carga una imagen desde la ruta especificada
        
        Args:
            ruta (str): Ruta del archivo de imagen
            
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        try:
            self.img_original = Image.open(ruta).convert("RGB")
            self.img_array = np.array(self.img_original)
            self.historial.clear()
            
            alto, ancho = self.img_array.shape[:2]
            nombre = Path(ruta).name
            total_pixeles = ancho * alto
            
            mensaje = (f"📷 {nombre} | Tamaño: {ancho} x {alto} px | "
                      f"Total píxeles: {total_pixeles:,}")
            
            return True, mensaje
            
        except Exception as e:
            return False, f"No se pudo cargar la imagen:\n{str(e)}"
    
    def guardar_imagen(self, ruta):
        """
        Guarda la imagen modificada en la ruta especificada
        
        Args:
            ruta (str): Ruta donde guardar la imagen
            
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        try:
            if self.img_array is None:
                return False, config.MSG_NO_IMAGE_TO_SAVE
            
            img_modificada = Image.fromarray(self.img_array)
            img_modificada.save(ruta)
            
            mensaje = f"Imagen guardada exitosamente en:\n{ruta}"
            return True, mensaje
            
        except Exception as e:
            return False, f"No se pudo guardar la imagen:\n{str(e)}"
    
    def modificar_pixel(self, x, y, r, g, b):
        """
        Modifica el color de un píxel específico
        
        Args:
            x, y (int): Coordenadas del píxel
            r, g, b (int): Valores RGB (0-255)
            
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        try:
            if self.img_array is None:
                return False, config.MSG_NO_IMAGE
            
            alto, ancho = self.img_array.shape[:2]
            
            # Validar coordenadas
            if not (0 <= x < ancho and 0 <= y < alto):
                mensaje = config.MSG_ERROR_OUT_OF_RANGE.format(ancho - 1, alto - 1)
                return False, mensaje
            
            # Validar valores RGB
            if not all(0 <= val <= 255 for val in [r, g, b]):
                return False, config.MSG_ERROR_RGB_RANGE
            
            # Guardar en historial antes de modificar
            self.historial.append(self.img_array.copy())
            if len(self.historial) > config.MAX_HISTORIAL:
                self.historial.pop(0)
            
            # Aplicar cambio
            self.img_array[y, x] = [r, g, b]
            
            mensaje = config.MSG_PIXEL_CHANGED.format(x, y, r, g, b)
            return True, mensaje
            
        except Exception as e:
            return False, f"Error al modificar píxel:\n{str(e)}"
    
    def deshacer(self):
        """
        Deshace el último cambio
        
        Returns:
            bool: True si se pudo deshacer, False si no hay historial
        """
        if len(self.historial) > 0:
            self.img_array = self.historial.pop()
            return True
        return False
    
    def restaurar_original(self):
        """
        Restaura la imagen original
        
        Returns:
            bool: True si se restauró, False si no hay imagen original
        """
        if self.img_original is not None:
            self.img_array = np.array(self.img_original)
            self.historial.clear()
            return True
        return False
    
    def obtener_imagen_actual(self):
        """
        Obtiene la imagen actual como objeto PIL Image
        
        Returns:
            Image: Imagen PIL o None si no hay imagen cargada
        """
        if self.img_array is not None:
            return Image.fromarray(self.img_array)
        return None
    
    def obtener_dimensiones(self):
        """
        Obtiene las dimensiones de la imagen actual
        
        Returns:
            tuple: (ancho, alto) o None si no hay imagen
        """
        if self.img_array is not None:
            alto, ancho = self.img_array.shape[:2]
            return ancho, alto
        return None
    
    def obtener_color_pixel(self, x, y):
        """
        Obtiene el color RGB de un píxel específico
        
        Args:
            x, y (int): Coordenadas del píxel
            
        Returns:
            tuple: (r, g, b) o None si está fuera de rango
        """
        if self.img_array is not None:
            alto, ancho = self.img_array.shape[:2]
            if 0 <= x < ancho and 0 <= y < alto:
                r, g, b = self.img_array[y, x]
                return r, g, b
        return None
    
    def modificar_pixeles_rectangulo(self, x1, y1, x2, y2, r, g, b):
        """
        Modifica múltiples píxeles en un área rectangular
        
        Args:
            x1, y1, x2, y2 (int): Coordenadas del rectángulo (esquinas)
            r, g, b (int): Valores RGB (0-255)
            
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        try:
            if self.img_array is None:
                return False, config.MSG_NO_IMAGE
            
            # Normalizar coordenadas
            x_min = min(x1, x2)
            x_max = max(x1, x2)
            y_min = min(y1, y2)
            y_max = max(y1, y2)
            
            alto, ancho = self.img_array.shape[:2]
            
            # Validar valores RGB
            if not all(0 <= val <= 255 for val in [r, g, b]):
                return False, config.MSG_ERROR_RGB_RANGE
            
            # Guardar en historial antes de modificar
            self.historial.append(self.img_array.copy())
            if len(self.historial) > config.MAX_HISTORIAL:
                self.historial.pop(0)
            
            # Aplicar cambio a todos los píxeles en el área
            x_min = max(0, x_min)
            x_max = min(ancho, x_max + 1)
            y_min = max(0, y_min)
            y_max = min(alto, y_max + 1)
            
            self.img_array[y_min:y_max, x_min:x_max] = [r, g, b]
            
            total_pixeles = (x_max - x_min) * (y_max - y_min)
            mensaje = f"✅ {total_pixeles} píxeles cambiados a RGB({r}, {g}, {b})"
            return True, mensaje
            
        except Exception as e:
            return False, f"Error al modificar píxeles:\n{str(e)}"
    
    def modificar_pixeles_circulo(self, x_centro, y_centro, radio, r, g, b):
        """
        Modifica múltiples píxeles en un área circular
        
        Args:
            x_centro, y_centro (int): Centro del círculo
            radio (int): Radio del círculo
            r, g, b (int): Valores RGB (0-255)
            
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        try:
            if self.img_array is None:
                return False, config.MSG_NO_IMAGE
            
            alto, ancho = self.img_array.shape[:2]
            
            # Validar valores RGB
            if not all(0 <= val <= 255 for val in [r, g, b]):
                return False, config.MSG_ERROR_RGB_RANGE
            
            # Guardar en historial
            self.historial.append(self.img_array.copy())
            if len(self.historial) > config.MAX_HISTORIAL:
                self.historial.pop(0)
            
            # Crear máscara circular
            contador = 0
            for y in range(max(0, y_centro - radio), min(alto, y_centro + radio + 1)):
                for x in range(max(0, x_centro - radio), min(ancho, x_centro + radio + 1)):
                    distancia = ((x - x_centro) ** 2 + (y - y_centro) ** 2) ** 0.5
                    if distancia <= radio:
                        self.img_array[y, x] = [r, g, b]
                        contador += 1
            
            mensaje = f"✅ {contador} píxeles cambiados en círculo"
            return True, mensaje
            
        except Exception as e:
            return False, f"Error al modificar píxeles:\n{str(e)}"
    
    def obtener_promedio_color_area(self, x1, y1, x2, y2):
        """
        Obtiene el color promedio de un área rectangular
        
        Args:
            x1, y1, x2, y2 (int): Coordenadas del rectángulo
            
        Returns:
            tuple: (r, g, b) o None si está fuera de rango
        """
        try:
            if self.img_array is None:
                return None
            
            # Normalizar coordenadas
            x_min = max(0, min(x1, x2))
            x_max = min(self.img_array.shape[1], max(x1, x2) + 1)
            y_min = max(0, min(y1, y2))
            y_max = min(self.img_array.shape[0], max(y1, y2) + 1)
            
            if x_max <= x_min or y_max <= y_min:
                return None
            
            area = self.img_array[y_min:y_max, x_min:x_max]
            promedio = area.mean(axis=(0, 1)).astype(int)
            
            return tuple(promedio[:3])
            
        except Exception:
            return None
