import os
import socket
import ssl
import sys
from multiprocessing import Process

import click
from uvicorn.config import LOGGING_CONFIG, SSL_PROTOCOL_VERSION
from uvicorn.main import LEVEL_CHOICES

file_content = """
from pinferencia.frontend.app import Server

service = Server(backend_server="{scheme}://{backend_host}:{backend_port}")
"""


def start_frontend(file_content, main_script_path=None, **kwargs):
    import streamlit
    import streamlit.bootstrap as bootstrap
    from streamlit.credentials import check_credentials
    from streamlit.temporary_directory import TemporaryDirectory

    bootstrap.load_config_options(flag_options=kwargs)

    # use a customized frontend script if provided
    if main_script_path:
        bootstrap.run(main_script_path, "", "", flag_options=kwargs)
    else:
        # create a temporary file as the frontend script
        with TemporaryDirectory() as temp_dir:
            main_script_path = os.path.join(temp_dir, "proxy.py")
            with open(main_script_path, "w") as f:
                f.write(file_content)
            streamlit._is_running_with_streamlit = True

            check_credentials()

            bootstrap.run(main_script_path, "", "", flag_options=kwargs)


def start_backend(app, **kwargs):
    import uvicorn

    uvicorn.run(app, **kwargs)


def check_dependencies():
    try:
        import streamlit  # noqa
    except ImportError:
        sys.exit(
            "You need to install streamlit to start the frontend. "
            "To install streamlit, run: pip install streamlit"
        )
    try:
        import uvicorn  # noqa
    except ImportError:
        sys.exit(
            "You need to install uvicorn to start the backend. "
            "To install uvicorn, run: pip install uvicorn"
        )


def check_port_availability(
    backend_host: str,
    backend_port: int,
    frontend_host: str,
    frontend_port: int,
):
    if backend_port == frontend_port:
        raise Exception("Choose different ports for backend and frontend.")
    # check backend port
    backend_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    error = ""
    try:
        backend_sock.bind((backend_host, backend_port))
    except Exception:
        error += (
            f"Port {backend_port} is in use. Try another port with --backend-port.\n"
        )
    backend_sock.close()

    # check frontend port
    frontend_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        frontend_sock.bind((frontend_host, frontend_port))
    except Exception:
        error += (
            f"Port {frontend_port} is in use. Try another port with --frontend-port.\n"
        )
    frontend_sock.close()
    if error:
        sys.exit(error)


