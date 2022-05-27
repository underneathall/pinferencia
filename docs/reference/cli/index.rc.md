# 命令行界面

**Pinfenrecia** 提供命令 `pinfer` 来简化启动前端和后端服务。

您可以使用 `pinfer --help` 查看可用选项：

```bash
Usage: pinfer [OPTIONS] APP

  Pinferencia Start backend server and/or frontend server.

  Argument APP:

      If mode is all or backend, app should be the backend uvicorn app.

      If mode is frontend, app should be the backend address

Options:
  --mode TEXT                     Serving mode: all, frontend, or backend.
                                  [default: all]
  --backend-host TEXT             Bind socket to this host.  [default:
                                  127.0.0.1]
  --backend-port INTEGER          Bind socket to this port.  [default: 8000]
  --backend-workers INTEGER       Number of worker processes. Defaults to the
                                  $WEB_CONCURRENCY environment variable if
                                  available, or 1. Not valid with --reload.
  --backend-env-file PATH         Environment configuration file.
  --backend-log-config PATH       Logging configuration file. Supported
                                  formats: .ini, .json, .yaml.
  --backend-log-level [critical|error|warning|info|debug|trace]
                                  Log level. [default: info]
  --backend-root-path TEXT        Set the ASGI 'root_path' for applications
                                  submounted below a given URL path.
  --backend-limit-concurrency INTEGER
                                  Maximum number of concurrent connections or
                                  tasks to allow, before issuing HTTP 503
                                  responses.
  --backend-backlog INTEGER       Maximum number of connections to hold in
                                  backlog
  --backend-limit-max-requests INTEGER
                                  Maximum number of requests to service before
                                  terminating the process.
  --backend-timeout-keep-alive INTEGER
                                  Close Keep-Alive connections if no new data
                                  is received within this timeout.  [default:
                                  5]
  --ssl-keyfile TEXT              SSL key file
  --ssl-certfile TEXT             SSL certificate file
  --ssl-keyfile-password TEXT     SSL keyfile password
  --ssl-version INTEGER           SSL version to use (see stdlib ssl module's)
                                  [default: 17]
  --ssl-cert-reqs INTEGER         Whether client certificate is required (see
                                  stdlib ssl module's)  [default: 0]
  --ssl-ca-certs TEXT             CA certificates file
  --ssl-ciphers TEXT              Ciphers to use (see stdlib ssl module's)
                                  [default: TLSv1]
  --backend-app-dir TEXT          Look for APP in the specified directory, by
                                  adding this to the PYTHONPATH. Defaults to
                                  the current working directory.  [default: .]
  --frontend-base-url-path TEXT   The base path for the URL where Streamlit
                                  should be served from.
  --frontend-port INTEGER         The port where the server will listen for
                                  browser connections.  [default: 8501]
  --frontend-host TEXT            The address where the server will listen for
                                  client and browser connections.  [default:
                                  127.0.0.1]
  --frontend-browser-server-address TEXT
                                  Internet address where users should point
                                  their browsers in order to connect to the
                                  app. Can be IP address or DNS name and path.
                                  [default: localhost]
  --frontend-script TEXT          Path to the customized frontend script.
  --reload                        Enable backend auto-reload.  [default:
                                  False]
  --help                          Show this message and exit.
```
