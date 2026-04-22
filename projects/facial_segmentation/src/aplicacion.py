
"""
Nombre de la aplicacion: FaceTrack
Unidad de aprendizaje: Procesamiento Digital de Imagenes 
Grupo 4BM1-Comunidad 3

Descripcion: 
    Aplicacion para procesar y analizar imagenes subidas por el usuario 
    utilizando tecnicas de ajuste de brillo, eliminacion de ruido y deteccion 
    de bordes para lograr segmentar parcial y totalmente un rostro. 

Tecnologias: 
    #-Flask 
    #-OpenCV
    #-NumPy
    #-PIL
"""


from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import numpy as np
import cv2
import os
from flask import render_template


# ============================================
# Configuracion de Flask y carpetas de trabajo
# ============================================


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
MASK_FOLDER = 'mask'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(MASK_FOLDER, exist_ok=True)

image_paths = {
    'Imagen1_obscura.bmp': 'Imagen1_obscura_mask.jpeg',
    'Imagen2_brillante.bmp': 'Imagen2_brillante_mask.jpeg',
    'Imagen3_alto contraste.bmp': 'Imagen3_alto contraste_mask.jpeg',
    'Imagen4_bajo contraste.bmp': 'Imagen4_bajo contraste_mask.jpeg'
}



# ============================================
# Carga y preprocesamiento de imagenes
# ============================================

def load_and_preprocess_image(filepath):
    """
    -Carga una imagen, analiza su brillo y contraste, y realiza ajustes necesarios.
    -Args:
        filepath (str): Ruta de la imagen a cargar.
    -Returns:
        tuple: Imagen procesada (grayscale), rutas de la imagen original,
               ajustada y en escala de grises.
    """
    
    image = cv2.imread(filepath)
    if image is None:
        raise ValueError('No se pudo cargar la imagen')

    original_path = os.path.join(PROCESSED_FOLDER, "original_" + os.path.basename(filepath))
    cv2.imwrite(original_path, image)

    brightness_level, contrast_level = analyze_image_properties(image)
    res_image = adjust_image(image, brightness_level, contrast_level)
    adjusted_path = os.path.join(PROCESSED_FOLDER, "adjusted_" + os.path.basename(filepath))
    cv2.imwrite(adjusted_path, res_image)

    res_image = cv2.cvtColor(res_image, cv2.COLOR_BGR2GRAY)
    grayscale_path = os.path.join(PROCESSED_FOLDER, "grayscale_" + os.path.basename(filepath))
    cv2.imwrite(grayscale_path, res_image)

    return res_image, original_path, adjusted_path, grayscale_path


# ============================================
# Ajuste de brillo y contraste
# ============================================

def analyze_image_properties(image):
    """
    -Analiza las propiedades de brillo y contraste de una imagen.
    -Args:
        image (np.ndarray): Imagen a analizar.
    -Returns:
        tuple: Niveles de brillo y contraste clasificados.
    """
    brightness = np.mean(image)
    contrast = np.std(image)

    if brightness > 200:
        brightness_level = "brillante"
    elif brightness < 50:
        brightness_level = "oscura"
    else:
        brightness_level = "normal"

    if contrast > 70:
        contrast_level = "alto_contraste"
    elif contrast < 30:
        contrast_level = "bajo_contraste"
    else:
        contrast_level = "contraste_normal"

    return brightness_level, contrast_level


def adjust_image(image, brightness_level, contrast_level):
    """
    -Ajusta la imagen según los niveles de brillo y contraste detectados.
    -Args:
        -image (np.ndarray): Imagen a ajustar.
        -brightness_level (str): Nivel de brillo detectado.
        -contrast_level (str): Nivel de contraste detectado.
    -Returns:
        np.ndarray: Imagen ajustada.
    """

    if brightness_level == "brillante" and contrast_level == "alto_contraste":
        result_image = cv2.convertScaleAbs(image, alpha=0.8, beta=-30)
        result_image = cv2.GaussianBlur(result_image, (5, 5), 0)
    elif brightness_level == "brillante" and contrast_level == "bajo_contraste":
        gamma = calculate_gamma(image)
        result_image = adjust_gamma(image, gamma)
    elif brightness_level == "oscura" and contrast_level == "alto_contraste":
        result_image = cv2.convertScaleAbs(image, alpha=0.9, beta=50)
    elif brightness_level == "oscura" and contrast_level == "bajo_contraste":
        result_image = adjust_gamma(image, 0.3)
    elif brightness_level == "normal" and contrast_level == "alto_contraste":
        result_image = soft_image(image)
    elif brightness_level == "normal" and contrast_level == "bajo_contraste":
        result_image = cv2.equalizeHist(image)
    else:
        result_image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    return result_image


