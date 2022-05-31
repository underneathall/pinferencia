import paddlehub as hub

from pinferencia import Server, task

emotion_detection_textcnn = hub.Module(name="emotion_detection_textcnn")


def predict(text: list) -> list:
    return emotion_detection_textcnn.emotion_classify(texts=text)


service = Server()
service.register(
    model_name="emotion_detection_textcnn",
    model=predict,
    metadata={"task": task.TEXT_TO_TEXT},
)
