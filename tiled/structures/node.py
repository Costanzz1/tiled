import io

from ..media_type_registration import serialization_registry
from ..utils import modules_available


def walk(node, pre=None):
    """
    Yield (key_path, value) where each value is an ArrayAdapter.

    As a succinct illustration (does not literally run):

    >>> list(walk{"a": {"b": 1, "c": {"d": 2}}})
    [
        (("a", "b"), 1),
        (("a", "c", "d"), 2),
    ]
    """
    pre = pre[:] if pre else []
    if node.structure_family != "array":
        for key, value in node.items():
            for d in walk(value, pre + [key]):
                yield d
    else:
        yield (pre, node)


if modules_available("h5py"):

    def serialize_hdf5(node, metadata):
        """
        Encode everything below this node as HDF5.

        Walk node. Encode all nodes an dataframes as Groups, all arrays and columns as Datasets.
        """
        import h5py

        buffer = io.BytesIO()
        with h5py.File(buffer, mode="w") as file:
            for key_path, array_adapter in walk(node):
                group = file
                for key in key_path[:-1]:
                    if key in group:
                        group = group[key]
                    else:
                        group = group.create_group(key)
                data = array_adapter.read()
                group.create_dataset(key_path[-1], data=data)
        return buffer.getbuffer()


serialization_registry.register("node", "application/x-hdf5", serialize_hdf5)
