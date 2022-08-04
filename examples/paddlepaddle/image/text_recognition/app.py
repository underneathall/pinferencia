from pinferencia import Server

import paddlehub as hub
import cv2

ocr = hub.Module(
    name="chinese_ocr_db_crnn_mobile", enable_mkldnn=True
)  # mkldnn acceleration only works under CPU


def predict(path: str):
    return ocr.recognize_text(
        images=[cv2.imread(path)], visualization=True, output_dir="./"
    )


service = Server()
service.register(model_name="ocr", model=predict)
