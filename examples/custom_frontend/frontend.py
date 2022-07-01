from pinferencia.frontend.app import Server

detail_description = """
# My Awesome Model

This is the service of my awesome model.

It is **fast**, **simple**, and **beautiful**.

Visit [My Awesome Model Home](/abc) to learn more about it.
"""

service = Server(
    title="My Awesome Model",
    short_description="This is the short description",
    detail_description=detail_description,
    backend_server="http://127.0.0.1:8000",
)
