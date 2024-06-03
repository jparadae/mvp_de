import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import csv
import logging


class FormatData(beam.DoFn):
    def process(self, element):
        if element:  # Validando de que el elemento no sea None
            try:
                # Transformando nombres de columnas
                element['VehicleMake'] = element.pop('Make')
                element['VehicleModel'] = element.pop('Model')
                element['EVType'] = element.pop('Electric Vehicle Type')

                # Crea nuevas variables
                element['IsEligible'] = 1 if element.pop('Clean Alternative Fuel Vehicle (CAFV) Eligibility') == 'Clean Alternative Fuel Vehicle Eligible' else 0

                yield element
            except KeyError as e:
                logging.error(f"Error procesando el elemento: {element}. Error: {e}")
            else:
                logging.info("Elemento vacío encontrado")


def run():
    options = PipelineOptions()
    p = beam.Pipeline(options=options)

    # Ruta del archivo CSV en el sistema Windows
    input_file = r'C:/Users/javie/Desktop/D-E/YOM/mvp_de/mnt/data/Electric_Vehicle_Population_Data.csv'
    """ 
    # Ruta del archivo CSV en Cloud Storage GCP
    input_file = 'gs://bucket_name/path/to/input/Electric_Vehicle_Population_Data.csv'
    output_path = 'gs://bucket_name/path/to/output/'
    """
    headers = ['VIN (1-10)', 'County', 'City', 'State', 'Postal Code', 'Model Year', 'Make', 'Model', 'Electric Vehicle Type', 'Clean Alternative Fuel Vehicle (CAFV) Eligibility', 'Electric Range', 'Base MSRP', 'Legislative District', 'DOL Vehicle ID', 'Vehicle Location', 'Electric Utility', '2020 Census Tract']

    # Leer y procesar datos del CSV
    (
        p
        | "ReadCSV" >> beam.io.ReadFromText(input_file, skip_header_lines=1)
        | "ParseCSV" >> beam.Map(lambda line: dict(zip(headers, next(csv.reader([line])))) if line else None)
        | "FilterEmptyLines" >> beam.Map(lambda element: element if element else beam.Row())  # Filtrar filas vacías
        | "FormatData" >> beam.ParDo(FormatData())
        | "WriteOutput" >> beam.io.WriteToText(r'C:/Users/javie/Desktop/D-E/YOM/mvp_de/mnt/data/output/transformed_data', file_name_suffix='.csv', shard_name_template='')
    )

    p.run().wait_until_finish()
    """ 
    SE comenta esta linea para que en un futuro se pueda subir el archivo de salida a Cloud Storage
    upload_to_gcs(output_path)

def upload_to_gcs(output_path):
    client = storage.Client()
    bucket_name = "bucket_name"
    bucket = client.bucket(bucket_name)
    
    # Obtenemos la fecha actual
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Subir el archivo de salida al bucket
    blob = bucket.blob(f"output/transformed_data_{current_date}.csv")
    blob.upload_from_filename(output_path + '-00000-of-00001') """


if __name__ == "__main__":
    run()
