"""
Módulo principal del Editor de Imágenes
Integra todos los componentes y gestiona la lógica de la aplicación
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import config
from image_handler import ImageHandler
from ui_components import (FrameControles, LabelInfo, CanvasImagen, 
                          LabelCoordenadas, FrameEdicion, FrameSeleccionMultiple)


class EditorImagenes:
    """Clase principal del editor de imágenes"""
    
    def __init__(self, root):
        self.root = root
        self._configurar_ventana()
        
        # Inicializar manejador de imágenes
        self.image_handler = ImageHandler()
        
        # Crear componentes de UI
        self._crear_interfaz()
        self._configurar_estilos()
    
    def _configurar_ventana(self):
        """Configura las propiedades de la ventana principal"""
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.resizable(config.WINDOW_RESIZABLE, config.WINDOW_RESIZABLE)
        
        # Centrar ventana en pantalla
        self.root.update_idletasks()
        ancho_ventana = self.root.winfo_width()
        alto_ventana = self.root.winfo_height()
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        
        x = (ancho_pantalla - ancho_ventana) // 2
        y = (alto_pantalla - alto_ventana) // 2
        self.root.geometry(f"+{x}+{y}")
        
        # Establecer fondo
        self.root.configure(bg="#ecf0f1")
        
        # Icono (si existe)
        try:
            # Puedes agregar un icono aquí
            pass
        except:
            pass
    
    def _configurar_estilos(self):
        """Configura estilos para la interfaz"""
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use('clam')
    
    def _crear_interfaz(self):
        """Crea todos los componentes de la interfaz"""
        # Frame superior con controles
        self.frame_controles = FrameControles(self.root, {
            'cargar': self.cargar_imagen,
            'guardar': self.guardar_imagen,
            'deshacer': self.deshacer,
            'restaurar': self.restaurar_original
        })
        
        # Label de información
        self.label_info = LabelInfo(self.root)
        
        # Canvas para la imagen
        self.canvas_imagen = CanvasImagen(self.root, 
                                         self.click_canvas, 
                                         self.mostrar_coordenadas)
        
        # Label de coordenadas
        self.label_coords = LabelCoordenadas(self.root)
        
        # Frame de edición
        self.frame_edicion = FrameEdicion(self.root, 
                                         self.aplicar_cambio, 
                                         self.actualizar_preview_color)
        
        # Frame de selección múltiple
        self.frame_seleccion = FrameSeleccionMultiple(self.root,
                                                     self.aplicar_seleccion_multiple)
        
        # Variables para almacenar selección
        self.seleccion_activa = None  # (x1, y1, x2, y2) para rectángulo
        self.canvas_imagen.rect_id = None  # ID del rectángulo en canvas
        # Agendar verificación de widgets tras inicializar la ventana
        try:
            self.root.after(200, self._diagnostico_widgets)
        except Exception:
            pass


    def _diagnostico_widgets(self):
        """Imprime en consola información básica sobre widgets relevantes.
        Útil para diagnosticar por qué botones no se muestran en tiempo de ejecución.
        """
        try:
            # Contar botones en frame_seleccion
            botones = []
            for w in self.frame_seleccion.frame.winfo_children():
                for child in w.winfo_children():
                    if child.__class__.__name__ == 'Button':
                        botones.append(child)

            print('DEBUG: botones en FrameSeleccionMultiple =', len(botones))
            for i, b in enumerate(botones):
                try:
                    txt = b.cget('text')
                except Exception:
                    txt = '<no-text>'
                print(f"DEBUG: boton[{i}] mapped={b.winfo_ismapped()} text={repr(txt)}")
        except Exception as e:
            print('DEBUG: error diagnostico widgets:', e)
    
    # ========== MÉTODOS DE CARGA Y GUARDADO ==========
    
    def cargar_imagen(self):
        """Carga una imagen desde el disco"""
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=config.IMAGE_FORMATS
        )
        
        if ruta:
            exito, mensaje = self.image_handler.cargar_imagen(ruta)
            
            if exito:
                self.label_info.actualizar(mensaje)
                imagen = self.image_handler.obtener_imagen_actual()
                self.canvas_imagen.mostrar_imagen(imagen)
            else:
                messagebox.showerror("Error", mensaje)
    
    def guardar_imagen(self):
        """Guarda la imagen modificada"""
        if self.image_handler.img_array is None:
            messagebox.showwarning("Advertencia", config.MSG_NO_IMAGE_TO_SAVE)
            return
        
        ruta = filedialog.asksaveasfilename(
            defaultextension=config.DEFAULT_SAVE_EXTENSION,
            filetypes=config.SAVE_FORMATS
        )
        
        if ruta:
            exito, mensaje = self.image_handler.guardar_imagen(ruta)
            
            if exito:
                messagebox.showinfo("💾 Guardado", mensaje)
            else:
                messagebox.showerror("Error", mensaje)
    
    # ========== MÉTODOS DE EDICIÓN ==========
    
    def aplicar_cambio(self):
        """Aplica el cambio de color al píxel especificado"""
        try:
            valores = self.frame_edicion.obtener_valores()
            x = int(valores['x'])
            y = int(valores['y'])
            r = int(valores['r'])
            g = int(valores['g'])
            b = int(valores['b'])
            
            exito, mensaje = self.image_handler.modificar_pixel(x, y, r, g, b)
            
            if exito:
                imagen = self.image_handler.obtener_imagen_actual()
                self.canvas_imagen.mostrar_imagen(imagen)
                messagebox.showinfo("✓ Éxito", mensaje)
            else:
                messagebox.showerror("Error de validación", mensaje)
                
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")
    
    def deshacer(self):
        """Deshace el último cambio"""
        if self.image_handler.deshacer():
            imagen = self.image_handler.obtener_imagen_actual()
            self.canvas_imagen.mostrar_imagen(imagen)
        else:
            messagebox.showinfo("Info", config.MSG_NO_UNDO)
    
    def restaurar_original(self):
        """Restaura la imagen original"""
        if self.image_handler.restaurar_original():
            imagen = self.image_handler.obtener_imagen_actual()
            self.canvas_imagen.mostrar_imagen(imagen)
            messagebox.showinfo("Restaurado", config.MSG_RESTORED)
        else:
            messagebox.showwarning("Advertencia", config.MSG_NO_IMAGE_WARNING)
    
    # ========== MÉTODOS DE INTERACCIÓN ==========
    
    def click_canvas(self, event):
        """Captura las coordenadas al hacer clic en el canvas"""
        if self.image_handler.img_array is None:
            return
        
        x_img, y_img = self.canvas_imagen.canvas_a_coordenadas_imagen(
            event.x, event.y
        )
        
        if x_img is None or y_img is None:
            return
        
        dimensiones = self.image_handler.obtener_dimensiones()
        if dimensiones is None:
            return
        
        ancho, alto = dimensiones
        
        if 0 <= x_img < ancho and 0 <= y_img < alto:
            color = self.image_handler.obtener_color_pixel(x_img, y_img)
            if color:
                r, g, b = color
                self.frame_edicion.establecer_valores(x_img, y_img, r, g, b)
                self.actualizar_preview_color()
    
    def mostrar_coordenadas(self, event):
        """Muestra las coordenadas en tiempo real al mover el mouse"""
        if self.image_handler.img_array is None:
            return
        
        x_img, y_img = self.canvas_imagen.canvas_a_coordenadas_imagen(
            event.x, event.y
        )
        
        if x_img is None or y_img is None:
            return
        
        dimensiones = self.image_handler.obtener_dimensiones()
        if dimensiones is None:
            return
        
        ancho, alto = dimensiones
        
        if 0 <= x_img < ancho and 0 <= y_img < alto:
            color = self.image_handler.obtener_color_pixel(x_img, y_img)
            if color:
                r, g, b = color
                texto = f"Posición: X={x_img}, Y={y_img} | Color: RGB({r}, {g}, {b})"
                self.label_coords.actualizar(texto)
        else:
            self.label_coords.actualizar("Posición: fuera de imagen")
    
    def actualizar_preview_color(self):
        """Actualiza el preview del color RGB ingresado"""
        self.frame_edicion.actualizar_preview_color()
    
    # ========== MÉTODOS DE SELECCIÓN MÚLTIPLE ==========
    
    def aplicar_seleccion_multiple(self):
        """Aplica el color a la selección múltiple"""
        if self.seleccion_activa is None:
            messagebox.showwarning("Advertencia", "⚠️ Selecciona una área primero")
            return
        
        config_sel = self.frame_seleccion.obtener_configuracion()
        
        x1, y1, x2, y2 = self.seleccion_activa
        r, g, b = config_sel['r'], config_sel['g'], config_sel['b']
        
        try:
            if config_sel['modo'] == 'rectangulo':
                exito, mensaje = self.image_handler.modificar_pixeles_rectangulo(x1, y1, x2, y2, r, g, b)
            elif config_sel['modo'] == 'circulo':
                # Para círculo: usar el punto como centro
                radio = config_sel['tamaño']
                x_centro = (x1 + x2) // 2
                y_centro = (y1 + y2) // 2
                exito, mensaje = self.image_handler.modificar_pixeles_circulo(x_centro, y_centro, radio, r, g, b)
            else:
                exito = False
                mensaje = "Modo no soportado"
            
            if exito:
                imagen = self.image_handler.obtener_imagen_actual()
                self.canvas_imagen.mostrar_imagen(imagen)
                messagebox.showinfo("✓ Éxito", mensaje)
                self._limpiar_seleccion_visual()
            else:
                messagebox.showerror("Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar selección:\n{str(e)}")
    
    def iniciar_seleccion_rectangulo(self, event):
        """Inicia la selección rectangular"""
        if self.image_handler.img_array is None:
            return
        
        self.seleccion_inicio = (event.x, event.y)
    
    def extender_seleccion_rectangulo(self, event):
        """Extiende la selección rectangular mientras se arrastra"""
        if not hasattr(self, 'seleccion_inicio') or self.seleccion_inicio is None:
            return
        
        # Dibujar rectángulo provisional en el canvas
        if self.canvas_imagen.rect_id is not None:
            self.canvas_imagen.canvas.delete(self.canvas_imagen.rect_id)
        
        x1, y1 = self.seleccion_inicio
        x2, y2 = event.x, event.y
        
        # Dibujar rectángulo en el canvas
        self.canvas_imagen.rect_id = self.canvas_imagen.canvas.create_rectangle(
            x1, y1, x2, y2, outline="#3498db", width=2, dash=(4, 4)
        )
    
    def finalizar_seleccion_rectangulo(self, event):
        """Finaliza la selección rectangular"""
        if not hasattr(self, 'seleccion_inicio') or self.seleccion_inicio is None:
            return
        
        x1_canvas, y1_canvas = self.seleccion_inicio
        x2_canvas, y2_canvas = event.x, event.y
        
        # Convertir a coordenadas de imagen
        x1_img, y1_img = self.canvas_imagen.canvas_a_coordenadas_imagen(x1_canvas, y1_canvas)
        x2_img, y2_img = self.canvas_imagen.canvas_a_coordenadas_imagen(x2_canvas, y2_canvas)
        
        if x1_img is not None and y1_img is not None and x2_img is not None and y2_img is not None:
            self.seleccion_activa = (x1_img, y1_img, x2_img, y2_img)
            
            # Mostrar información de la selección
            ancho = abs(x2_img - x1_img)
            alto = abs(y2_img - y1_img)
            area = ancho * alto
            
            messagebox.showinfo("✅ Selección", 
                              f"Área seleccionada: {ancho}x{alto}\n"
                              f"Total píxeles: {area}")
        
        self.seleccion_inicio = None
    
    def _limpiar_seleccion_visual(self):
        """Limpia la visualización de la selección"""
        if self.canvas_imagen.rect_id is not None:
            self.canvas_imagen.canvas.delete(self.canvas_imagen.rect_id)
            self.canvas_imagen.rect_id = None
        self.seleccion_activa = None


def main():
    """Función principal para iniciar la aplicación"""
    root = tk.Tk()
    app = EditorImagenes(root)
    root.mainloop()


if __name__ == "__main__":
    main()
