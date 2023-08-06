import unittest
from strix.gca import GCA
from strix.file_formats import geo_json
from tests.file_formats.tests import gca_vars


class TestFromGCA(unittest.TestCase):

    def test_from_gca_point(self):
        # Valid Point
        pt = GCA(*gca_vars.gca_pt_components)
        self.assertEqual(geo_json.from_gca(pt), gca_vars.pt_as_json)
        # Valid Linestring
        ls = GCA(*gca_vars.gca_ls_components)
        self.assertEqual(geo_json.from_gca(ls), gca_vars.ls_as_json)
        # Valid Polygon
        poly = GCA(*gca_vars.gca_poly_components)
        self.assertEqual(geo_json.from_gca(poly), gca_vars.poly_as_json)


if __name__ == '__main__':
    unittest.main()