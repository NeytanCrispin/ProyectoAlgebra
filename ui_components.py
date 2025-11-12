"""
Módulo de componentes de interfaz gráfica
Define todos los widgets y componentes visuales - VERSIÓN MEJORADA
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import config


class FrameControles:
    """Frame superior con botones de control principales"""
    
    def __init__(self, parent, callbacks):
        """
        Args:
            parent: Widget padre (root window)
            callbacks: Dict con callbacks {'cargar': func, 'guardar': func, ...}
        """
        # Frame con gradiente simulado
        self.frame = tk.Frame(parent, bg=config.COLOR_BG_TOP, padx=15, pady=12)
        self.frame.pack(fill=tk.X, ipady=5)
        
        # Agregar título/separador
        titulo = tk.Label(self.frame, text="CONTROLES PRINCIPALES", 
                         bg=config.COLOR_BG_TOP, fg="white", 
                         font=("Arial", 9, "bold"))
        titulo.pack(side=tk.LEFT, padx=5)
        
        # Separador visual
        sep = tk.Frame(self.frame, bg="#1a252f", height=2)
        sep.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, ipady=1)
        
        # Botones con estilo mejorado
        botones_info = [
            ("📂 Cargar", callbacks['cargar'], "Cargar una imagen"),
            ("💾 Guardar", callbacks['guardar'], "Guardar cambios"),
            ("↩️ Deshacer", callbacks['deshacer'], "Deshacer último cambio"),
            ("🔄 Restaurar", callbacks['restaurar'], "Volver a original"),
        ]
        
        for texto, comando, tooltip in botones_info:
            btn = tk.Button(self.frame, text=texto, command=comando,
                           font=("Arial", 9, "bold"), 
                           bg="#34495e", fg="white",
                           padx=12, pady=6,
                           relief=tk.RAISED, bd=1,
                           cursor="hand2",
                           activebackground="#2c3e50",
                           activeforeground="#3498db")
            btn.pack(side=tk.LEFT, padx=4)
            self._agregar_tooltip(btn, tooltip)
    
    def _agregar_tooltip(self, widget, texto):
        """Agrega tooltip (ayuda) al pasar sobre el widget"""
        def mostrar_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=texto, background="#ffffe0", 
                           foreground="black", relief=tk.SOLID, bd=1,
                           font=("Arial", 8))
            label.pack()
            
            def ocultar_tooltip():
                tooltip.destroy()
            widget.tooltip = tooltip
            tooltip.after(3000, ocultar_tooltip)
        
        widget.bind("<Enter>", mostrar_tooltip)


class LabelInfo:
    """Label para mostrar información de la imagen - MEJORADO"""
    
    def __init__(self, parent):
        # Frame con fondo
        self.frame = tk.Frame(parent, bg="#ecf0f1", relief=tk.SUNKEN, bd=1)
        self.frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.label = tk.Label(self.frame, text=config.MSG_NO_IMAGE,
                             font=("Arial", 9), fg=config.COLOR_TEXT_INFO, 
                             pady=8, bg="#ecf0f1", wraplength=600, justify=tk.LEFT)
        self.label.pack(fill=tk.X, padx=10)
    
    def actualizar(self, texto):
        """Actualiza el texto del label con animación"""
        self.label.config(text=texto, fg="#27ae60")  # Verde cuando se carga
        # Volver a color normal después de 2 segundos
        self.label.after(2000, lambda: self.label.config(fg=config.COLOR_TEXT_INFO))


class LabelCoordenadas:
    """Label pequeño para mostrar coordenadas y color bajo el canvas"""

    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#ecf0f1")
        self.frame.pack(fill=tk.X, padx=5)
        self.label = tk.Label(self.frame, text="Posición: - ", font=("Arial", 9), bg="#ecf0f1")
        self.label.pack(anchor=tk.W, padx=10)

    def actualizar(self, texto):
        self.label.config(text=texto)


class CanvasImagen:
    """Canvas para mostrar la imagen - MEJORADO"""
    
    def __init__(self, parent, click_callback, motion_callback):
        """
        Args:
            parent: Widget padre
            click_callback: Función al hacer clic
            motion_callback: Función al mover el mouse
        """
        # Frame contenedor con sombra
        self.frame_container = tk.Frame(parent, bg="#2c3e50", padx=3, pady=3)
        self.frame_container.pack(pady=15, padx=10)
        
        # Canvas con border mejorado
        self.canvas = tk.Canvas(parent, width=config.CANVAS_WIDTH, height=config.CANVAS_HEIGHT,
                               bg=config.COLOR_BG_CANVAS, highlightthickness=3,
                               highlightbackground="#34495e", cursor="crosshair")
        self.canvas.pack(in_=self.frame_container, padx=3, pady=3)
        self.canvas.bind("<Button-1>", click_callback)
        self.canvas.bind("<Motion>", motion_callback)
        self.canvas.bind("<Button-3>", self.click_derecho)  # Click derecho para más opciones
        
        self.img_display = None
        self.display_ratio = 1.0
        self.rect_id = None  # Para almacenar ID del rectángulo de selección
        self.dibujar_rejilla_inicial()
    
    def dibujar_rejilla_inicial(self):
        """Dibuja una rejilla de referencia cuando no hay imagen"""
        self.canvas.delete("all")
        # Dibuja línea punteada como referencia
        for i in range(0, config.CANVAS_WIDTH, 50):
            self.canvas.create_line(i, 0, i, config.CANVAS_HEIGHT, 
                                   fill="#bdc3c7", dash=(2, 2), width=1)
        for i in range(0, config.CANVAS_HEIGHT, 50):
            self.canvas.create_line(0, i, config.CANVAS_WIDTH, i, 
                                   fill="#bdc3c7", dash=(2, 2), width=1)
        # Texto central
        self.canvas.create_text(config.CANVAS_CENTER_X, config.CANVAS_CENTER_Y,
                               text="Carga una imagen aquí", font=("Arial", 12, "italic"),
                               fill="#95a5a6")
    
    def mostrar_imagen(self, imagen):
        """
        Muestra la imagen en el canvas con ajuste proporcional
        
        Args:
            imagen: Objeto PIL Image
        """
        max_size = config.CANVAS_WIDTH
        width, height = imagen.size
        ratio = min(max_size / width, max_size / height)
        nuevo_width = int(width * ratio)
        nuevo_height = int(height * ratio)
        
        self.img_display = imagen.resize((nuevo_width, nuevo_height), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(self.img_display)
        
        self.canvas.delete("all")
        self.canvas.img = img_tk
        self.canvas.create_image(config.CANVAS_CENTER_X, config.CANVAS_CENTER_Y, image=img_tk)
        
        self.display_ratio = ratio
    
    def click_derecho(self, event):
        """Menú contextual al hacer click derecho"""
        pass  # Puede implementarse más adelante
class FrameEdicion:
    """Frame para edición de píxeles - MEJORADO"""

    def __init__(self, parent, aplicar_callback, preview_callback):
        """Inicializa el panel de edición de píxel.

        Args:
            parent: widget padre
            aplicar_callback: función a ejecutar al aplicar cambio
            preview_callback: función para actualizar vista previa
        """
        self.frame = tk.LabelFrame(parent, text="Edición de Píxel",
                                   font=("Arial", 11, "bold"), padx=20, pady=15,
                                   bg="#ecf0f1", relief=tk.GROOVE, bd=2)
        self.frame.pack(pady=12, padx=10, fill=tk.X)

        # Fila 1 - coordenadas
        row1 = tk.Frame(self.frame, bg="#ecf0f1")
        row1.pack(pady=8, fill=tk.X)

        tk.Label(row1, text="Coordenadas:", font=("Arial", 9, "bold"),
                 bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT, padx=5)

        tk.Label(row1, text="X:", font=("Arial", 9, "bold"), bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        self.entry_x = tk.Entry(row1, width=6, font=("Arial", 10, "bold"), bg="white", relief=tk.SUNKEN, bd=1)
        self.entry_x.pack(side=tk.LEFT, padx=2)

        tk.Label(row1, text="Y:", font=("Arial", 9, "bold"), bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        self.entry_y = tk.Entry(row1, width=6, font=("Arial", 10, "bold"), bg="white", relief=tk.SUNKEN, bd=1)
        self.entry_y.pack(side=tk.LEFT, padx=2)

        # Fila 2 - RGB
        row2 = tk.Frame(self.frame, bg="#ecf0f1")
        row2.pack(pady=8, fill=tk.X)

        tk.Label(row2, text="Color RGB:", font=("Arial", 9, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT, padx=5)

        self.sliders = {}
        self.entries_rgb = {}
        for nombre, color, label in [("R", config.COLOR_RED, "R"), ("G", config.COLOR_GREEN, "G"), ("B", config.COLOR_BLUE, "B")]:
            sub_frame = tk.Frame(row2, bg="#ecf0f1")
            sub_frame.pack(side=tk.LEFT, padx=8)

            tk.Label(sub_frame, text=f"{label} {nombre}:", font=("Arial", 9, "bold"), bg="#ecf0f1", fg=color).pack()

            slider_frame = tk.Frame(sub_frame, bg="#ecf0f1")
            slider_frame.pack(fill=tk.X, pady=2)

            slider = tk.Scale(slider_frame, from_=0, to=255, orient=tk.HORIZONTAL, bg="white", fg=color, highlightthickness=0, length=80,
                              command=lambda val, n=nombre: self._en_cambio_slider(n, val, preview_callback))
            slider.pack(side=tk.LEFT, padx=2)
            self.sliders[nombre] = slider

            entry = tk.Entry(slider_frame, width=4, font=("Arial", 10, "bold"), bg="white", relief=tk.SUNKEN, bd=1)
            entry.pack(side=tk.LEFT, padx=2)
            entry.bind("<KeyRelease>", lambda e, n=nombre, p=preview_callback: self._en_cambio_entry(n, e, p))
            self.entries_rgb[nombre] = entry

        # Fila 3 - preview y botones
        row3 = tk.Frame(self.frame, bg="#ecf0f1")
        row3.pack(pady=10, fill=tk.X)

        preview_frame = tk.Frame(row3, bg="#ecf0f1")
        preview_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(preview_frame, text="Vista Previa:", font=("Arial", 9, "bold"), bg="#ecf0f1", fg="#2c3e50").pack()

        self.color_preview = tk.Canvas(preview_frame, width=80, height=60, bg="#ffffff", highlightthickness=2, highlightbackground="#95a5a6", cursor="hand2")
        self.color_preview.pack(pady=5)
        self.color_preview.create_rectangle(2, 2, 78, 58, fill="#ffffff")

        # Botones (guardados como atributos)
        self.btn_aplicar = tk.Button(row3, text="Aplicar Cambio", command=aplicar_callback, font=("Arial", 10, "bold"), bg="#27ae60", fg="white", padx=20, pady=10, relief=tk.RAISED, bd=2, cursor="hand2", activebackground="#229954", activeforeground="#ffffff")
        self.btn_aplicar.pack(side=tk.LEFT, padx=10, expand=True)

        self.btn_limpiar = tk.Button(row3, text="Limpiar", command=self.limpiar_campos, font=("Arial", 10), bg="#95a5a6", fg="white", padx=15, pady=10, relief=tk.RAISED, bd=2, cursor="hand2", activebackground="#7f8c8d")
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)

        # Vincular Enter
        for entry in [self.entry_x, self.entry_y]:
            entry.bind("<Return>", lambda e: aplicar_callback())

    def _en_cambio_slider(self, nombre, valor, callback):
        """Sincroniza slider con entry"""
        self.entries_rgb[nombre].delete(0, tk.END)
        self.entries_rgb[nombre].insert(0, str(int(float(valor))))
        self.sliders[nombre].set(int(float(valor)))
        callback()

    def _en_cambio_entry(self, nombre, event, callback):
        """Sincroniza entry con slider"""
        try:
            val = int(self.entries_rgb[nombre].get() or 0)
            val = max(0, min(255, val))
            self.sliders[nombre].set(val)
            callback()
        except ValueError:
            pass

    def limpiar_campos(self):
        """Limpia todos los campos de entrada"""
        self.entry_x.delete(0, tk.END)
        self.entry_y.delete(0, tk.END)
        for slider in self.sliders.values():
            slider.set(0)
        for entry in self.entries_rgb.values():
            entry.delete(0, tk.END)
            entry.insert(0, "0")
        self.color_preview.delete("all")
        self.color_preview.create_rectangle(2, 2, 78, 58, fill="#ffffff")

    def obtener_valores(self):
        return {
            'x': self.entry_x.get(),
            'y': self.entry_y.get(),
            'r': self.entries_rgb['R'].get(),
            'g': self.entries_rgb['G'].get(),
            'b': self.entries_rgb['B'].get()
        }

    def establecer_valores(self, x, y, r, g, b):
        self.entry_x.delete(0, tk.END)
        self.entry_x.insert(0, str(x))
        self.entry_y.delete(0, tk.END)
        self.entry_y.insert(0, str(y))
        self.sliders['R'].set(r)
        self.sliders['G'].set(g)
        self.sliders['B'].set(b)
        self.entries_rgb['R'].delete(0, tk.END)
        self.entries_rgb['R'].insert(0, str(r))
        self.entries_rgb['G'].delete(0, tk.END)
        self.entries_rgb['G'].insert(0, str(g))
        self.entries_rgb['B'].delete(0, tk.END)
        self.entries_rgb['B'].insert(0, str(b))

    def actualizar_preview_color(self):
        try:
            r = int(self.entries_rgb['R'].get() or 0)
            g = int(self.entries_rgb['G'].get() or 0)
            b = int(self.entries_rgb['B'].get() or 0)
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.color_preview.delete("all")
            self.color_preview.create_rectangle(2, 2, 78, 58, fill=color)
            hex_text = f"{color.upper()}\nRGB({r},{g},{b})"
            self.color_preview.create_text(40, 29, text=hex_text, font=("Courier", 7, "bold"), fill="white" if (r+g+b) < 384 else "black")
        except ValueError:
            self.color_preview.delete("all")
            self.color_preview.create_rectangle(2, 2, 78, 58, fill="#ffffff")


class FrameSeleccionMultiple:
    """Frame para seleccionar múltiples píxeles - NUEVO"""
    
    def __init__(self, parent, aplicar_callback):
        """
        Args:
            parent: Widget padre
            aplicar_callback: Función al aplicar cambio
        """
        self.frame = tk.LabelFrame(parent, text="🎯 Selección Múltiple",
                                  font=("Arial", 11, "bold"), padx=20, pady=15,
                                  bg="#ecf0f1", relief=tk.GROOVE, bd=2)
        self.frame.pack(pady=12, padx=10, fill=tk.X)
        
        # ===== FILA 1: MODO DE SELECCIÓN =====
        row1 = tk.Frame(self.frame, bg="#ecf0f1")
        row1.pack(pady=8, fill=tk.X)
        
        tk.Label(row1, text="📐 Modo de Selección:", font=("Arial", 9, "bold"),
                bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT, padx=5)
        
        self.modo_seleccion = tk.StringVar(value="rectangulo")
        
        modos = [("🟫 Rectángulo", "rectangulo"), 
                ("⭕ Círculo", "circulo"),
                ("🎨 Pincel", "pincel")]
        
        for texto, valor in modos:
            rb = tk.Radiobutton(row1, text=texto, variable=self.modo_seleccion, 
                              value=valor, bg="#ecf0f1", activebackground="#ecf0f1",
                              font=("Arial", 9))
            rb.pack(side=tk.LEFT, padx=8)
        
        # ===== FILA 2: HERRAMIENTAS =====
        row2 = tk.Frame(self.frame, bg="#ecf0f1")
        row2.pack(pady=8, fill=tk.X)
        
        tk.Label(row2, text="🎛️ Herramientas:", font=("Arial", 9, "bold"),
                bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT, padx=5)
        
        # Tamaño/radio
        tk.Label(row2, text="Tamaño:", font=("Arial", 9), bg="#ecf0f1").pack(side=tk.LEFT, padx=5)
        self.slider_tamaño = tk.Scale(row2, from_=1, to=100, orient=tk.HORIZONTAL,
                                     bg="white", fg="#3498db", highlightthickness=0, length=100)
        self.slider_tamaño.set(10)
        self.slider_tamaño.pack(side=tk.LEFT, padx=2)
        
        # Label para mostrar tamaño
        self.lbl_tamaño = tk.Label(row2, text="10px", font=("Arial", 9, "bold"),
                                  bg="#ecf0f1", fg="#3498db", width=6)
        self.lbl_tamaño.pack(side=tk.LEFT, padx=2)
        self.slider_tamaño.config(command=self._actualizar_tamaño)
        
        # ===== FILA 3: COLOR RGB =====
        row3 = tk.Frame(self.frame, bg="#ecf0f1")
        row3.pack(pady=8, fill=tk.X)
        
        tk.Label(row3, text="🎨 Color:", font=("Arial", 9, "bold"),
                bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT, padx=5)
        
        # Sliders RGB compactos
        for nombre, color, emoji in [("R", "#e74c3c", "🔴"), 
                                      ("G", "#27ae60", "🟢"), 
                                      ("B", "#3498db", "🔵")]:
            sub_frame = tk.Frame(row3, bg="#ecf0f1")
            sub_frame.pack(side=tk.LEFT, padx=5)
            
            tk.Label(sub_frame, text=emoji, font=("Arial", 9, "bold"),
                    bg="#ecf0f1").pack(side=tk.LEFT)
            
            slider = tk.Scale(sub_frame, from_=0, to=255, orient=tk.HORIZONTAL,
                            bg="white", fg=color, highlightthickness=0, length=60)
            slider.set(128)
            slider.pack(side=tk.LEFT, padx=2)
            
            setattr(self, f'slider_{nombre.lower()}', slider)
        
        # ===== FILA 4: BOTONES =====
        row4 = tk.Frame(self.frame, bg="#ecf0f1")
        row4.pack(pady=10, fill=tk.X)
        
        # Botón aplicar
        btn_aplicar = tk.Button(row4, text="Aplicar a Selección",
                               command=aplicar_callback,
                               font=("Arial", 10, "bold"),
                               bg="#27ae60", fg="white",
                               padx=20, pady=8,
                               relief=tk.RAISED, bd=2,
                               cursor="hand2",
                               activebackground="#229954")
        btn_aplicar.pack(side=tk.LEFT, padx=5)

        # Botón limpiar selección
        btn_limpiar = tk.Button(row4, text="Limpiar Selección",
                               command=self.limpiar_seleccion,
                               font=("Arial", 10),
                               bg="#e74c3c", fg="white",
                               padx=15, pady=8,
                               relief=tk.RAISED, bd=2,
                               cursor="hand2",
                               activebackground="#c0392b")
        btn_limpiar.pack(side=tk.LEFT, padx=5)

        # Botón usar color promedio
        btn_promedio = tk.Button(row4, text="Color Promedio",
                                command=self.usar_color_promedio,
                                font=("Arial", 10),
                                bg="#9b59b6", fg="white",
                                padx=15, pady=8,
                                relief=tk.RAISED, bd=2,
                                cursor="hand2",
                                activebackground="#8e44ad")
        btn_promedio.pack(side=tk.LEFT, padx=5)
    
    def _actualizar_tamaño(self, valor):
        """Actualiza el label del tamaño"""
        self.lbl_tamaño.config(text=f"{int(float(valor))}px")
    
    def obtener_configuracion(self):
        """Obtiene configuración actual"""
        return {
            'modo': self.modo_seleccion.get(),
            'tamaño': int(self.slider_tamaño.get()),
            'r': int(self.slider_r.get()),
            'g': int(self.slider_g.get()),
            'b': int(self.slider_b.get())
        }
    
    def limpiar_seleccion(self):
        """Limpia la selección"""
        pass  # Se implementa en main_editor.py
    
    def usar_color_promedio(self):
        """Usa color promedio de la selección"""
        pass  # Se implementa en main_editor.py
    
    def establecer_color(self, r, g, b):
        """Establece el color RGB en los sliders"""
        self.slider_r.set(r)
        self.slider_g.set(g)
        self.slider_b.set(b)