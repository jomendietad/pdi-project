# PDI Project - Segmentación Semántica de Escenas Urbanas con CamVid

Este repositorio contiene el desarrollo de un proyecto de Procesamiento Digital de Imágenes orientado a la **segmentación semántica de escenas urbanas** mediante técnicas de aprendizaje profundo.

El objetivo principal del proyecto es entrenar un modelo capaz de analizar una imagen urbana y clasificar cada píxel dentro de una categoría específica, como carretera, edificio, cielo, vehículo, peatón, árbol, señales de tránsito, entre otras clases.

Para esto se utiliza una arquitectura tipo **U-Net**, la cual es ampliamente empleada en tareas de segmentación de imágenes porque permite generar una máscara de salida con la misma estructura espacial de la imagen de entrada.

---

## Base de datos utilizada

La base de datos utilizada de forma obligatoria en este proyecto fue:

## CamVid - Cambridge-driving Labeled Video Database

CamVid es una base de datos de escenas urbanas utilizada comúnmente para tareas de segmentación semántica. Está compuesta por imágenes capturadas desde una cámara en movimiento en entornos urbanos, junto con sus respectivas máscaras de segmentación etiquetadas píxel a píxel.

En este proyecto, CamVid se utiliza para entrenar, validar y probar el modelo de segmentación semántica.

### Ruta usada en el entorno de trabajo

En el experimento del proyecto, la base de datos fue cargada desde la siguiente ruta en Kaggle:

```text
/kaggle/input/datasets/carlolepelaars/camvid/CamVid
```

### Tipo de datos

La base de datos contiene:

* Imágenes RGB de escenas urbanas.
* Máscaras de segmentación asociadas a cada imagen.
* Etiquetas por píxel, donde cada color o índice representa una clase semántica.
* División de datos para entrenamiento, validación y prueba.

### Número de clases

El proyecto trabaja con un total de:

```text
32 clases
```

### Clases utilizadas

Las clases consideradas en el proyecto son:

```text
Animal
Archway
Bicyclist
Bridge
Building
Car
CartLuggagePram
Child
Column_Pole
Fence
LaneMkgsDriv
LaneMkgsNonDriv
Misc_Text
MotorcycleScooter
OtherMoving
ParkingBlock
Pedestrian
Road
RoadShoulder
Sidewalk
SignSymbol
Sky
SUVPickupTruck
TrafficCone
TrafficLight
Train
Tree
Truck_Bus
Tunnel
VegetationMisc
Void
Wall
```

### Justificación del uso de CamVid

Se seleccionó CamVid porque es una base de datos adecuada para problemas de segmentación semántica urbana. Sus imágenes contienen elementos reales de ciudad, como vías, autos, edificios, árboles, peatones, señales y otros objetos presentes en escenarios de movilidad.

Esta base de datos permite evaluar la capacidad del modelo para reconocer diferentes regiones de una imagen y asignar correctamente una clase a cada píxel. Por esta razón, resulta pertinente para un proyecto académico de Procesamiento Digital de Imágenes enfocado en visión por computador.

---

## Descripción del problema

El problema abordado corresponde a una tarea de **segmentación semántica multiclase**.

A diferencia de una clasificación tradicional de imágenes, donde el modelo asigna una sola etiqueta a toda la imagen, en la segmentación semántica el modelo realiza una clasificación por cada píxel.

Por ejemplo, en una imagen urbana, el modelo debe identificar qué píxeles pertenecen a la carretera, cuáles pertenecen al cielo, cuáles a vehículos, peatones, edificios, árboles u otros elementos.

La salida del modelo es una máscara de segmentación, donde cada región de la imagen queda representada por una clase.

---

## Objetivo general

Desarrollar un modelo de aprendizaje profundo para segmentar escenas urbanas del dataset CamVid, clasificando cada píxel de una imagen dentro de una de las 32 clases disponibles.

---

## Objetivos específicos

