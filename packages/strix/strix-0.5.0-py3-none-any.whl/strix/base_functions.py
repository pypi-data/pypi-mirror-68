from strix import file_actions as fa
from strix.file_formats import egf
from strix.file_formats import csv
from strix.file_formats import geo_json

__all__ = ["read_egf", "write_egf", "write_geojson", "read_csv", "write_csv"]


def read_egf(file_path):
    egf_as_str = fa.str_file_read(file_path)
    egf_as_gca = egf.to_gca(egf_as_str)

    return egf_as_gca


def write_egf(file_path, gca_obj):
    gca_as_egf = egf.from_gca(gca_obj)
    fa.text_writer(file_path, gca_as_egf)

    return gca_as_egf


def write_geojson(file_path, gca_obj, visualize=False):
    gca_as_json_str = geo_json.from_gca(gca_obj, visualize)
    fa.text_writer(file_path, gca_as_json_str)

    return gca_as_json_str


def read_csv(file_path):
    csv_as_list = fa.read_csv(file_path)
    csv_as_gca = csv.to_gca(csv_as_list)

    return csv_as_gca


def write_csv(file_path, gca_obj):
    gca_as_csv = csv.from_gca(gca_obj)
    fa.write_csv(file_path, gca_as_csv)
