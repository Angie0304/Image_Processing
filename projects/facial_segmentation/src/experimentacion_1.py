"""
Nombre: Aplicación para experimentar las técnicas de PDI 
Unidad de aprendizaje: Procesamiento Digital de Imagenes 
Grupo 4BM1-Comunidad 3

Descripcion: 
    Aplicación diseñada para experimentar con diversas técnicas 
    de Procesamiento Digital de Imágenes (PDI), facilitando el 
    análisis y la manipulación de imágenes mediante ajustes de 
    brillo, eliminación de ruido y detección de bordes,
    
Tecnologias: 
    -OpenCV 
    -NumPy 
    -Tkinter 
    -Pillow 
    -Matplotlib 
    -SciPy
"""

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from scipy.stats import mode

# =============================
# Cargar imagenes
# =============================

def mostrar_imagen1(img):
    """
    -Muestra la primera imagen en la interfaz grafica.
    -Args:
        img (numpy.ndarray): Imagen en formato NumPy que se desea mostrar.
    -Returns:
        None
    """

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image=img_pil)
    btn_imagen1.config(image=img_tk)
    btn_imagen1.image = img_tk


def mostrar_imagen2(img):
    """
    -Muestra la segunda imagen en la interfaz grafica.
    -Args:
        img (numpy.ndarray): Imagen en formato NumPy que se desea mostrar.
    -Returns:
        None
    """

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image=img_pil)
    btn_imagen2.config(image=img_tk)
    btn_imagen2.image = img_tk


def mostrar_imagen(img):
    """
    -Muestra la imagen resultante en la interfaz grafica.
    -Args:
        img (numpy.ndarray): Imagen en formato NumPy que se desea mostrar.
    -Returns:
        None
    """

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(image=img_pil)
    btn_imagen_resultado.config(image=img_tk)
    btn_imagen_resultado.image = img_tk


def cargar_imagen1():
    """
    -Carga la primera imagen desde el sistema de archivos y la muestra en la interfaz.
    -Args:
        None
    -Returns:
        None
    """

    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg;*.bmp")])
    if filepath:
        global img1
        img1 = cv2.imread(filepath)
        img1 = cv2.resize(img1, (150, 150))
        mostrar_imagen1(img1)


def cargar_imagen2():
    """
    -Carga la segunda imagen desde el sistema de archivos y la muestra en la interfaz.
    -Args:
        None
    -Returns:
        None
    """

    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg;*.bmp")])
    if filepath:
        global img2
        img2 = cv2.imread(filepath)
        img2 = cv2.resize(img2, (150, 150))
        mostrar_imagen2(img2)


# =============================
# Conversión de imágenes
# =============================

def convertir_escala_grises():
    """
    -Convierte la imagen cargada a escala de grises y la muestra en la interfaz.
    -Args:
        None
    -Returns:
        None
    """

    global img_resultado
    if img1 is None:
        return messagebox.showerror("Error", "Debe seleccionar una imagen")

    if img_resultado is None:
        img_resultado = img1.copy()

    gris = cv2.cvtColor(img_resultado, cv2.COLOR_BGR2GRAY)
    mostrar_imagen(cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR))


# ==================================
# Operaciones aritmeticas y logicas
# ==================================

def operacion_aritmetica(operacion):
    """
    -Realiza una operacion aritmetica entre dos imagenes cargadas.
    -Args:
        operacion (str): Operacion a realizar ('Suma', 'Resta', 'Multiplicacion').
    -Returns:
        None
    """

    global img_resultado
    if img1 is None or img2 is None:
        return messagebox.showerror("Error", "Debe seleccionar dos imágenes antes de realizar alguna operación")

    if img1.shape != img2.shape:
        return messagebox.showerror("Error", "Las imágenes deben tener las mismas dimensiones")

    if operacion == 'Suma':
        img_resultado = cv2.add(img1, img2)
    elif operacion == 'Resta':
        img_resultado = cv2.subtract(img1, img2)
    elif operacion == 'Multiplicación':
        img_resultado = cv2.multiply(img1, img2)
    else:
        return messagebox.showerror("Error", "Operación no válida")

    mostrar_imagen(img_resultado)


def operacion_aritmetica_escalar(operacion):
    """
    -Realiza una operacion aritmetica entre una imagen y un escalar.
    -Args:
        operacion (str): Operacion a realizar ('Desplazamiento', 'Contraccion', 'Expansion').
    -Returns:
        None
    """

    global img_resultado
    if img1 is None:
        return messagebox.showerror("Error", "Debe seleccionar una imagen antes de realizar la operación")

    if img_resultado is None:
        img_resultado = img1.copy()

    valor_escalar = valida_escalar()
    if valor_escalar is None:
        return

    if operacion == 'Desplazamiento':
        img_resultado = cv2.add(img_resultado, valor_escalar)
    elif operacion == 'Contracción':
        img_resultado = cv2.multiply(img_resultado, valor_escalar)
    elif operacion == 'Expansión':
        img_resultado = cv2.subtract(img_resultado, valor_escalar)
    else:
        return messagebox.showerror("Error", "Operación no válida")

    mostrar_imagen(img_resultado)

