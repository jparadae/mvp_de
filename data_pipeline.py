import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import csv

class FormatData(beam.DoFn):
    def process(self, element):
        if element:  # Validando de que el elemento no sea None
            try:
                # Transformando nombres de columnas
                element['VehicleMake'] = element.pop('Make')
                element['VehicleModel'] = element.pop('Model')
                element['EVType'] = element.pop('Electric Vehicle Type')
                # Creando nuevas variables
                element['IsEligible'] = 1 if element.pop('Clean Alternative Fuel Vehicle (CAFV) Eligibility') == 'Clean Alternative Fuel Vehicle Eligible' else 0
                yield element
            except KeyError as e:
                print(f"Error procesando el elemento: {element}. Error: {e}")
        else:
            print("Elemento vacío encontrado")

def run():
    options = PipelineOptions()
    p = beam.Pipeline(options=options)

    # Ruta del archivo CSV en el sistema Windows
    input_file = r'C:/Users/javie/Desktop/D-E/YOM/mvp_de/mnt/data/Electric_Vehicle_Population_Data.csv'

    headers = ['VIN (1-10)', 'County', 'City', 'State', 'Postal Code', 'Model Year', 'Make', 'Model', 'Electric Vehicle Type', 'Clean Alternative Fuel Vehicle (CAFV) Eligibility', 'Electric Range', 'Base MSRP', 'Legislative District', 'DOL Vehicle ID', 'Vehicle Location', 'Electric Utility', '2020 Census Tract']

    # Leer y procesar datos del CSV
    (p
     | 'ReadCSV' >> beam.io.ReadFromText(input_file, skip_header_lines=1)
     | 'ParseCSV' >> beam.Map(lambda line: dict(zip(headers, next(csv.reader([line])))) if line else None)
     | 'PrintParsedData' >> beam.Map(print)  # Imprimir datos parseados
     | 'TransformData' >> beam.ParDo(FormatData())
     | 'PrintTransformedData' >> beam.Map(print)  # Imprimir datos transformados
     | 'WriteOutput' >> beam.io.WriteToText(r'C:/Users/javie/Desktop/D-E/YOM/mvp_de/mnt/data/output/transformed_data', file_name_suffix='.csv', shard_name_template=''))

    p.run().wait_until_finish()

if __name__ == '__main__':
    run()
