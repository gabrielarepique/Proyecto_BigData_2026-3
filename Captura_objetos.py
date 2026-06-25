import cv2
import os
import imutils
import tkinter as tk
from tkinter import messagebox
import time

base_path = # Ruta base de tu proyecto

# ---- PALETA DE COLORES PREMIUM (ESTILO LOGIN MODERNO) ----
COLOR_AZUL_OSCURO = "#1E40AF"  # Azul principal corporativo
COLOR_AZUL_CLARO = "#60A5FA"   # Azul claro para gradientes visuales
COLOR_FONDO_DER = "#FFFFFF"    # Blanco puro para inputs y paneles
COLOR_FONDO_IZQ = "#2563EB"    # Fondo azul plano para el panel izquierdo
COLOR_TEXTO_MAIN = "#1E293B"   # Gris oscuro/Casi negro para alta legibilidad
COLOR_TEXTO_MUTED = "#64748B"  # Gris intermedio para subtítulos e instrucciones
COLOR_ENTRY_BORDER = "#CBD5E1" # Borde sutil para los campos de texto
COLOR_BOTON_HOVER = "#1D4ED8"  # Color de acción al pasar el mouse

FONT_TITULO = ("Segoe UI", 16, "bold")
FONT_SUBTITULO = ("Segoe UI", 9, "normal")
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_BUTTON = ("Segoe UI", 10, "bold")

def crear_carpeta(nombre):
    ruta_carpeta = os.path.join(base_path, nombre)
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        print(f"Carpeta creada: {ruta_carpeta}")
    else:
        print(f"Carpeta ya existente: {ruta_carpeta}")
    return ruta_carpeta

