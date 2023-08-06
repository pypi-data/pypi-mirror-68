import unittest
from strix.gca import GCA
from strix.file_formats import csv
from tests.file_formats.tests import gca_vars, csv_vars


class TestFromGCA(unittest.TestCase):

    def test_from_gca_point(self):
        # Valid Point
        pt = GCA(gca_vars.pt_geom, gca_vars.pt_coords, gca_vars.pt_attrs)
        self.assertEqual(csv.from_gca_point(pt), gca_vars.pt_as_csv)
        self.assertEqual(csv.from_gca_point(pt, True), gca_vars.pt_as_csv_xyz_and_geometry_true)
        self.assertEqual(csv.from_gca_point(pt, False, False), gca_vars.pt_as_csv_xyz_and_geometry_false)

    def test_from_gca_linestring(self):
        # Valid Linestring
        ls = GCA(gca_vars.ls_geom, gca_vars.ls_coords, gca_vars.ls_attrs)
        self.assertEqual(csv.from_gca_linestring(ls), gca_vars.ls_as_csv)

    def test_from_gca_polygon(self):
        # Valid Linestring
        poly = GCA(gca_vars.poly_geom, gca_vars.poly_coords, gca_vars.poly_attrs)
        self.assertEqual(csv.from_gca_polygon(poly), gca_vars.poly_as_csv)


class TestToGCA(unittest.TestCase):

    def test_to_gca_point_components(self):
        # Valid Point
        result = gca_vars.gca_pt_components
        csv_in = csv_vars.pt_csv_parsed
        self.assertEqual(csv.to_gca_point_components(csv_in), result)

    def test_to_gca_linestring_components(self):
        # Valid Linestring
        result = (gca_vars.ls_geom, gca_vars.ls_coords, gca_vars.ls_attrs)
        csv_in = csv_vars.ls_csv_parsed
        self.assertEqual(csv.to_gca_linestring_components(csv_in), result)

    def test_to_gca_polygon_components(self):
        # Valid Polygon
        result = (gca_vars.poly_geom, gca_vars.poly_coords, gca_vars.poly_attrs)
        csv_in = csv_vars.poly_csv_parsed
        self.assertEqual(csv.to_gca_polygon_components(csv_in), result)


class TestCSVGeomDetect(unittest.TestCase):

    def test_csv_geom_detect(self):
        # Valid Header
        pt_headers_1 = ['ID', 'NAME', 'GEOMETRY_PT']
        self.assertEqual(csv.csv_geom_detect(pt_headers_1), 'PT')

        pt_headers_1 = ['ID', 'NAME', 'GEOMETRY_LS']
        self.assertEqual(csv.csv_geom_detect(pt_headers_1), 'LS')

        pt_headers_1 = ['ID', 'NAME', 'GEOMETRY_POLY']
        self.assertEqual(csv.csv_geom_detect(pt_headers_1), 'POLY')

        # Invalid headers
        pt_headers_2 = ['ID', 'GEOMETRY_PT', 'GEOMETRY_LS', 'GEOMETRY_POLY']
        pt_headers_3 = ['ID', 'NAME', 'GEOMETRY_PT', 'GEOMETRY_PT']

        self.assertRaises(AssertionError, csv.csv_geom_detect, pt_headers_2)
        self.assertRaises(AssertionError, csv.csv_geom_detect, pt_headers_3)


if __name__ == '__main__':
    unittest.main()