def operacion_logica(operacion):
    """
    -Realiza una operación logica entre dos imagenes cargadas.
    -Args:
        operacion (str): Operacion logica a realizar ('AND', 'OR', 'XOR').
    -Returns:
        None
    """

    global img_resultado
    if img1 is None or img2 is None:
        return messagebox.showerror("Error", "Debe seleccionar dos imágenes antes de realizar alguna operación")

    if operacion == 'AND':
        img_resultado = cv2.bitwise_and(img1, img2)
    elif operacion == 'OR':
        img_resultado = cv2.bitwise_or(img1, img2)
    elif operacion == 'XOR':
        img_resultado = cv2.bitwise_xor(img1, img2)
    else:
        return messagebox.showerror("Error", "Operación no válida")

    mostrar_imagen(img_resultado)

# =============================
# Ruido y eliminacion de ruido
# =============================

def generar_ruido_gaussiano():
    """
    -Añade ruido gaussiano a la imagen cargada.
    -Args:
        None
    -Returns:
        None
    """
    global img_resultado
    if img1 is None:
        return messagebox.showerror("Error", "Debe seleccionar una imagen")

    if img_resultado is None:
        img_resultado = img1.copy()

    mean = 0
    std_dev = 25
    ruido = np.random.normal(mean, std_dev, img_resultado.shape).astype(np.float32)
    img_resultado = np.clip(img_resultado + ruido, 0, 255).astype(np.uint8)
    mostrar_imagen(img_resultado)


