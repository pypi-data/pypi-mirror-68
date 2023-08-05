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


if __name__ == "__main__":
    unittest.main()
