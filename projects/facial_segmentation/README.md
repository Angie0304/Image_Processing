# Facial Segmentation (FaceTrack)
This module implements a facial segmentation system using digital image processing techniques. It includes a backend application for processing and segmenting facial images, as well as an experimental application used to explore fundamental image processing operations.

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
└── README.md                      #Documentation and execution guide

```
## How it works

### Facial Segmentation Backend
The system follows these steps:

1. Upload an input image  
2. Analyze brightness and contrast  
3. Adjust image properties automatically  
4. Convert the image to grayscale  
5. Apply noise reduction  
6. Detect edges using filters (Roberts and Sobel)  
7. Combine edge information  
8. Apply thresholding for segmentation  
9. enerate a partially segmented facial image  

