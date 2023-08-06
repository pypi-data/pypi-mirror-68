import unittest
from strix import gca
from tests.file_formats.tests import gca_vars


class TestGCA(unittest.TestCase):

    def setUp(self):
        self.pt = gca.GCA(gca_vars.pt_geom, gca_vars.pt_coords, gca_vars.pt_attrs)
        self.ls = gca.GCA(gca_vars.ls_geom, gca_vars.ls_coords, gca_vars.ls_attrs)
        self.poly = gca.GCA(gca_vars.poly_geom, gca_vars.poly_coords, gca_vars.poly_attrs)

    def test_gca_geomtype(self):
        # Point
        self.assertEqual(self.pt.geometry_type, gca_vars.pt_geom)

        # Linestring
        self.assertEqual(self.ls.geometry_type, gca_vars.ls_geom)

        # Polygon
        self.assertEqual(self.poly.geometry_type, gca_vars.poly_geom)

    def test_gca_headers(self):
        # Point
        self.assertEqual(self.pt.headers, gca_vars.pt_attrs[0])

        # Linestring
        self.assertEqual(self.ls.headers, gca_vars.ls_attrs[0])

        # Polygon
        self.assertEqual(self.poly.headers, gca_vars.poly_attrs[0])

    def test_gca_attributes(self):
        # Point
        self.assertEqual(self.pt.attributes, gca_vars.pt_attrs[1:])

        # Linestring
        self.assertEqual(self.ls.attributes, gca_vars.ls_attrs[1:])

        # Polygon
        self.assertEqual(self.poly.attributes, gca_vars.poly_attrs[1:])

    def test_gca_coord_sets(self):
        # Point
        self.assertEqual(self.pt.coord_sets, gca_vars.pt_coords)

        # Linestring
        self.assertEqual(self.ls.coord_sets, gca_vars.ls_coords)

        # Polygon
        self.assertEqual(self.poly.coord_sets, gca_vars.poly_coords)

    def test_gca_features(self):
        # Point
        self.assertEqual(self.pt.features, gca_vars.pt_features)

        # Linestring
        self.assertEqual(self.ls.features, gca_vars.ls_features)

        # Polygon
        self.assertEqual(self.poly.features, gca_vars.poly_features)


if __name__ == '__main__':
    unittest.main()
