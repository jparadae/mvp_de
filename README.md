# Data Pipeline Project MVP para YOM

## Descripción

Este proyecto implementa un pipeline de procesamiento de datos utilizando Apache Beam, orquestado con Apache Airflow y desplegado en Google Cloud Dataflow.

## Estructura del Proyecto

- `mvp_de/`: Archivos de datos de entrada.
- `mnt/`: Directorio procesamiento CSV de input y output.
- `tests/`: Pruebas unitarias.
- `data_pipeline.py`: Código fuente del pipeline.
- `README.md`: Documentación del proyecto.
- `requirements.txt`: Dependencias del proyecto.

## Instrucciones

1. Instalar dependencias:
    ```sh
    pip install -r requirements.txt
    ```
2. Ejecutar el pipeline:
    ```sh
    python data_pipeline.py
    ```
3. Desplegar en Google Cloud:
    ```sh
    python data_pipeline.py --runner DataflowRunner --project YOUR_PROJECT --temp_location gs://YOUR_BUCKET/temp
    ```

## Git y CI/CD

Este proyecto utiliza GitHub Actions para CI/CD. Las pruebas se ejecutan automáticamente al hacer push en la rama `main`.
