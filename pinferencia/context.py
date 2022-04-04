class PredictContext:
    """Prediction Context
    Attributes:
        scheme(str): "kservev2"
        request_data(dict): request json data
    """

    scheme = None
    request_data = None

    def __init__(self, scheme, request_data):
        super().__init__()
        self.scheme = scheme
        self.request_data = request_data
