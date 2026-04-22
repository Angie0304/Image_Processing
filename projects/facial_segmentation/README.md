# FaceTrack: Facial Segmentation
This module implements a facial segmentation system using digital image processing techniques. It includes a backend application for processing and segmenting facial images, based on prior experimentation with fundamental image processing operations such as noise handling, filtering, and edge detection.

## Module Structure

```text
facial_segmentation/
├── docs/
│   └── reporte.pdf                # Project report
├── data/                          # Input images
│   ├── Imagen1_obscura.bmp       
│   ├── Imagen2_brillante.bmp       
│   ├── Imagen3_alto_contraste.bmp  
│   └── Imagen4_bajo_contraste.bmp  
├── src/
│   ├── aplicacion.py              # Backend for facial segmentation
│   └── experimentacion_1.py       # Experimental PDI application
├── requirements.txt               # Dependencies
└── README.md                      # Documentation and usage guide

```
## How it works

### Facial Segmentation Backend
The system works as follows:
- Upload an input image
-  Analyze brightness and contrast
-  Adjust image properties automatically  
-  Convert the image to grayscale  
-  Apply noise reduction
-  Detect edges using filters (Roberts and Sobel)   
-  Combine edge information  
-  Apply thresholding for segmentation  
-  Generate a partially segmented facial image


## Usage

### 1. Install dependencies

```bash id="y8i2v3"
pip install -r requirements.txt
```

### 2. Run the backend

```bash id="c1l8mx"
python src/aplicacion.py
```

### 3. Open in browser

Go to:

```
http://localhost:3000
```

### 4. Upload an image

- Upload an image from your device  
- Wait for the processing to complete  
- View the segmentation result  



## Status

The backend for facial segmentation is fully implemented.  
The frontend interface is currently under development.

## Notes

The application runs as a backend service and does not include a graphical interface at this stage.

