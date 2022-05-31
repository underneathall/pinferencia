import paddlehub as hub

from pinferencia import Server, task

lexical_analysis = hub.Module(name="jieba_paddle")


def predict(text: str):
    return lexical_analysis.cut(text, cut_all=False, HMM=True)


service = Server()
service.register(
    model_name="lexical_analysis", model=predict, metadata={"task": task.TEXT_TO_TEXT}
)
