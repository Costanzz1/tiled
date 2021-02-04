import dask.array
import h5py


class ArraySource:
    def __init__(self, data):
        self.metadata = {}
        self._data = dask.array.from_array(data)

    def __repr__(self):
        return f"{type(self).__name__}({self._data!r})"

    def describe(self):
        return {
            "shape": self._data.shape,
            "chunks": self._data.chunks,
            "dtype": self._data.dtype.str,
        }

    def read(self):
        return self._data


class HDF5DatasetSource:
    def __init__(self, filepath, dataset_path):
        self._file = h5py.File(filepath)
        self._dataset_path = dataset_path
        dataset = self._file[dataset_path]
        self._data = dask.array.from_array(dataset)

    def __repr__(self):
        return f"{type(self).__name__}({self._data!r}, {self._dataset_path!r})"

    def describe(self):
        return {
            "shape": self._data.shape,
            "chunks": self._data.chunks,
            "dtype": self._data.dtype.str,
        }

    def read(self):
        return self._data
