from openpyxl.cell.cell import Cell

import types


def values(val):
    if isinstance(val, types.GeneratorType):
        val = tuple(val)

    if isinstance(val, Cell):
        return from_cell(val)
    elif isinstance(val, tuple):
        if isinstance(val[0], Cell):
            return from_array(val)
        else:
            return from_range(val)
    else:
        return val


def from_cell(cell):
    if type(cell) is Cell:
        return cell.value
    else:
        return cell


def from_array(row):
    return list(from_cell(cell) for cell in list(row))


def from_range(range_):
    return list([from_array(row) for row in list(range_)])