def calculate_gamma(image):
    """
    -Calcula el valor gamma basado en el brillo promedio de la imagen.
    -Args:
        image (np.ndarray): Imagen a analizar.
    -Returns:
        float: Valor de gamma calculado.
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness_mean = np.mean(gray)
    ideal_brightness = 128
    gamma = 1.0 + (brightness_mean - ideal_brightness) / 32 if brightness_mean > ideal_brightness else 1.0 - (ideal_brightness - brightness_mean) / 32
    return max(0.1, min(gamma, 5.0))


def adjust_gamma(image, gamma):
    """
    -Aplica correccion gamma a la imagen.
    -Args:
        -image (np.ndarray): Imagen a ajustar.
        -gamma (float): Valor gamma para la corrección.
    -Returns:
        np.ndarray: Imagen con gamma ajustado.
    """

    lookUpTable = np.empty((1, 256), np.uint8)
    for i in range(256):
        lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    return cv2.LUT(image, lookUpTable)


def soft_image(image):
    """
    -Suaviza la imagen utilizando el modelo de color LAB y mejora el contraste.
    -Args:
        image (np.ndarray): Imagen a suavizar.
    -Returns:
        np.ndarray: Imagen suavizada y mejorada.
    """

    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_image)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_clahe = clahe.apply(l)
    lab_clahe = cv2.merge((l_clahe, a, b))
    result_image = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2BGR)
    gamma = calculate_gamma(result_image)
    return adjust_gamma(result_image, gamma)


# ============================================
# Funciones para ruido y filtrado
# ============================================

def denoise_image(image):
    """
    -Aplica un filtro Gaussiano para reducir el ruido en la imagen.
    -Args:
        image (np.ndarray): Imagen con ruido.
    -Returns:
        np.ndarray: Imagen con ruido reducido.
    """

    return cv2.GaussianBlur(image, (5, 5), 0)


def enhance_contrast(image):
    """
    -Mejora el contraste de una imagen utilizando ecualizacion de histograma.
    -Args:
        image (np.ndarray): Imagen a mejorar.
    -Returns:
        np.ndarray: Imagen con contraste mejorado.
    """
    return cv2.equalizeHist(image)


# ============================================
# Funciones de segmentacion y deteccion de bordes
# ============================================

def filtro_roberts(image):
    """
    -Aplica el filtro de deteccion de bordes de Roberts.
    -Args:
        image (np.ndarray): Imagen de entrada.
    -Returns:
        np.ndarray: Imagen con bordes detectados.
    """

    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel_gx = np.array([[1, 0], [0, -1]], dtype=np.float32)
    kernel_gy = np.array([[0, 1], [-1, 0]], dtype=np.float32)
    gx = cv2.filter2D(image, cv2.CV_64F, kernel_gx)
    gy = cv2.filter2D(image, cv2.CV_64F, kernel_gy)
    magnitud = np.sqrt(gx**2 + gy**2)
    magnitud = (magnitud / np.max(magnitud)) * 255 if np.max(magnitud) != 0 else magnitud
    return cv2.convertScaleAbs(magnitud)


def filtro_sobel(image):
    """
    -Aplica el filtro de deteccion de bordes de Sobel.
    -Args:
        image (np.ndarray): Imagen de entrada.
    -Returns:
        np.ndarray: Imagen con bordes detectados.
    """

    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    gradiente_magnitud = cv2.magnitude(sobel_x, sobel_y)
    return cv2.normalize(gradiente_magnitud, None, 0, 255, cv2.NORM_MINMAX)


def combinar_filtros(image1, weight_roberts, image2, weight_sobel, offset=0):
    """
    -Combina los resultados de los filtros de Roberts y Sobel.
    -Args:
        -image1 (np.ndarray): Resultado del filtro Roberts.
        -weight_roberts (float): Peso asignado al filtro Roberts.
        -image2 (np.ndarray): Resultado del filtro Sobel.
        -weight_sobel (float): Peso asignado al filtro Sobel.
        -offset (int): Valor de desplazamiento para ajustar el brillo.
    -Returns:
        np.ndarray: Imagen combinada con bordes detectados.
    """

    image1 = image1.astype(np.float32)
    image2 = image2.astype(np.float32)
    combinada = (weight_roberts * image1 + weight_sobel * image2 + offset)
    return np.clip(combinada, 0, 255).astype(np.uint8)


def partial_segmentation(image, filepath):
    """
    -Realiza una segmentacion parcial utilizando los filtros de Roberts y Sobel.
    -Args:
        -image (np.ndarray): Imagen a segmentar.
        -filepath (str): Ruta del archivo de imagen.
    -Returns:
        tuple: Imagen combinada y ruta de la imagen segmentada.
    """

    edges_roberts = filtro_roberts(image)
    edges_sobel = filtro_sobel(image)
    combined_edges = combinar_filtros(edges_roberts, 0.5, edges_sobel, 0.5)
    combined_edges = cv2.normalize(combined_edges, None, 0, 255, cv2.NORM_MINMAX)
    _, thresholded_image = cv2.threshold(combined_edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresholded_path = os.path.join(PROCESSED_FOLDER, "thresholded_" + os.path.basename(filepath))
    cv2.imwrite(thresholded_path, thresholded_image)
    return combined_edges, thresholded_path


# ============================================
# Interfaz Flask
# ============================================

@app.route('/processed/<path:filename>')
def serve_processed_file(filename):
    """
    -Sirve una imagen procesada desde la carpeta de archivos procesados.
    -Args:
        filename (str): Nombre del archivo.
    -Returns:
        Response: Archivo procesado como respuesta HTTP.
    """

    response = send_from_directory(PROCESSED_FOLDER, filename)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    -Maneja la subida de archivos y procesa la imagen subida.
    -Returns:
        Response: JSON con las rutas de las imagenes procesadas o mensaje de error.
    """

    if 'image' not in request.files:
        return jsonify({'error': 'No se encontró ninguna imagen'}), 400

    file = request.files['image']
    filename = os.path.basename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        preprocessed_image, original_path, adjusted_path, grayscale_path = load_and_preprocess_image(filepath)
        secondary_path, segmentation_path = partial_segmentation(preprocessed_image, filepath)

        return jsonify({
            "message": "Imagen procesada exitosamente",
            "original_image": original_path,
            "adjusted_image": adjusted_path,
            "grayscale_image": grayscale_path,
            "segmented_image": segmentation_path
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =========================================
# RUTAS FLASK
# =========================================


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    ...

if __name__ == "__main__":
    app.run(port=3000, debug=True)