@click.command(context_settings={"auto_envvar_prefix": "PINFER"})
@click.argument("app")
@click.option(
    "--mode",
    type=str,
    default="all",
    help="Serving mode: all, frontend, or backend.",
    show_default=True,
)
@click.option(
    "--backend-host",
    type=str,
    default="127.0.0.1",
    help="Bind socket to this host.",
    show_default=True,
)
@click.option(
    "--backend-port",
    type=int,
    default=8000,
    help="Bind socket to this port.",
    show_default=True,
)
@click.option(
    "--backend-debug",
    is_flag=True,
    default=False,
    help="Enable debug mode.",
    hidden=True,
)
@click.option(
    "--backend-workers",
    default=None,
    type=int,
    help="Number of worker processes. Defaults to the $WEB_CONCURRENCY environment"
    " variable if available, or 1. Not valid with --reload.",
)
@click.option(
    "--backend-env-file",
    type=click.Path(exists=True),
    default=None,
    help="Environment configuration file.",
    show_default=True,
)
@click.option(
    "--backend-log-config",
    type=click.Path(exists=True),
    default=None,
    help="Logging configuration file. Supported formats: .ini, .json, .yaml.",
    show_default=True,
)
@click.option(
    "--backend-log-level",
    type=LEVEL_CHOICES,
    default=None,
    help="Log level. [default: info]",
    show_default=True,
)
@click.option(
    "--backend-root-path",
    type=str,
    default="",
    help="Set the ASGI 'root_path' for applications submounted below a given URL path.",
)
@click.option(
    "--backend-limit-concurrency",
    type=int,
    default=None,
    help="Maximum number of concurrent connections or tasks to allow, before issuing"
    " HTTP 503 responses.",
)
@click.option(
    "--backend-backlog",
    type=int,
    default=2048,
    help="Maximum number of connections to hold in backlog",
)
@click.option(
    "--backend-limit-max-requests",
    type=int,
    default=None,
    help="Maximum number of requests to service before terminating the process.",
)
@click.option(
    "--backend-timeout-keep-alive",
    type=int,
    default=5,
    help="Close Keep-Alive connections if no new data is received within this timeout.",
    show_default=True,
)
@click.option(
    "--ssl-keyfile",
    type=str,
    default=None,
    help="SSL key file",
    show_default=True,
)
@click.option(
    "--ssl-certfile",
    type=str,
    default=None,
    help="SSL certificate file",
    show_default=True,
)
@click.option(
    "--ssl-keyfile-password",
    type=str,
    default=None,
    help="SSL keyfile password",
    show_default=True,
)
@click.option(
    "--ssl-version",
    type=int,
    default=int(SSL_PROTOCOL_VERSION),
    help="SSL version to use (see stdlib ssl module's)",
    show_default=True,
)
@click.option(
    "--ssl-cert-reqs",
    type=int,
    default=int(ssl.CERT_NONE),
    help="Whether client certificate is required (see stdlib ssl module's)",
    show_default=True,
)
@click.option(
    "--ssl-ca-certs",
    type=str,
    default=None,
    help="CA certificates file",
    show_default=True,
)
@click.option(
    "--ssl-ciphers",
    type=str,
    default="TLSv1",
    help="Ciphers to use (see stdlib ssl module's)",
    show_default=True,
)
@click.option(
    "--backend-app-dir",
    default=".",
    show_default=True,
    help="Look for APP in the specified directory, by adding this to the PYTHONPATH."
    " Defaults to the current working directory.",
)
@click.option(
    "--frontend-base-url-path",
    default="",
    show_default=True,
    help="The base path for the URL where Streamlit should be served from.",
)
@click.option(
    "--frontend-port",
    default=8501,
    show_default=True,
    help="The port where the server will listen for browser connections.",
)
@click.option(
    "--frontend-host",
    default="127.0.0.1",
    show_default=True,
    help="The address where the server will listen for client and browser connections.",
)
@click.option(
    "--frontend-browser-server-address",
    default="localhost",
    show_default=True,
    help="Internet address where users should point their browsers in order to"
    " connect to the app. Can be IP address or DNS name and path.",
)
@click.option(
    "--frontend-script",
    default=None,
    show_default=True,
    help="Path to the customized frontend script.",
)
@click.option(
    "--reload",
    is_flag=True,
    default=False,
    show_default=True,
    help="Enable backend auto-reload.",
)
def main(
    app: str,
    mode: str,
    backend_host: str,
    backend_port: int,
    backend_debug: bool,
    backend_workers: int,
    backend_env_file: str,
    backend_log_config: str,
    backend_log_level: str,
    backend_root_path: str,
    backend_limit_concurrency: int,
    backend_backlog: int,
    backend_limit_max_requests: int,
    backend_timeout_keep_alive: int,
    ssl_keyfile: str,
    ssl_certfile: str,
    ssl_keyfile_password: str,
    ssl_version: int,
    ssl_cert_reqs: int,
    ssl_ca_certs: str,
    ssl_ciphers: str,
    backend_app_dir: str,
    frontend_base_url_path: str,
    frontend_port: int,
    frontend_host: str,
    frontend_browser_server_address: str,
    frontend_script: str,
    reload: bool,
) -> None:
    """Entrypoint

    Args:
        app (str): uvicorn flag
        model (str): all, backend or frontend
        backend_host (str): uvicorn flag: host
        backend_port (int): uvicorn flag: port
        backend_debug (bool): uvicorn flag: debug
        backend_reload (bool): uvicorn flag: reload
        backend_workers (int): uvicorn flag: workers
        backend_env_file (str): uvicorn flag: env_file
        backend_log_config (str): uvicorn flag: log_config
        backend_log_level (str): uvicorn flag: log_level
        backend_root_path (str): uvicorn flag: root_path
        backend_limit_concurrency (int): uvicorn flag: limit_concurrency
        backend_backlog (int): uvicorn flag: backlog
        backend_limit_max_requests (int): uvicorn flag: limit_max_requests
        backend_timeout_keep_alive (int): uvicorn flag: timeout_keep_alive
        ssl_keyfile (str): uvicorn flag: ssl_keyfile
        ssl_certfile (str): uvicorn flag: ssl_certfile
        ssl_keyfile_password (str): uvicorn flag: ssl_keyfile_password
        ssl_version (int): uvicorn flag: ssl_version
        ssl_cert_reqs (int): uvicorn flag: ssl_cert_reqs
        ssl_ca_certs (str): uvicorn flag: ssl_ca_certs
        ssl_ciphers (str): uvicorn flag: ssl_ciphers
        backend_app_dir (str): uvicorn flag: app_dir
        frontend_base_url_path (str): streamlit flag: server.baseUrlPath
        frontend_port (int): streamlit flag: server.port
        frontend_host (str): streamlit flag: server.address
        frontend_browser_server_address (str): streamlit flag: browser.serverAddress
        frontend_script (str): streamlit flag: main_script_path
        reload (bool): uvicorn flag: reload
    """
    # flags of uvicorn
    backend_kwargs = {
        "host": backend_host,
        "port": backend_port,
        "env_file": backend_env_file,
        "log_config": LOGGING_CONFIG
        if backend_log_config is None
        else backend_log_config,
        "log_level": backend_log_level,
        "debug": backend_debug,
        "workers": backend_workers,
        "root_path": backend_root_path,
        "limit_concurrency": backend_limit_concurrency,
        "backlog": backend_backlog,
        "limit_max_requests": backend_limit_max_requests,
        "timeout_keep_alive": backend_timeout_keep_alive,
        "ssl_keyfile": ssl_keyfile,
        "ssl_certfile": ssl_certfile,
        "ssl_keyfile_password": ssl_keyfile_password,
        "ssl_version": ssl_version,
        "ssl_cert_reqs": ssl_cert_reqs,
        "ssl_ca_certs": ssl_ca_certs,
        "ssl_ciphers": ssl_ciphers,
        "app_dir": backend_app_dir,
        "reload": reload,
    }

    # flags of streamlit
    frontend_kwargs = {
        "server.baseUrlPath": frontend_base_url_path,
        "server.port": frontend_port,
        "server.address": frontend_host,
        "browser.serverAddress": frontend_browser_server_address,
    }
    check_dependencies()
    check_port_availability(
        backend_host=backend_host,
        backend_port=backend_port,
        frontend_host=frontend_host,
        frontend_port=frontend_port,
    )
    if mode not in ["all", "backend", "frontend"]:
        sys.exit(f"Invalid mode {mode}.")

    if mode == "backend":
        start_backend(app, **backend_kwargs)
    else:
        if mode == "all":
            # start backend
            p = Process(target=start_backend, args=[app], kwargs=backend_kwargs)
            p.start()

        # start frontend
        # TODO: if the mode is only frontend, how to set https scheme?
        if ssl_keyfile and ssl_certfile:
            http_scheme = "https"
        else:
            http_scheme = "http"
        start_frontend(
            file_content.format(
                scheme=http_scheme,
                backend_host=backend_host,
                backend_port=backend_port,
            ),
            main_script_path=frontend_script,
            **frontend_kwargs,
        )


if __name__ == "__main__":
    main()  # pragma: no cover
