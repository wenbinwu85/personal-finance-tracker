from .cjs import CJS


def load_data(file):
    """"""
    return CJS().load(file)

def dump_data(data, file):
    """"""
    CJS().dump(data, file)
