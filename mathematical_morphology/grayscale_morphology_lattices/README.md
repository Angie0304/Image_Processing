# Grayscale Morphology on Lattices

This module implements grayscale morphological operations based on lattice theory for image analysis. It applies dilation, erosion, opening, and closing, along with gradient-based methods and top-hat transformations to enhance and extract image features.



## Module structure
```text
grayscale_morphology_lattices/
├── README.md                       # Documentation and execution guide
├── morfologia_escala_grises.ipynb  # Grayscale morphology operations
├── reporte.pdf                     # Report 
└── requirements.txt                # Dependencies  
```

## How it works

The module follows these steps:

1. Load a grayscale image
2. Define a structuring element (kernel)
3. Apply dilation and erosion
4. Use opening to smooth the image
5. Use closing to fill small holes
6. Compute the boundary (dilation − erosion)
7. Apply morphological gradients
8. Compute gradient by dilation and by erosion
9. Apply top-hat and black-hat transformations


## Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the notebook

```bash
jupyter notebook morfologia_escala_grises.ipynb
```

### 3. Output

The notebook will:

* Display the original image
* Show results of morphological operations
* Visualize gradients and transformations


## Status 
Completed