* Cargar y preparar la base de datos CamVid.
* Procesar imágenes y máscaras de segmentación.
* Entrenar una arquitectura U-Net para segmentación semántica.
* Evaluar el desempeño del modelo mediante métricas especializadas.
* Guardar el mejor modelo obtenido durante el entrenamiento.
* Implementar una aplicación sencilla para realizar inferencia sobre nuevas imágenes.
* Visualizar la máscara de segmentación predicha sobre la imagen original.

---

## Modelo utilizado

El modelo utilizado corresponde a una arquitectura **U-Net**.

La U-Net es una red neuronal convolucional diseñada para tareas de segmentación. Su estructura se compone principalmente de dos partes:

1. **Encoder o codificador:** extrae características relevantes de la imagen mediante capas convolucionales.
2. **Decoder o decodificador:** reconstruye la información espacial para generar una máscara de segmentación.

Además, la U-Net utiliza conexiones entre el encoder y el decoder para conservar detalles espaciales importantes, lo cual mejora la precisión en los bordes y regiones pequeñas de la imagen.

---

## Configuración del experimento

La configuración principal usada en el entrenamiento fue:

| Parámetro              |                                    Valor |
| ---------------------- | ---------------------------------------: |
| Tamaño de imagen       |                                256 x 384 |
| Batch size             |                                        4 |
| Épocas                 |                                      100 |
| Learning rate          |                                   0.0003 |
| Weight decay           |                                   0.0001 |
| Canales base           |                                       32 |
| Número de clases       |                                       32 |
| Función de pérdida     | Combinación de Cross Entropy y Dice Loss |
| Peso Cross Entropy     |                                      0.7 |
| Peso Dice Loss         |                                      0.3 |
| Uso de pesos por clase |                                       Sí |
| Uso de AMP             |                                       Sí |

---

## Métricas de evaluación

Para evaluar el rendimiento del modelo se utilizaron métricas comunes en segmentación semántica:

### Pixel Accuracy

Mide el porcentaje de píxeles clasificados correctamente respecto al total de píxeles evaluados.

### mIoU

El mean Intersection over Union mide el promedio de intersección sobre unión entre la máscara predicha y la máscara real para las clases evaluadas.

### mDice

El mean Dice Score mide la similitud promedio entre las regiones predichas y las regiones reales.

### Loss

Representa el error del modelo durante el entrenamiento o evaluación. Un valor menor indica mejor ajuste del modelo.

---

## Resultados obtenidos

Los principales resultados del experimento fueron:

| Métrica                  |  Valor |
| ------------------------ | -----: |
| Mejor mIoU en validación | 0.4890 |
| Test loss                | 0.9810 |
| Test pixel accuracy      | 0.8652 |
| Test mIoU                | 0.4090 |
| Test mDice               | 0.5288 |

Estos resultados muestran que el modelo logra una buena precisión general por píxel, aunque la métrica mIoU evidencia que la segmentación por clase puede seguir mejorando, especialmente en clases pequeñas o menos frecuentes.

