# PDI Project - Segmentación Semántica de Escenas Urbanas

Este repositorio contiene un proyecto de Procesamiento Digital de Imágenes enfocado en la **segmentación semántica de escenas urbanas** usando el dataset **CamVid** y una arquitectura tipo **U-Net**.

El objetivo principal es clasificar cada píxel de una imagen urbana en una categoría específica, como carretera, edificio, cielo, árbol, vehículo, peatón, señales de tránsito, entre otras clases.

## Descripción del proyecto

La segmentación semántica permite identificar regiones dentro de una imagen asignando una clase a cada píxel.  
En este proyecto se entrena un modelo de deep learning para reconocer elementos presentes en escenas urbanas, lo cual puede aplicarse en áreas como visión por computador, análisis de movilidad, conducción asistida y sistemas inteligentes de transporte.

El modelo fue entrenado con imágenes del dataset **CamVid**, utilizando una arquitectura **U-Net** para generar máscaras de segmentación.

## Estructura del repositorio

```text
pdi-project/
│
├── training/
│   ├── proyecto-imagenes.ipynb
│   ├── best-model/
│   │   └── best_camvid_unet.pth
│   └── parameters/
│       └── experiment_summary.json
│
├── deployment/
│   ├── app.py
│   ├── requirements.txt
│   └── Despliegue_Modelo_Proyecto_PDI.ipynb
│
└── README.md#
