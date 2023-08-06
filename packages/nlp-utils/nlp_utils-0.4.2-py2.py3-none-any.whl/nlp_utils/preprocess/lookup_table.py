import json
from typing import Union, List, Tuple, Hashable, Any


class LookupTable(object):
    def __init__(
        self,
        table: Union[dict, list, tuple],
        oov=None,
        oov_key=None,
        inverse_oov=None,
        inverse_oov_key=None,
    ):
        if isinstance(table, (list, tuple)):
            table = {v: k for k, v in enumerate(table)}
        if not isinstance(table, dict):
            raise ValueError(
                "table argument do not accept type: {}".format(type(table))
            )

        if oov is not None and oov_key is not None:
            raise ValueError("Only one of oov and oov_key can be set to non None")
        if inverse_oov is not None and inverse_oov_key is not None:
            raise ValueError(
                "Only one of inverse_oov and inverse_oov_key can be set to non None"
            )

        self.table = table
        self.inverse_table = {v: k for k, v in table.items()}
        if len(self.table) != len(self.inverse_table):
            raise ValueError(
                "table values are duplicated, reverse table cannot be created"
            )

        self.oov = oov
        self.oov_key = oov_key
        self.inverse_oov = inverse_oov
        self.inverse_oov_key = inverse_oov_key

        if self.oov is not None and self.oov not in self.table.values():
            print("WARNING: oov not in table")
        if self.oov_key is not None and self.oov_key not in self.table.keys():
            raise ValueError("WARNING: oov_key not in table")
        if (
            self.inverse_oov is not None
            and self.inverse_oov not in self.inverse_table.values()
        ):
            print("WARNING: inverse_oov not in inverse_table")
        if (
            self.inverse_oov_key is not None
            and self.inverse_oov_key not in self.inverse_table.keys()
        ):
            raise ValueError("WARNING: inverse_oov_key not in inverse_table")

    def __call__(self, key):
        return self.batch_lookup(key)

    def batch_lookup(self, key):
        return [self.lookup(i) for i in key]

    def lookup(
        self, key: Union[Hashable, List[Hashable], Tuple[Hashable]]
    ) -> Union[Any, List[Any]]:
        if isinstance(key, (list, tuple)):
            return tuple(self._do_lookup(i) for i in key)
        return self._do_lookup(key)

    def _do_lookup(self, key: Hashable) -> Any:
        try:
            return self.table[key]
        except KeyError:
            if self.oov is not None:
                return self.oov
            elif self.oov_key is not None:
                return self.table[self.oov_key]
            else:
                raise

    def inverse_lookup(
        self, key: Union[Hashable, List[Hashable], Tuple[Hashable]]
    ) -> Union[Any, List[Any]]:
        if isinstance(key, (list, tuple)):
            return tuple(self.inverse_table[i] for i in key)
        return self.inverse_table[key]

    def _do_inverse_lookup(self, key: Hashable) -> Any:
        try:
            return self.inverse_table[key]
        except KeyError:
            if self.inverse_oov is not None:
                return self.inverse_oov
            elif self.inverse_oov_key is not None:
                return self.inverse_table[self.inverse_oov_key]
            else:
                raise

    def size(self) -> int:
        return len(self.table)

    @classmethod
    def read_from_file(cls, data_file, kwargs: dict = {}):
        with open(data_file, "rt") as fd:
            paired_dict = json.load(fd)

            return cls(paired_dict, **kwargs)

    # alias for compatible
    load_from_file = read_from_file

    def write_to_file(self, data_file):
        with open(data_file, "wt") as fd:
            # set ensure_ascii=False for human readability of dumped file
            json.dump(self.table, fd, ensure_ascii=False)

    def dump_to_file(self, data_file):
        # alias for compatible
        return self.write_to_file(data_file)

    def get_config(self):
        return {
            "oov": self.oov,
            "oov_key": self.oov_key,
            "inverse_oov": self.inverse_oov,
            "inverse_oov_key": self.inverse_oov_key,
        }
