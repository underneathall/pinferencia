import pandas as pd


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
    elif isinstance(prediction, str):
        component.info(prediction)
        return
    component.json(prediction)
