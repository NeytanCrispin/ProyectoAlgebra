import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
from pathlib import Path


class EditorImagenes:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imágenes - Versión Mejorada")
        self.root.geometry("700x650")
        self.root.resizable(False, False)

        # Variables de estado
        self.img_array = None
        self.img_original = None
        self.img_display = None
        self.historial = []
        self.max_historial = 10

        self._crear_interfaz()
        self._configurar_estilos()

    def _configurar_estilos(self):
        """Configura estilos para la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')

    def _crear_interfaz(self):
        """Crea todos los widgets de la interfaz"""
        # Frame superior - Controles principales
        frame_top = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        frame_top.pack(fill=tk.X)

        ttk.Button(frame_top, text="📂 Cargar Imagen",
                   command=self.cargar_imagen).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_top, text="💾 Guardar",
                   command=self.guardar_imagen).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_top, text="↩️ Deshacer",
                   command=self.deshacer).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_top, text="🔄 Restaurar",
                   command=self.restaurar_original).pack(side=tk.LEFT, padx=5)

        # Label de información
        self.lbl_info = tk.Label(self.root, text="No hay imagen cargada",
                                 font=("Arial", 10), fg="#34495e", pady=5)
        self.lbl_info.pack()

        # Canvas para mostrar la imagen
        self.canvas = tk.Canvas(self.root, width=400, height=400,
                                bg="#ecf0f1", highlightthickness=2,
                                highlightbackground="#95a5a6")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.click_canvas)
        self.canvas.bind("<Motion>", self.mostrar_coordenadas)

        # Label para coordenadas en tiempo real
        self.lbl_coords = tk.Label(self.root, text="Posición: ---, ---",
                                   font=("Courier", 9), fg="#7f8c8d")
        self.lbl_coords.pack()

        # Frame de controles de edición
        frame_edit = tk.LabelFrame(self.root, text="Edición de Píxel",
                                   font=("Arial", 10, "bold"), padx=15, pady=10)
        frame_edit.pack(pady=10, padx=20    , fill=tk.X)

        # Inputs organizados
        row1 = tk.Frame(frame_edit)
        row1.pack(pady=5)

        tk.Label(row1, text="X:", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        self.entry_x = tk.Entry(row1, width=8, font=("Arial", 10))
        self.entry_x.pack(side=tk.LEFT, padx=5)

        tk.Label(row1, text="Y:", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        self.entry_y = tk.Entry(row1, width=8, font=("Arial", 10))
        self.entry_y.pack(side=tk.LEFT, padx=5)

        row2 = tk.Frame(frame_edit)
        row2.pack(pady=5)

        tk.Label(row2, text="R:", font=("Arial", 9), fg="#e74c3c").pack(side=tk.LEFT, padx=5)
        self.entry_r = tk.Entry(row2, width=8, font=("Arial", 10))
        self.entry_r.pack(side=tk.LEFT, padx=5)

        tk.Label(row2, text="G:", font=("Arial", 9), fg="#27ae60").pack(side=tk.LEFT, padx=5)
        self.entry_g = tk.Entry(row2, width=8, font=("Arial", 10))
        self.entry_g.pack(side=tk.LEFT, padx=5)

        tk.Label(row2, text="B:", font=("Arial", 9), fg="#3498db").pack(side=tk.LEFT, padx=5)
        self.entry_b = tk.Entry(row2, width=8, font=("Arial", 10))
        self.entry_b.pack(side=tk.LEFT, padx=5)

        # Preview del color y botón
        row3 = tk.Frame(frame_edit)
        row3.pack(pady=10)

        tk.Label(row3, text="Vista previa:", font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        self.color_preview = tk.Canvas(row3, width=60, height=35,
                                       bg="#ffffff", highlightthickness=1)
        self.color_preview.pack(side=tk.LEFT, padx=5)

        ttk.Button(row3, text="✏️ Aplicar Cambio",
                   command=self.aplicar_cambio).pack(side=tk.LEFT, padx=10)

        # Vincular eventos para actualizar preview
        for entry in [self.entry_r, self.entry_g, self.entry_b]:
            entry.bind("<KeyRelease>", lambda e: self.actualizar_preview_color())

        # Bind Enter para aplicar cambio rápido
        for entry in [self.entry_x, self.entry_y, self.entry_r, self.entry_g, self.entry_b]:
            entry.bind("<Return>", lambda e: self.aplicar_cambio())

    def actualizar_preview_color(self):
        """Muestra un preview del color RGB ingresado"""
        try:
            r = int(self.entry_r.get() or 0)
            g = int(self.entry_g.get() or 0)
            b = int(self.entry_b.get() or 0)

            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            color = f'#{r:02x}{g:02x}{b:02x}'
            self.color_preview.configure(bg=color)
        except ValueError:
            self.color_preview.configure(bg="#ffffff")

    def guardar_en_historial(self):
        """Guarda el estado actual en el historial"""
        if self.img_array is not None:
            self.historial.append(self.img_array.copy())
            if len(self.historial) > self.max_historial:
                self.historial.pop(0)

    def deshacer(self):
        """Deshace el último cambio"""
        if len(self.historial) > 0:
            self.img_array = self.historial.pop()
            img_modificada = Image.fromarray(self.img_array)
            self.mostrar_imagen(img_modificada)
        else:
            messagebox.showinfo("Info", "No hay más acciones para deshacer")

    def restaurar_original(self):
        """Restaura la imagen original"""
        if self.img_original is not None:
            self.img_array = np.array(self.img_original)
            self.historial.clear()
            self.mostrar_imagen(self.img_original)
            messagebox.showinfo("Restaurado", "Imagen restaurada al original")
        else:
            messagebox.showwarning("Advertencia", "No hay imagen cargada")

    def cargar_imagen(self):
        """Carga una imagen desde el disco"""
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Todos los archivos", "*.*")
            ]
        )

        if ruta:
            try:
                self.img_original = Image.open(ruta).convert("RGB")
                self.img_array = np.array(self.img_original)
                self.historial.clear()

                alto, ancho = self.img_array.shape[:2]
                nombre = Path(ruta).name
                self.lbl_info.config(
                    text=f"📷 {nombre} | Tamaño: {ancho} x {alto} px | "
                         f"Total píxeles: {ancho * alto:,}"
                )

                self.mostrar_imagen(self.img_original)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{str(e)}")

    def mostrar_imagen(self, imagen):
        """Muestra la imagen en el canvas con ajuste proporcional"""
        # Calcular tamaño proporcional
        max_size = 400
        width, height = imagen.size
        ratio = min(max_size / width, max_size / height)
        nuevo_width = int(width * ratio)
        nuevo_height = int(height * ratio)

        self.img_display = imagen.resize((nuevo_width, nuevo_height), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(self.img_display)

        self.canvas.delete("all")
        self.canvas.img = img_tk
        self.canvas.create_image(200, 200, image=img_tk)

        # Guardar el ratio para conversión de coordenadas
        self.display_ratio = ratio

    def click_canvas(self, event):
        """Captura las coordenadas al hacer clic en el canvas"""
        if self.img_array is not None and self.img_display is not None:
            # Convertir coordenadas del canvas a coordenadas de la imagen original
            x_canvas = event.x - (400 - self.img_display.width) // 2
            y_canvas = event.y - (400 - self.img_display.height) // 2

            x_img = int(x_canvas / self.display_ratio)
            y_img = int(y_canvas / self.display_ratio)

            alto, ancho = self.img_array.shape[:2]

            if 0 <= x_img < ancho and 0 <= y_img < alto:
                self.entry_x.delete(0, tk.END)
                self.entry_x.insert(0, str(x_img))
                self.entry_y.delete(0, tk.END)
                self.entry_y.insert(0, str(y_img))

                # Mostrar el color actual del píxel
                r, g, b = self.img_array[y_img, x_img]
                self.entry_r.delete(0, tk.END)
                self.entry_r.insert(0, str(r))
                self.entry_g.delete(0, tk.END)
                self.entry_g.insert(0, str(g))
                self.entry_b.delete(0, tk.END)
                self.entry_b.insert(0, str(b))
                self.actualizar_preview_color()

    def mostrar_coordenadas(self, event):
        """Muestra las coordenadas en tiempo real al mover el mouse"""
        if self.img_array is not None and self.img_display is not None:
            x_canvas = event.x - (400 - self.img_display.width) // 2
            y_canvas = event.y - (400 - self.img_display.height) // 2

            x_img = int(x_canvas / self.display_ratio)
            y_img = int(y_canvas / self.display_ratio)

            alto, ancho = self.img_array.shape[:2]

            if 0 <= x_img < ancho and 0 <= y_img < alto:
                r, g, b = self.img_array[y_img, x_img]
                self.lbl_coords.config(
                    text=f"Posición: X={x_img}, Y={y_img} | "
                         f"Color: RGB({r}, {g}, {b})"
                )
            else:
                self.lbl_coords.config(text="Posición: fuera de imagen")

    def aplicar_cambio(self):
        """Aplica el cambio de color al píxel especificado"""
        try:
            x = int(self.entry_x.get())
            y = int(self.entry_y.get())
            r = int(self.entry_r.get())
            g = int(self.entry_g.get())
            b = int(self.entry_b.get())

            if self.img_array is None:
                raise ValueError("No hay imagen cargada")

            # Validar rangos
            alto, ancho = self.img_array.shape[:2]
            if not (0 <= x < ancho and 0 <= y < alto):
                raise ValueError(f"Coordenadas fuera de rango. "
                                 f"Máximo: X={ancho - 1}, Y={alto - 1}")

            if not all(0 <= val <= 255 for val in [r, g, b]):
                raise ValueError("Los valores RGB deben estar entre 0 y 255")

            # Guardar en historial antes de modificar
            self.guardar_en_historial()

            # Aplicar cambio
            self.img_array[y, x] = [r, g, b]
            img_modificada = Image.fromarray(self.img_array)
            self.mostrar_imagen(img_modificada)

            messagebox.showinfo("✓ Éxito",
                                f"Píxel ({x}, {y}) cambiado a RGB({r}, {g}, {b})")

        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado:\n{str(e)}")

    def guardar_imagen(self):
        """Guarda la imagen modificada"""
        if self.img_array is not None:
            img_modificada = Image.fromarray(self.img_array)
            ruta = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG", "*.png"),
                    ("JPEG", "*.jpg"),
                    ("BMP", "*.bmp"),
                    ("Todos los archivos", "*.*")
                ]
            )

            if ruta:
                try:
                    img_modificada.save(ruta)
                    messagebox.showinfo("💾 Guardado",
                                        f"Imagen guardada exitosamente en:\n{ruta}")
                except Exception as e:
                    messagebox.showerror("Error",
                                         f"No se pudo guardar la imagen:\n{str(e)}")
        else:
            messagebox.showwarning("Advertencia",
                                   "No hay imagen para guardar")


if __name__ == "__main__":
    root = tk.Tk()
    app = EditorImagenes(root)
    root.mainloop()