import sys
import typing

import pandas as pd
from pydantic import BaseModel


def display_text_prediction(prediction: object, component):
    if isinstance(prediction, list) and prediction:
        if isinstance(prediction[0], dict):
            try:
                hide_table_row_index = """
                    <style>
                    tbody th {display:none}
                    .blank {display:none}
                    </style>
                """
                component.markdown(hide_table_row_index, unsafe_allow_html=True)
                df = pd.DataFrame(prediction)
                component.table(df)
                return
            except Exception:
                pass
    elif isinstance(prediction, (str, int, float, bool)):
        component.info(prediction)
        return
    component.json(prediction)


def is_list_type(type_hint_str: str):
    return type_hint_str.startswith("list") or type_hint_str.startswith("typing.List")


def format_data_with_type_hint_str(data: object, type_hint_str: str) -> object:
    if hasattr(typing, "ForwardRef"):
        # Python 3.7 and above
        forward_ref = typing.ForwardRef(type_hint_str)  # pragma: no cover
    else:
        # Python 3.6
        forward_ref = typing._ForwardRef(type_hint_str)  # pragma: no cover
    data_type = typing._eval_type(forward_ref, sys.modules, None)

    class DataModel(BaseModel):
        data: data_type

    return DataModel(data=data).dict()["data"]
