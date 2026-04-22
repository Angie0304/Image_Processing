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
   - Morphological gradient 
   - Internal boundary


## Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the notebook

```bash
jupyter notebook morfologia_binaria.ipynb
```

### 3. Output

The notebook will:

* Display original images
* Show results of erosion and dilation
* Apply opening and closing for noise removal
* Visualize extracted boundaries

## Status 
Completed
