import unittest
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import BeamAssert

from data_pipeline import FormatData  

class FormatDataTest(unittest.TestCase):

    def test_format_data(self):
        test_data = [
            {'Make': 'Tesla', 'Model': 'Model 3', 'Electric Vehicle Type': 'Battery Electric',
             'Clean Alternative Fuel Vehicle (CAFV) Eligibility': 'Clean Alternative Fuel Vehicle Eligible'},
            {'Make': 'Toyota', 'Model': 'Prius', 'Electric Vehicle Type': 'Plug-in Hybrid',
             'Clean Alternative Fuel Vehicle (CAFV) Eligibility': 'Not Applicable'},
            {},  # Probando un elemento vacio
            {'ExtraColumn': 'This should be ignored'}, 
        ]

        expected_output = [
            {'VehicleMake': 'Tesla', 'VehicleModel': 'Model 3', 'EVType': 'Battery Electric', 'IsEligible': 1},
            {'VehicleMake': 'Toyota', 'VehicleModel': 'Prius', 'EVType': 'Plug-in Hybrid', 'IsEligible': 0},
            {},  # Probando un elemento vacio
            {'ExtraColumn': 'This should be ignored', 'VehicleMake': None, 'VehicleModel': None, 'EVType': None, 'IsEligible': None},  # Unexpected column is not removed
        ]

        with TestPipeline() as p:
            formatted_data = (p
                | beam.Create(test_data)
                | beam.ParDo(FormatData())
            )

            BeamAssert(formatted_data).equal_to(expected_output)

if __name__ == '__main__':
    unittest.main()
