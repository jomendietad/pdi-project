# PDI Project - Hugging Face Deployment & Artifact Generation

Este directorio contiene los archivos de configuración y la bitácora de automatización utilizados para compilar, optimizar y desplegar el modelo de segmentación semántica en la plataforma de producción web **Hugging Face Spaces**. 

Este espacio actúa como un registro transparente de la canalización (*pipeline*) de despliegue para la evaluación del proyecto de Procesamiento Digital de Imágenes.

## Entorno de Despliegue

Esta aplicación se encuentra desplegada y funcionando a través de Hugging Face Spaces. 

* **Aplicación en vivo:** [https://huggingface.co/spaces/jomendietad/pdi-project](https://huggingface.co/spaces/jomendietad/pdi-project)
* **Framework utilizado:** Gradio / Streamlit *(Nota: ajusta esto según lo que estés usando)*

Todos los archivos contenidos en este directorio están destinados a dicho entorno. Las dependencias listadas en el archivo `requirements.txt` y la lógica principal contenida en `app.py` son leídas y ejecutadas directamente por Hugging Face para construir la aplicación web.

---

## Estructura del Directorio

* `Despliegue_Modelo_Proyecto_PDI.ipynb`: Notebook principal que ejecuta de extremo a extremo el flujo de compilación, optimización y publicación automática.
* `app.py`: Script de la aplicación web que define la interfaz gráfica interactiva en **Gradio** y gestiona el ciclo de inferencia del modelo.
* `requirements.txt`: Declaración estricta de las dependencias de Python requeridas por el contenedor de Hugging Face para construir el entorno aislado.

---

## Documentación del Proceso Paso a Paso (`Despliegue_Modelo_Proyecto_PDI.ipynb`)

El notebook describe y ejecuta una metodología estricta para transformar el modelo de investigación basado en PyTorch clásico en un artefacto altamente optimizado para arquitecturas Edge mediante el ecosistema **ExecuTorch**, culminando en un despliegue automatizado. El flujo se divide en las siguientes etapas consecutivas:

### Pasó 1: Aprovisionamiento del Entorno de Compilación
Se realiza la instalación de los paquetes base de ExecuTorch junto con las herramientas del sistema necesarias para compilar y enlazar los operadores gráficos requeridos por la arquitectura del modelo.

### Paso 2: Carga del Modelo y Trazado del Grafo (`torch.export`)
* Se instancia la arquitectura de la red neuronal y se cargan los pesos previamente entrenados (`best_camvid_unet.pth`).
* Utilizando un tensor de ejemplo (*dummy tensor*) estructurado estrictamente bajo las dimensiones de entrada del conjunto de datos **CamVid**, se invoca la API `torch.export` para capturar el grafo estático de la red y registrar el flujo de operaciones.

### Paso 3: Conversión al Dialecto Edge
El grafo capturado en el paso anterior se procesa mediante la función `to_edge_transform_and_lower()`. Esta etapa reduce la complejidad de los operadores de alto nivel de PyTorch, transformándolos en un conjunto restringido de operaciones estandarizadas y eficientes de bajo nivel optimizadas para dispositivos embebidos.

### Paso 4: Optimización mediante Delegado XNNPACK
Para garantizar una inferencia de baja latencia en entornos de computación en la nube basados en CPU, se invoca el particionador de **XNNPACK**. Este analiza el grafo de bajo nivel y delega la ejecución de los operadores gráficos (como convoluciones e interpolaciones) a núcleos altamente optimizados de XNNPACK. Tras esto, el grafo final y sus parámetros se serializan en un binario plano de extensión `.pte` (`unet_camvid.pte`).

### Paso 5: Generación de Archivos de la Aplicación
El notebook escribe de manera procedural los archivos necesarios para la interfaz web dentro del espacio de trabajo:
* Genera `requirements.txt` con los componentes mínimos del *runtime*.
* Estructura `app.py` integrando las funciones de preprocesamiento, la inicialización del motor de ejecución nativo de ExecuTorch para leer el archivo `.pte`, y el diseño de la interfaz de usuario con Gradio.

### Paso 6: Autenticación y Despliegue Automatizado en Hugging Face
La fase final del script interactúa directamente con la infraestructura de Hugging Face de la siguiente manera:
1. Solicita un token de acceso con permisos de escritura (`Hugging Face Write Token`) y el nombre del espacio destino.
2. Clona el repositorio remoto del espacio de Hugging Face de forma local en el entorno de ejecución.
3. Configura **Git LFS (Large File Storage)** para rastrear y gestionar el archivo pesado `.pte` generado de manera transitoria, evitando bloqueos en el control de versiones estándar.
4. Sincroniza los artefactos (`app.py`, `requirements.txt` y `unet_camvid.pte`) y realiza un `git push` definitivo para disparar la construcción automática del contenedor en la nube.