def capturar_datos(nombre, num_imagenes=300):
    ruta_carpeta = crear_carpeta(nombre)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    count = 0

    recuadro_w, recuadro_h = 300, 300
    x_start = (640 - recuadro_w) // 2
    y_start = 100  

    print("Presiona 's' para detener la captura.")
    print("Presiona 'c' para capturar una imagen dentro del recuadro.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al acceder a la cámara.")
            break

        frame = imutils.resize(frame, width=640)
        aux_frame = frame.copy()

        # Dibujar el recuadro de enfoque
        cv2.rectangle(frame, (x_start, y_start), (x_start + recuadro_w, y_start + recuadro_h), (0, 255, 0), 2)

        # Textos informativos superpuestos en la cámara
        cv2.putText(frame, f"Capturando {nombre} - Imagen {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(frame, "Presiona 'c' para capturar, 's' para salir", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow('Captura de objetos', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            roi = aux_frame[y_start:y_start + recuadro_h, x_start:x_start + recuadro_w]
            roi_resized = cv2.resize(roi, (224, 224))  

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f'{nombre}_{timestamp}_{count}.jpg'

            # 🔄 CORRECCIÓN AQUÍ: Cambiamos el string viejo por la variable 'nombre_archivo'
            cv2.imwrite(os.path.join(ruta_carpeta, nombre_archivo), roi_resized)
            
            print(f"Imagen guardada con éxito: {nombre_archivo}")
            count += 1

            if count >= num_imagenes:
                print("Se alcanzó la cantidad máxima de imágenes.")
                break

        elif key == ord('s'):
            print("Captura finalizada por usuario.")
            break

    cap.release()
    cv2.destroyAllWindows()


# ---- CLASE PARA CANVAS DE DECORACIÓN LATERAL (DISEÑO FLUIDO) ----

def dibujar_decoracion(canvas, width, height):
    """Dibuja formas orgánicas modernas imitando el diseño de referencia"""
    canvas.create_rectangle(0, 0, width, height, fill=COLOR_FONDO_IZQ, outline="")
    # Curvas/Ondas decorativas en la parte inferior trasera
    canvas.create_oval(-50, height - 150, width + 80, height + 100, fill="#3B82F6", outline="")
    canvas.create_oval(-20, height - 100, width + 50, height + 120, fill="#60A5FA", outline="")

# ---- VENTANAS DE DIÁLOGO REESTILIZADAS (DOS COLUMNAS) ----

class ElegantDialog(tk.Toplevel):
    def __init__(self, parent, titulo_ventana, titulo_interfaz, descripcion, placeholder="", is_numeric=False):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.title(titulo_ventana)
        self.resizable(False, False)
        self.configure(bg=COLOR_FONDO_DER)
        
        # Dimensiones estilo Login split
        window_width = 520
        window_height = 240
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (window_width // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.resultado = None
        self.is_numeric = is_numeric

        # COLUMNA IZQUIERDA: Panel decorativo visual
        self.canvas_left = tk.Canvas(self, width=180, height=window_height, bd=0, highlightthickness=0)
        self.canvas_left.pack(side="left", fill="y")
        dibujar_decoracion(self.canvas_left, 180, window_height)
        
        # Texto de marca en el panel izquierdo
        self.canvas_left.create_text(20, 40, text="SISTEMA V2.0", font=("Segoe UI", 10, "bold"), fill="#93C5FD", anchor="w")
        self.canvas_left.create_text(20, 75, text="Módulo de\nConfiguración", font=("Segoe UI", 12, "bold"), fill="#FFFFFF", anchor="w")

        # COLUMNA DERECHA: Formulario limpio
        right_frame = tk.Frame(self, bg=COLOR_FONDO_DER, padx=25, pady=20)
        right_frame.pack(side="right", fill="both", expand=True)

        # Título del input
        lbl_titulo = tk.Label(right_frame, text=titulo_interfaz, font=("Segoe UI", 14, "bold"), fg=COLOR_AZUL_OSCURO, bg=COLOR_FONDO_DER, anchor="w")
        lbl_titulo.pack(fill="x", pady=(0, 2))
        
        # Subtítulo explicativo
        lbl_desc = tk.Label(right_frame, text=descripcion, font=FONT_SUBTITULO, fg=COLOR_TEXTO_MUTED, bg=COLOR_FONDO_DER, anchor="w", justify="left")
        lbl_desc.pack(fill="x", pady=(0, 15))

        # Input Wrapper para simular un borde limpio estilizado
        entry_container = tk.Frame(right_frame, bg=COLOR_ENTRY_BORDER, bd=1)
        entry_container.pack(fill="x", ipady=1, pady=(0, 20))

        self.entry = tk.Entry(entry_container, font=("Segoe UI", 11), bg="#FFFFFF", fg=COLOR_TEXTO_MAIN, bd=0, highlightthickness=0)
        self.entry.pack(fill="x", padx=8, ipady=4)
        self.entry.insert(0, placeholder)
        self.entry.focus_set()
        self.entry.select_range(0, tk.END)

        # Botonera inferior derecha
        btn_container = tk.Frame(right_frame, bg=COLOR_FONDO_DER)
        btn_container.pack(fill="x", side="bottom")

        # Botón Aceptar principal (Estilo Azul Sólido)
        self.btn_ok = tk.Button(btn_container, text="ACEPTAR", font=FONT_BUTTON, bg=COLOR_FONDO_IZQ, fg="white",
                                bd=0, activebackground=COLOR_BOTON_HOVER, activeforeground="white", cursor="hand2", width=11, height=1)
        self.btn_ok.pack(side="right", padx=(8, 0))
        self.btn_ok.config(command=self.on_aceptar)

        # Botón Cancelar secundario (Texto gris/sin bordes invasivos)
        self.btn_cancel = tk.Button(btn_container, text="Cancelar", font=("Segoe UI", 10), bg=COLOR_FONDO_DER, fg=COLOR_TEXTO_MUTED,
                                    bd=0, activebackground="#F1F5F9", activeforeground=COLOR_TEXTO_MAIN, cursor="hand2", width=9)
        self.btn_cancel.pack(side="right")
        self.btn_cancel.config(command=self.on_cancelar)

        # Eventos del teclado para agilidad
        self.bind("<Return>", lambda e: self.on_aceptar())
        self.bind("<Escape>", lambda e: self.on_cancelar())

        # Efectos hover en el botón de acción
        self.btn_ok.bind("<Enter>", lambda e: self.btn_ok.config(bg=COLOR_BOTON_HOVER))
        self.btn_ok.bind("<Leave>", lambda e: self.btn_ok.config(bg=COLOR_FONDO_IZQ))

    def on_aceptar(self):
        valor = self.entry.get().strip()
        if self.is_numeric:
            if not valor:
                self.resultado = None
                self.destroy()
                return
            try:
                self.resultado = int(valor)
                if self.resultado < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Formato Inválido", "Ingrese una cantidad entera válida mayor a cero.")
                self.entry.focus_set()
                self.entry.select_range(0, tk.END)
                return
        else:
            self.resultado = valor
        self.destroy()

    def on_cancelar(self):
        self.resultado = None
        self.destroy()


# ---- VENTANA PRINCIPAL DEL SISTEMA (SPLIT VIEW) ----

def iniciar_gui():
    def iniciar_captura():
        # Diálogo para el nombre con la nueva interfaz de dos columnas
        dialogo_nombre = ElegantDialog(root, "Configurar Objeto", "Nombre del Objeto", "Identificador único para el dataset del envase:")
        root.wait_window(dialogo_nombre)
        nombre = dialogo_nombre.resultado

        if not nombre:
            messagebox.showerror("Error", "Debe ingresar un nombre válido para continuar.")
            return

        # Diálogo para la cantidad con la nueva interfaz de dos columnas
        dialogo_cantidad = ElegantDialog(root, "Configurar Cantidad", "Cantidad de Imágenes", "Total de fotogramas a almacenar en ráfaga:", placeholder="300", is_numeric=True)
        root.wait_window(dialogo_cantidad)
        num_imagenes = dialogo_cantidad.resultado

        if num_imagenes is None:
            num_imagenes = 300

        messagebox.showinfo("Proceso Iniciado", f"Iniciando la cámara para registrar {num_imagenes} muestras de '{nombre}'.")
        capturar_datos(nombre, num_imagenes)

    root = tk.Tk()
    root.title("Captura de Objetos v2.0")
    
    # Ventana principal más amplia para el estilo split
    main_width = 560
    main_height = 320
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    pos_x = (screen_w // 2) - (main_width // 2)
    pos_y = (screen_h // 2) - (main_height // 2)
    root.geometry(f"{main_width}x{main_height}+{pos_x}+{pos_y}")
    root.resizable(False, False)
    root.configure(bg=COLOR_FONDO_DER)

    # SECCIÓN IZQUIERDA: Panel Visual Corporativo Completo
    canvas_main_left = tk.Canvas(root, width=220, height=main_height, bd=0, highlightthickness=0)
    canvas_main_left.pack(side="left", fill="y")
    dibujar_decoracion(canvas_main_left, 220, main_height)

    # Textos de presentación del panel izquierdo
    canvas_main_left.create_text(25, 50, text="DATASET BUILDER", font=("Segoe UI", 9, "bold"), fill="#93C5FD", anchor="w")
    canvas_main_left.create_text(25, 90, text="Captura de\nObjetos", font=("Segoe UI", 18, "bold"), fill="#FFFFFF", anchor="w")
    canvas_main_left.create_text(25, 150, text="Herramienta para el\nreconocimiento óptico de\nenvases y botellas.", font=("Segoe UI", 9), fill="#E0F2FE", anchor="w")

    # SECCIÓN DERECHA: Panel de Control y Acciones
    right_control_frame = tk.Frame(root, bg=COLOR_FONDO_DER, padx=30, pady=40)
    right_control_frame.pack(side="right", fill="both", expand=True)

    lbl_main_title = tk.Frame(right_control_frame, bg=COLOR_FONDO_DER)
    lbl_main_title.pack(fill="x", pady=(0, 25))

    tk.Label(lbl_main_title, text="Bienvenido", font=FONT_TITULO, fg=COLOR_TEXTO_MAIN, bg=COLOR_FONDO_DER, anchor="w").pack(fill="x")
    tk.Label(lbl_main_title, text="Configure los parámetros iniciales de captura.", font=FONT_SUBTITULO, fg=COLOR_TEXTO_MUTED, bg=COLOR_FONDO_DER, anchor="w").pack(fill="x")

    # Botón Iniciar Captura Estilizado (Azul Vibrante)
    boton_iniciar = tk.Button(right_control_frame, text="INICIAR CAPTURA", font=FONT_BUTTON, bg=COLOR_FONDO_IZQ, fg="white",
                              bd=0, activebackground=COLOR_BOTON_HOVER, activeforeground="white", cursor="hand2", width=22, height=2)
    boton_iniciar.pack(pady=8, fill="x")

    # Botón Salir Estilizado (Gris Claro)
    boton_salir = tk.Button(right_control_frame, text="Salir del Sistema", font=("Segoe UI", 10), bg="#F1F5F9", fg=COLOR_TEXTO_MUTED,
                            bd=0, activebackground="#E2E8F0", activeforeground=COLOR_TEXTO_MAIN, cursor="hand2", width=22, height=1)
    boton_salir.pack(pady=4, fill="x")

    # Vinculación de efectos dinámicos en los botones (Hover)
    boton_iniciar.bind("<Enter>", lambda e: boton_iniciar.config(bg=COLOR_BOTON_HOVER))
    boton_iniciar.bind("<Leave>", lambda e: boton_iniciar.config(bg=COLOR_FONDO_IZQ))
    boton_salir.bind("<Enter>", lambda e: boton_salir.config(bg="#E2E8F0", fg=COLOR_TEXTO_MAIN))
    boton_salir.bind("<Leave>", lambda e: boton_salir.config(bg="#F1F5F9", fg=COLOR_TEXTO_MUTED))

    # Asignación de funciones
    boton_iniciar.config(command=iniciar_captura)
    boton_salir.config(command=root.destroy)

    root.mainloop()

if __name__ == "__main__":
    iniciar_gui()