def generar_ruido_sal_pimienta():
    """
    -Añade ruido de tipo sal y pimienta a la imagen cargada.
    -Args:
        None
    -Returns:
        None
    """

    global img_resultado
    if img1 is None:
        return messagebox.showerror("Error", "Debe seleccionar una imagen")

    if img_resultado is None:
        img_resultado = img1.copy()

    prob_ruido = 0.05
    cantidad_salpimienta = int(prob_ruido * img_resultado.size)
    coords_sal = [np.random.randint(0, i - 1, cantidad_salpimienta // 2) for i in img_resultado.shape]
    coords_pimienta = [np.random.randint(0, i - 1, cantidad_salpimienta // 2) for i in img_resultado.shape]

    img_resultado[coords_sal[0], coords_sal[1], :] = 255
    img_resultado[coords_pimienta[0], coords_pimienta[1], :] = 0
    mostrar_imagen(img_resultado)


# =============================
# Deteccion de bordes
# =============================

def deteccion_bordes():
    """
    -Aplica el detector de bordes de Canny a la imagen cargada.
    -Args:
        None
    -Returns:
        None
    """

    global img_resultado
    if img1 is None:
        return messagebox.showerror("Error", "Debe seleccionar una imagen")

    if img_resultado is None:
        img_resultado = img1.copy()

    gris = cv2.cvtColor(img_resultado, cv2.COLOR_BGR2GRAY)
    img_resultado = cv2.Canny(gris, 100, 200)
    mostrar_imagen(cv2.cvtColor(img_resultado, cv2.COLOR_GRAY2BGR))


def filtro_roberts():
    """
    -Aplica el filtro de deteccion de bordes de Roberts a la imagen cargada.
    -Args:
        None
    -Returns:
        None
    """

    global img_resultado
    if img1 is None:
        return messagebox.showerror("Error", "Debe seleccionar una imagen")

    if img_resultado is None:
        img_resultado = img1.copy()

    imagen_gris = cv2.cvtColor(img_resultado, cv2.COLOR_BGR2GRAY)

    kernel_gx = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernel_gy = np.array([[0, 1], [-1, 0]], dtype=np.float32)

    gx = cv2.filter2D(imagen_gris, cv2.CV_64F, kernel_gx)
    gy = cv2.filter2D(imagen_gris, cv2.CV_64F, kernel_gy)

    magnitud = np.sqrt(gx**2 + gy**2)
    img_resultado = cv2.convertScaleAbs(magnitud)
    mostrar_imagen(cv2.cvtColor(img_resultado, cv2.COLOR_GRAY2BGR))


# =============================
# Interfaz grafica
# =============================

# Crear la ventana principal
root = tk.Tk()
root.title("Procesamiento de Imágenes Avanzado")
root.geometry("1200x800")

# Crear marco para cargar imagenes y botones
frame_cargar = tk.Frame(root, padx=10, pady=10)
frame_cargar.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

# Crear marco para mostrar imagenes
frame_imagenes = tk.Frame(root, padx=10, pady=10, relief=tk.SUNKEN, bd=2)
frame_imagenes.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")

# Crear marco para operaciones
frame_operaciones = tk.Frame(root, padx=10, pady=10)
frame_operaciones.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")

# Botones para cargar imagenes
tk.Button(frame_cargar, text="Cargar imagen 1", command=cargar_imagen1, width=15).grid(row=0, column=0, padx=10)
tk.Button(frame_cargar, text="Cargar imagen 2", command=cargar_imagen2, width=15).grid(row=0, column=1, padx=10)

# Etiquetas para mostrar las imagenes
lbl_imagen1 = tk.Label(frame_imagenes, relief=tk.RIDGE)
lbl_imagen1.grid(row=0, column=0, padx=10, pady=10)

lbl_imagen2 = tk.Label(frame_imagenes, relief=tk.RIDGE)
lbl_imagen2.grid(row=0, column=1, padx=10, pady=10)

lbl_imagen_resultado = tk.Label(frame_imagenes, relief=tk.RIDGE)
lbl_imagen_resultado.grid(row=0, column=2, padx=10, pady=10)

# Crear un marco principal para las secciones
frame_principal = tk.Frame(root, padx=10, pady=10)
frame_principal.grid(row=3, column=0, columnspan=3, sticky="nsew")

# Configurar columnas del marco principal
frame_principal.grid_columnconfigure(0, weight=1)
frame_principal.grid_columnconfigure(1, weight=1)
frame_principal.grid_columnconfigure(2, weight=1)
frame_principal.grid_columnconfigure(3, weight=1)
frame_principal.grid_columnconfigure(4, weight=1)

# Crear botones para las operaciones
# Operaciones Aritmeticas
frame_oper_arit = tk.Frame(frame_principal, padx=10, pady=10, relief=tk.GROOVE, bd=2)
frame_oper_arit.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
tk.Label(frame_oper_arit, text="Operaciones Aritméticas", font=("Arial", 10, "bold")).pack(pady=5)

operaciones_aritmeticas = ttk.Combobox(frame_oper_arit, values=["Suma", "Resta", "Multiplicación"], width=20)
operaciones_aritmeticas.pack(pady=5)
btn_aplicar_aritmetica = tk.Button(frame_oper_arit, text="Aplicar", command=lambda: operacion_aritmetica(operaciones_aritmeticas.get()))
btn_aplicar_aritmetica.pack(pady=5)

# Operaciones Escalares
frame_oper_escalar = tk.Frame(frame_principal, padx=10, pady=10, relief=tk.GROOVE, bd=2)
frame_oper_escalar.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
tk.Label(frame_oper_escalar, text="Operaciones Escalares", font=("Arial", 10, "bold")).pack(pady=5)

entry_escalar = tk.Entry(frame_oper_escalar, width=15)
entry_escalar.pack(pady=5)
tk.Button(frame_oper_escalar, text="Desplazamiento", command=lambda: operacion_aritmetica_escalar('Desplazamiento'), width=20).pack(pady=5)
tk.Button(frame_oper_escalar, text="Contracción", command=lambda: operacion_aritmetica_escalar('Contracción'), width=20).pack(pady=5)
tk.Button(frame_oper_escalar, text="Expansión", command=lambda: operacion_aritmetica_escalar('Expansión'), width=20).pack(pady=5)

# Operaciones Logicas
frame_oper_logica = tk.Frame(frame_principal, padx=10, pady=10, relief=tk.GROOVE, bd=2)
frame_oper_logica.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
tk.Label(frame_oper_logica, text="Operaciones Lógicas", font=("Arial", 10, "bold")).pack(pady=5)

operaciones_logicas = ttk.Combobox(frame_oper_logica, values=["AND", "OR", "XOR"], width=20)
operaciones_logicas.pack(pady=5)
btn_operacion_logica = tk.Button(frame_oper_logica, text="Aplicar", command=lambda: operacion_logica(operaciones_logicas.get()))
btn_operacion_logica.pack(pady=5)

# Filtros de Ruido
frame_filtros = tk.Frame(frame_principal, padx=10, pady=10, relief=tk.GROOVE, bd=2)
frame_filtros.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
tk.Label(frame_filtros, text="Ruido y Filtros", font=("Arial", 10, "bold")).pack(pady=5)

btn_ruido_gaussiano = tk.Button(frame_filtros, text="Ruido Gaussiano", command=generar_ruido_gaussiano, width=20)
btn_ruido_gaussiano.pack(pady=5)

btn_ruido_sal_pimienta = tk.Button(frame_filtros, text="Ruido Sal y Pimienta", command=generar_ruido_sal_pimienta, width=20)
btn_ruido_sal_pimienta.pack(pady=5)

# Deteccion de Bordes
frame_bordes = tk.Frame(frame_principal, padx=10, pady=10, relief=tk.GROOVE, bd=2)
frame_bordes.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")
tk.Label(frame_bordes, text="Detección de Bordes", font=("Arial", 10, "bold")).pack(pady=5)

btn_canny = tk.Button(frame_bordes, text="Bordes Canny", command=deteccion_bordes, width=20)
btn_canny.pack(pady=5)

btn_roberts = tk.Button(frame_bordes, text="Filtro Roberts", command=filtro_roberts, width=20)
btn_roberts.pack(pady=5)

# Boton para salir
btn_salir = tk.Button(root, text="Salir", command=root.quit, width=20, bg="red", fg="white")
btn_salir.grid(row=4, column=0, columnspan=3, pady=20)

# Iniciar el loop de la interfaz
tk.mainloop()

