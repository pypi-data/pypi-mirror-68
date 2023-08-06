import strix
from tests.file_formats.tests import gca_vars
from strix.file_formats import geo_json

gca = strix.GCA(*gca_vars.gca_poly_components)

print(geo_json.from_gca(gca, visualize=True))

# print(strix.file_actions.read_csv("/Users/henryiii/Documents/csvtest.csv"))
