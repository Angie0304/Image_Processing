# Binary Morphology for Boundary Extraction

This module implements binary morphological operations for boundary extraction and noise removal in images. It applies erosion, dilation, opening, and closing to analyze and enhance object structures.

## Module structure
```text
binary_morphology_boundary_extraction/
├── README.md                   # Documentation and execution guide
├── morfologia_binaria.ipynb    # Morphological operations and boundary extraction
├── reporte.pdf                 # Report 
└── requirements.txt            # Dependencies  
```

## How it works
The module follows these steps:
1. Load binary images
2. Apply erosion to shrink objects
3. Apply dilation to expand objects
4. Use opening to remove noise
5. Use closing to fill gaps
6. Extract boundaries using:
   - Morphological gradient (dilation − erosion)
   - Internal boundary (image − erosion)

## Boundary Extraction Methods


**Morphological Gradient**

$$
G = (A ⊕ S) - (A ⊖ S)
$$


**Internal Boundary**

$$
B = A - (A ⊖ S)
$$
