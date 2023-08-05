import unittest
from ...Read import InowasModflowReadAdapter


class InowasModflowReadAdapterTest(unittest.TestCase):
    def it_can_be_instantiated_test(self):
        instance = InowasModflowReadAdapter()
        self.assertIsInstance(instance, InowasModflowReadAdapter)

    def it_throws_exception_if_path_is_wrong_test(self):
        with self.assertRaises(FileNotFoundError) as context:
            InowasModflowReadAdapter.load('abc')
        self.assertEqual('Path not found: abc', str(context.exception))

    def it_throws_exception_if_path_does_not_contain_name_file_test(self):
        with self.assertRaises(FileNotFoundError) as context:
            InowasModflowReadAdapter.load('./FlopyAdapter/test/Read/data/emptyFolder')
        self.assertEqual('Modflow name file with ending .nam or .mfn not found', str(context.exception))

    def it_loads_the_model_correctly_test(self):
        instance = InowasModflowReadAdapter.load('./FlopyAdapter/test/Read/data/test_example_1')
        self.assertIsInstance(instance, InowasModflowReadAdapter)

    def it_converts_wgs84_to_utm_correctly_test(self):
        lat = 50.966319
        long = 13.923273
        easting, northing, zone_number, zone_letter = InowasModflowReadAdapter.wgs82ToUtm(long, lat)
        self.assertEqual(round(easting), 424393)
        self.assertEqual(round(northing), 5646631)
        self.assertEqual(zone_number, 33)
        self.assertEqual(zone_letter, 'U')

    def it_converts_utm_to_wgs84_correctly_test(self):
        easting, northing, zone_number, zone_letter = 424393, 5646631, 33, 'U'
        long, lat = InowasModflowReadAdapter.utmToWgs82XY(easting, northing, zone_number, zone_letter)
        self.assertEqual(round(long, 5), 13.92328)
        self.assertEqual(round(lat, 5), 50.96632)

    def it_returns_a_model_geometry_correctly_test(self):
        instance = InowasModflowReadAdapter.load('./FlopyAdapter/test/Read/data/test_example_1')
        self.assertIsInstance(instance, InowasModflowReadAdapter)
        geometry = instance.model_geometry(279972.0566, 9099724.9436, 31985, 0, 0)
        self.assertEqual(geometry["type"], 'Polygon')
        self.assertEqual(len(geometry["coordinates"][0]), 520)
        self.assertEqual(geometry["coordinates"][0][0], [-34.896872, -8.04386])

        geometry = instance.model_geometry(279972.0566, 9099724.9436, 31985, -15.5, 0)
        self.assertEqual(geometry["type"], 'Polygon')
        self.assertEqual(len(geometry["coordinates"][0]), 520)
        self.assertEqual(geometry["coordinates"][0][0], [-34.874832, -8.073986])

    def it_returns_model_gid_size_test(self):
        instance = InowasModflowReadAdapter.load('./FlopyAdapter/test/Read/data/test_example_1')
        self.assertIsInstance(instance, InowasModflowReadAdapter)
        grid_size = instance.model_grid_size()
        self.assertEqual(grid_size, {
            'n_x': 227,
            'n_y': 221,
        })

    def it_returns_model_stressperiods_test(self):
        instance = InowasModflowReadAdapter.load('./FlopyAdapter/test/Read/data/test_example_1')
        self.assertIsInstance(instance, InowasModflowReadAdapter)
        stress_periods = instance.model_stress_periods()
        expected = {
            'start_date_time': '1970-01-01',
            'end_date_time': '1970-02-06',
            'time_unit': 4,
            'stressperiods': [
                {
                    'start_date_time': '1970-01-01',
                    'nstp': 1,
                    'tsmult': 1.0,
                    'steady': True,
                },
                {
                    'start_date_time': '1970-01-02',
                    'nstp': 5,
                    'tsmult': 1.0,
                    'steady': False,
                },
                {
                    'start_date_time': '1970-01-12',
                    'nstp': 10,
                    'tsmult': 1.5,
                    'steady': False,
                }
            ]
        }
        self.assertEqual(stress_periods, expected)

    def it_returns_model_length_unit_test(self):
        instance = InowasModflowReadAdapter.load('./FlopyAdapter/test/Read/data/test_example_1')
        self.assertIsInstance(instance, InowasModflowReadAdapter)
        length_unit = instance.model_length_unit()
        self.assertEqual(length_unit, 2)

    def it_returns_model_time_unit_test(self):
        instance = InowasModflowReadAdapter.load('./FlopyAdapter/test/Read/data/test_example_1')
        self.assertIsInstance(instance, InowasModflowReadAdapter)
        time_unit = instance.model_time_unit()
        self.assertEqual(time_unit, 4)

    def it_returns_wel_boundaries_of_example_1_test(self):
        instance = InowasModflowReadAdapter.load('./FlopyAdapter/test/Read/data/test_example_1')
        self.assertIsInstance(instance, InowasModflowReadAdapter)
        wel_boundaries = instance.wel_boundaries(279972.0566, 9099724.9436, 31985, -15.5)
        self.assertEqual(len(wel_boundaries), 93)
        self.assertEqual(wel_boundaries[0], {
            'type': 'wel',
            'name': 'Well 1',
            'geometry': {"coordinates": [-34.879086, -8.084038], "type": "Point"},
            'layers': [0],
            'sp_values': [-2039.0, -2039.0, -2039.0]
        })

    def it_returns_wel_boundaries_of_example_2_test(self):
        instance = InowasModflowReadAdapter.load('./FlopyAdapter/test/Read/data/test_example_2')
        self.assertIsInstance(instance, InowasModflowReadAdapter)
        wel_boundaries = instance.wel_boundaries(0, 0, 4326, 0)
        self.assertEqual(len(wel_boundaries), 6)
        self.assertEqual(wel_boundaries, [
            {
                'type': 'wel',
                'name': 'Well 1',
                'geometry': {"coordinates": [0.013454, 0.040657], "type": "Point"},
                'layers': [0],
                'sp_values': [0, -5000.0, -5000.0]
            },
            {
                'type': 'wel',
                'name': 'Well 2',
                'geometry': {"coordinates": [0.022429, 0.040658], "type": "Point"},
                'layers': [0],
                'sp_values': [0, -5000.0, -5000.0]
            },
            {
                'type': 'wel',
                'name': 'Well 3',
                'geometry': {"coordinates": [0.058327, 0.040659], "type": "Point"},
                'layers': [0],
                'sp_values': [0, -10000.0, -10000.0]
            },
            {
                'type': 'wel',
                'name': 'Well 4',
                'geometry': {"coordinates": [0.085252, 0.04066], "type": "Point"},
                'layers': [0],
                'sp_values': [0, -5000.0, -5000.0]
            },
            {
                'type': 'wel',
                'name': 'Well 5',
                'geometry': {"coordinates": [0.013454, 0.022587], "type": "Point"},
                'layers': [0],
                'sp_values': [0, -5000.0, -5000.0]
            },
            {
                'type': 'wel',
                'name': 'Well 6',
                'geometry': {"coordinates": [0.040379, 0.013553], "type": "Point"},
                'layers': [0],
                'sp_values': [0, -5000.0, -5000.0]
            }
        ])


if __name__ == "__main__":
    unittest.main()
