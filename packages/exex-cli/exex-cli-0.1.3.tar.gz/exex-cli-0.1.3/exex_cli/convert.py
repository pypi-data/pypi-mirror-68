import csv
import json
from io import StringIO

from exex_cli.util import array_dimensions


def to_string(value):
    if isinstance(value, int):
        return str(value)
    elif value:
        return str(value)
    else:
        return ""


def to_strings(values):
    outer_dim, inner_dim = array_dimensions(values)

    if outer_dim == 0 and inner_dim == 0:
        return to_string(values)
    elif inner_dim == 0:
        return list(map(to_string, values))
    else:
        return [list(map(to_string, row)) for row in values]


def to_csv(values, delimiter=","):
    newline = "\n"

    if values is None or (isinstance(values, list) and not values):
        return newline

    outer_dim, inner_dim = array_dimensions(values)

    if outer_dim == 0 and inner_dim == 0:
        rows = [[values]]
    elif inner_dim == 0:
        rows = [values]
    else:
        rows = values

    fileobj = StringIO()
    csv_writer = csv.writer(fileobj, delimiter=delimiter, lineterminator=newline)
    csv_writer.writerows(rows)
    csv_string = fileobj.getvalue()
    fileobj.close()

    return csv_string


def to_json(values):
    return json.dumps(values, indent=2)