---

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
└── README.md
```

---

## Carpeta training

La carpeta `training` contiene los archivos relacionados con el entrenamiento del modelo.

### `proyecto-imagenes.ipynb`

Notebook principal del proyecto. En este archivo se realiza el proceso de carga de datos, preparación de imágenes y máscaras, definición del modelo, entrenamiento y evaluación.

### `best-model/best_camvid_unet.pth`

Archivo que contiene el mejor modelo entrenado en formato PyTorch.

### `parameters/experiment_summary.json`

Archivo que almacena información relevante del experimento, como:

* Nombre del proyecto.
* Ruta de la base de datos.
* Número de clases.
* Nombres de las clases.
* Configuración del entrenamiento.
* Ruta del mejor modelo.
* Métricas obtenidas en validación y prueba.

---

## Carpeta deployment

La carpeta `deployment` contiene los archivos relacionados con el despliegue del modelo.

### `app.py`

Aplicación que permite cargar una imagen y obtener como salida la segmentación predicha por el modelo.

La aplicación utiliza una interfaz con Gradio para facilitar la interacción con el usuario.

### `requirements.txt`

Archivo con las dependencias necesarias para ejecutar la aplicación.

### `Despliegue_Modelo_Proyecto_PDI.ipynb`

Notebook relacionado con el proceso de despliegue del modelo.

---

## Funcionamiento general del proyecto

El flujo general del proyecto es el siguiente:

1. Se carga la base de datos CamVid.
2. Se leen las imágenes urbanas y sus respectivas máscaras.
3. Se ajusta el tamaño de las imágenes a 256 x 384.
4. Se normalizan los valores de entrada.
5. Se entrena una red U-Net para segmentación semántica.
6. El modelo predice una clase para cada píxel de la imagen.
7. Se compara la máscara predicha con la máscara real.
8. Se calculan métricas como Pixel Accuracy, mIoU y mDice.
9. Se guarda el mejor modelo obtenido.
10. Se implementa una aplicación para probar el modelo con nuevas imágenes.

---

## Instalación

Para clonar el repositorio:

```bash
git clone https://github.com/jomendietad/pdi-project.git
cd pdi-project
```

Para instalar las dependencias del despliegue:

```bash
pip install -r deployment/requirements.txt
```

En caso de ser necesario, instalar también:

```bash
pip install gradio pillow opencv-python numpy torch
```

---

## Ejecución de la aplicación

Para ejecutar la aplicación:

```bash
cd deployment
python app.py
```

La aplicación permite cargar una imagen urbana y visualizar la máscara de segmentación generada por el modelo.

---

## Archivos necesarios para la inferencia

La aplicación de despliegue espera encontrar los siguientes archivos:

```text
experiment_summary.json
unet_camvid.pte
```

El archivo `experiment_summary.json` contiene la configuración del experimento y la paleta de colores de las clases.
El archivo `unet_camvid.pte` corresponde al modelo exportado para inferencia.

---

## Tecnologías utilizadas

* Python
* PyTorch
* U-Net
* OpenCV
* NumPy
* PIL
* Gradio
* ExecuTorch
* Kaggle
* CamVid Dataset

---

## Importancia del proyecto

Este proyecto permite aplicar conceptos de Procesamiento Digital de Imágenes y aprendizaje profundo a un problema real de visión por computador.

La segmentación semántica es una técnica importante porque permite comprender el contenido de una imagen a nivel de píxel. Esto tiene aplicaciones en áreas como:

* Vehículos autónomos.
* Sistemas inteligentes de transporte.
* Análisis de escenas urbanas.
* Robótica móvil.
* Monitoreo de espacios públicos.
* Asistencia a la conducción.

---

## Conclusión

El proyecto desarrolla un sistema de segmentación semántica urbana usando la base de datos CamVid y una arquitectura U-Net.

Se logró entrenar un modelo capaz de identificar diferentes elementos presentes en escenas urbanas y generar máscaras de segmentación sobre imágenes de entrada.

La base de datos utilizada fue CamVid, la cual es adecuada para este tipo de problema porque contiene imágenes reales de entornos urbanos con anotaciones píxel a píxel.

Los resultados obtenidos muestran un desempeño aceptable para un proyecto académico, con una precisión por píxel superior al 86% en prueba. Sin embargo, métricas como mIoU y mDice indican que todavía existen oportunidades de mejora, especialmente en clases pequeñas, poco frecuentes o visualmente similares.

---

## Autor

Proyecto desarrollado por:

```text
jomendietad  jomendietad@unal.edu.co
Sebastian-Torres-Gamboa setorresg@unal.edu.co
```

---

## Materia

Procesamiento Digital de Imágenes

---

## Tipo de proyecto

Segmentación semántica de imágenes urbanas usando aprendizaje profundo.
