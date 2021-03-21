from .cjs import CJS


def load_data(file):
    """"""

    loader = CJS()
    return loader.load(file)

def dump_data(data, file):
    """"""

    dumper = CJS()
    dumper.dump(data, file)
    