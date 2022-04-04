import copy

import pytest

from pinferencia.apis.kserve.v2.models import Request
from pinferencia.apis.kserve.v2.parsers import InputParser, OutputParser


def test_input_parser_single_inputs():
    request = Request(
        inputs=[
            {"name": "a", "data": "a"},
        ]
    )
    parser = InputParser(request)
    assert parser.data == "a"


def test_input_parser_multiple_inputs():
    request = Request(
        inputs=[
            {"name": "a", "data": "a"},
            {"name": "b", "data": "b"},
        ]
    )
    parser = InputParser(request)
    assert parser.data == {"a": "a", "b": "b"}


def test_output_parser_list_data_without_schema():
    data = [1, 2]
    parser = OutputParser(raw_data=data)
    assert parser.data == [
        {"name": "default", "shape": [2], "data": [1, 2], "datatype": "int64"}
    ]


def test_output_parser_dict_data_without_schema():
    data = {"test": 1}
    parser = OutputParser(raw_data=data)
    assert parser.data == [
        {"name": "test", "shape": -1, "data": 1, "datatype": "int64"}
    ]


def test_output_parser_dict_data_with_schema():
    schema = [
        {"name": "a", "data": 1, "datatype": "int64"},
        {"name": "b", "data": 1, "datatype": "int64"},
    ]
    data = {"test": 1, "a": 2, "b": 3}
    parser = OutputParser(raw_data=copy.deepcopy(data), schema=schema)
    for d in parser.data:
        assert data[d["name"]] == d["data"]
        assert d["shape"] == -1
        assert d["datatype"] == "int64"


def test_output_parser_dict_data_with_incomplete_schema():
    schema = [
        {"name": "a", "data": 1, "datatype": "int64"},
        {"data": 1, "datatype": "int64"},
    ]
    data = {"test": 1, "a": 2, "b": 3}
    parser = OutputParser(raw_data=copy.deepcopy(data), schema=schema)
    for d in parser.data:
        assert data[d["name"]] == d["data"]
        assert d["shape"] == -1
        assert d["datatype"] == "int64"


def test_output_parser_list_data_with_schema():
    schema = [
        {"name": "test", "data": 1, "datatype": "int64"},
    ]
    data = [1, 2]
    parser = OutputParser(raw_data=data, schema=schema)
    assert parser.data == [
        {"name": "test", "shape": [2], "data": [1, 2], "datatype": "int64"}
    ]


def test_output_parser_error_list_data_with_schema():
    schema = [
        {"name": "a", "data": 1, "datatype": "int64"},
        {"name": "b", "data": 1, "datatype": "int64"},
    ]
    data = [1, 2]
    parser = OutputParser(raw_data=data, schema=schema)
    with pytest.raises(ValueError) as exc:
        parser.data
    assert "Multiple outputs defined, prediction must be a dict." in str(
        exc.value
    )
