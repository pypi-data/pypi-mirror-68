import unittest
from strix.gca import GCA
from strix.file_formats import egf
from tests.file_formats.tests import egf_vars, gca_vars


class TestFromGCA(unittest.TestCase):

    def test_from_gca_point(self):
        # Valid Point
        pt = GCA(*gca_vars.gca_pt_components)
        self.assertEqual(egf.from_gca_point(pt), gca_vars.pt_as_egf)

    def test_from_gca_linestring(self):
        # Valid Linestring
        ls = GCA(gca_vars.ls_geom, gca_vars.ls_coords, gca_vars.ls_attrs)
        self.assertEqual(egf.from_gca_linestring(ls), gca_vars.ls_as_egf)

    def test_from_gca_polygon(self):
        # Valid Polygon
        poly = GCA(gca_vars.poly_geom, gca_vars.poly_coords, gca_vars.poly_attrs)
        self.assertEqual(egf.from_gca_polygon(poly), gca_vars.poly_as_egf)


class TestEGFValidate(unittest.TestCase):
    """
        Checks that the general structure of an GEF file is correct.
        - That the EGF is of a valid geometry type
        - That there are the correct number of sections in the EGF
        - That sections are separated by 3 blank lines
        - That there are the minimum number of coordinate sets required for declared geometry type
        - That the header section is a single line
        - That last line of file is blank

    """

    def setUp(self):
        self.pt = egf.EGFValidate(gca_vars.pt_as_egf)
        self.ls = egf.EGFValidate(gca_vars.ls_as_egf)
        self.poly = egf.EGFValidate(gca_vars.poly_as_egf)

    def test_sections(self):
        # Point Sections
        result = ['PT', 'Park Name, City, Pond, Fountain', 'Post office Square, Boston, FALSE, TRUE\n42.356243, -71.055631, 2.0', 'Boston Common, Boston, TRUE, TRUE\n42.355465, -71.066412, 10.0\n']
        self.assertEqual(self.pt.sections, result)
        self.assertRaises(AssertionError, egf.EGFValidate, egf_vars.invalid_pt_sections)

        # Linestring Sections
        result = ['LS', 'Park Name, Feature Description', 'Post Office Square, A walk by the fountain\n42.356716, -71.055685, 0.0\n42.356587, -71.055769, 0.0\n42.356566, -71.055754, 0.0\n42.356539, -71.055746, 0.0\n42.356511, -71.055757, 0.0\n42.356495, -71.05579, 0.0\n42.356485, -71.05583, 0.0\n42.356389, -71.055842, 0.0\n42.356252, -71.055796, 0.0\n42.356046, -71.055642, 0.0\n42.355876, -71.055697, 0.0\n42.355828, -71.055758, 0.0', 'Boston Common, A walk by the fountain\n42.356251, -71.062737, 0.0\n42.35621, -71.063012, 0.0\n42.356153, -71.06305, 0.0\n42.356144, -71.063115, 0.0\n42.356136, -71.063261, 0.0\n42.355825, -71.064018, 0.0\n']
        self.assertEqual(self.ls.sections, result)
        self.assertRaises(AssertionError, egf.EGFValidate, egf_vars.invalid_ls_sections)

        # Polygon Sections
        result = ['POLY', 'Park Name, Feature Description', 'Post Office Square, Boundary of Post Office Square with holes for buildings\n42.356856, -71.055757, 0.0\n42.35608, -71.054976, 0.0\n42.355697, -71.055636, 0.0\n42.356003, -71.055941, 0.0\n42.356767, -71.05622, 0.0\n42.356856, -71.055757, 0.0\n\n42.355955, -71.055522, 0.0\n42.355894, -71.055458, 0.0\n42.355846, -71.055546, 0.0\n42.355908, -71.055615, 0.0\n42.355955, -71.055522, 0.0\n\n42.356089, -71.055312, 0.0\n42.356005, -71.055226, 0.0\n42.355969, -71.055288, 0.0\n42.356058, -71.055373, 0.0\n42.356089, -71.055312, 0.0', 'Boston Common, Boundary of Boston Common with a hole for the Frog Pond\n42.356514, -71.062157, 0.0\n42.355222, -71.063337, 0.0\n42.352457, -71.064638, 0.0\n42.352639, -71.067238, 0.0\n42.356132, -71.06915, 0.0\n42.357591, -71.06326, 0.0\n42.356514, -71.062157, 0.0\n\n42.356047, -71.065045, 0.0\n42.355953, -71.065107, 0.0\n42.355911, -71.065249, 0.0\n42.356018, -71.065909, 0.0\n42.35601, -71.066016, 0.0\n42.355918, -71.066198, 0.0\n42.355854, -71.066417, 0.0\n42.355876, -71.066521, 0.0\n42.355938, -71.066564, 0.0\n42.355985, -71.066547, 0.0\n42.356221, -71.066, 0.0\n42.356296, -71.065647, 0.0\n42.35627, -71.065341, 0.0\n42.356186, -71.065127, 0.0\n42.356123, -71.065061, 0.0\n42.356047, -71.065045, 0.0\n']
        self.assertEqual(self.poly.sections, result)

    def test_geom_type(self):
        # Valid geometry types
        self.assertEqual(self.pt.geom_type(), gca_vars.pt_geom)
        self.assertEqual(self.ls.geom_type(), gca_vars.ls_geom)
        self.assertEqual(self.poly.geom_type(), gca_vars.poly_geom)

        # Invalid geometry type
        self.assertRaises(AssertionError, egf.EGFValidate, egf_vars.invalid_pt_geom)

    def test_last_line_blank(self):
        # Valid last line
        self.assertEqual(self.pt.last_line_blank(), True)
        self.assertEqual(self.ls.last_line_blank(), True)
        self.assertEqual(self.poly.last_line_blank(), True)

        # Invalid last line
        self.assertRaises(AssertionError, egf.EGFValidate, egf_vars.invalid_pt_last_line_1)
        self.assertRaises(AssertionError, egf.EGFValidate, egf_vars.invalid_pt_last_line_2)

    def test_headers_single_line(self):
        # Valid headers
        self.assertEqual(self.pt.headers_single_line(), True)
        self.assertEqual(self.ls.headers_single_line(), True)
        self.assertEqual(self.poly.headers_single_line(), True)

        # Invalid headers
        self.assertRaises(AssertionError, egf.EGFValidate, egf_vars.invalid_pt_headers)

    def test_section_separators(self):
        # Valid section separations
        self.assertEqual(self.pt.section_separators(), True)
        self.assertEqual(self.ls.section_separators(), True)
        self.assertEqual(self.poly.section_separators(), True)

        # Invalid section separations
        self.assertRaises(AssertionError, egf.EGFValidate, egf_vars.invalid_pt_section_separators)

    def test_min_coord_sets(self):
        # Valid number of coordinate sets
        self.assertEqual(self.pt.min_coord_sets(), True)
        self.assertEqual(self.ls.min_coord_sets(), True)
        self.assertEqual(self.poly.min_coord_sets(), True)

        # Invalid number of coordinate sets
        self.assertRaises(AssertionError, egf.EGFValidate, egf_vars.invalid_pt_coord_sets)
        self.assertRaises(AssertionError, egf.EGFValidate, egf_vars.invalid_ls_coord_sets_1)
        self.assertRaises(AssertionError, egf.EGFValidate, egf_vars.invalid_ls_coord_sets_2)
        self.assertRaises(AssertionError, egf.EGFValidate, egf_vars.invalid_poly_coord_sets_1)
        self.assertRaises(AssertionError, egf.EGFValidate, egf_vars.invalid_poly_coord_sets_2)


class TestToGCA(unittest.TestCase):

    def test_to_gca_point_components(self):
        # Valid Point
        result = (gca_vars.pt_geom, gca_vars.pt_coords, gca_vars.pt_attrs)
        self.assertEqual(egf.to_gca_point_components(gca_vars.pt_as_egf), result)

    def test_to_gca_linestring_components(self):
        # Valid Linestring
        result = (gca_vars.ls_geom, gca_vars.ls_coords, gca_vars.ls_attrs)
        self.assertEqual(egf.to_gca_linestring_components(gca_vars.ls_as_egf), result)

    def test_to_gca_polygon_components(self):
        # Valid Polygon
        result = (gca_vars.poly_geom, gca_vars.poly_coords, gca_vars.poly_attrs)
        self.assertEqual(egf.to_gca_polygon_components(gca_vars.poly_as_egf), result)


if __name__ == '__main__':
    unittest.main()
