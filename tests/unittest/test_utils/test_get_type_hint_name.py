import sys
import typing

import pytest

from pinferencia.utils import get_type_hint_name


@pytest.mark.parametrize(
    "type_hint_and_name",
    [
        (typing.List, "typing.List"),
        (typing.Dict, "typing.Dict"),
        (typing.Tuple, "typing.Tuple"),
        (typing.List[str], "typing.List[str]"),
        (typing.List[int], "typing.List[int]"),
        (typing.List[float], "typing.List[float]"),
        (typing.List[bool], "typing.List[bool]"),
        (str, "str"),
        (int, "int"),
        (float, "float"),
        (bool, "bool"),
        (list, "list"),
        (dict, "dict"),
        (tuple, "tuple"),
    ],
)
@pytest.mark.parametrize("has_ipython", [True, False])
def test(type_hint_and_name, has_ipython, monkeypatch):
    if not has_ipython:
        monkeypatch.setitem(sys.modules, "IPython.lib.pretty", None)
    type_hint, type_hint_name = type_hint_and_name
    assert get_type_hint_name(type_hint) == type_hint_name
