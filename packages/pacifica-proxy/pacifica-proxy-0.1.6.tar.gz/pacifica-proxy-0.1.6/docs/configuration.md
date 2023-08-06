# Configuration

The Pacifica Core services require two configuration files. The REST
API utilizes [CherryPy](https://github.com/cherrypy) and review of
their
[configuration documentation](http://docs.cherrypy.org/en/latest/config.html)
is recommended. The service configuration file is a INI formatted
file containing configuration for database connections.

## CherryPy Configuration File

An example of Proxy server CherryPy configuration:

```ini
[global]
log.screen: True
log.access_file: 'access.log'
log.error_file: 'error.log'
server.socket_host: '0.0.0.0'
server.socket_port: 8051

[/]
request.dispatch: cherrypy.dispatch.MethodDispatcher()
tools.response_headers.on: True
tools.response_headers.headers: [('Content-Type', 'application/json')]
```

## Service Configuration File

The service configuration is an INI file and an example is as follows:

```ini
[database]
; This section contains database connection configuration

; peewee_url is defined as the URL PeeWee can consume.
; http://docs.peewee-orm.com/en/latest/peewee/database.html#connecting-using-a-database-url
peewee_url = sqliteext:///db.sqlite3

; connect_attempts are the number of times the service will attempt to
; connect to the database if unavailable.
connect_attempts = 10

; connect_wait are the number of seconds the service will wait between
; connection attempts until a successful connection to the database.
connect_wait = 20
```

## Starting the Service

Starting the Proxy service can be done by two methods. However,
understanding the requirements and how they apply to REST services
is important to address as well. Using the
internal CherryPy server to start the service is recommended for
Windows platforms. For Linux/Mac platforms it is recommended to
deploy the service with
[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

### Deployment Considerations

The Proxy service utilizes both connectivity to the Metadata service
and the Archive Interface. As a result close connectivity to those
services is a must.

### CherryPy Server

To make running the Proxy service using the CherryPy's builtin
server easier we have a command line entry point.

```
$ pacifica-proxy --help
usage: pacifica-proxy [-h] [-c CONFIG] [-p PORT] [-a ADDRESS]

Run the proxy server.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        cherrypy config file
  -p PORT, --port PORT  port to listen on
  -a ADDRESS, --address ADDRESS
                        address to listen on
$ pacifica-proxy
[09/Jan/2019:09:17:26] ENGINE Listening for SIGTERM.
[09/Jan/2019:09:17:26] ENGINE Bus STARTING
[09/Jan/2019:09:17:26] ENGINE Set handler for console events.
[09/Jan/2019:09:17:26] ENGINE Started monitor thread 'Autoreloader'.
[09/Jan/2019:09:17:26] ENGINE Serving on http://0.0.0.0:8180
[09/Jan/2019:09:17:26] ENGINE Bus STARTED
```

### uWSGI Server

To make running the Proxy service using uWSGI easier we have a
module to be included as part of the uWSGI configuration. uWSGI is
very configurable and can use this module many different ways. Please
consult the
[uWSGI Configuration](https://uwsgi-docs.readthedocs.io/en/latest/Configuration.html)
documentation for more complicated deployments.

```
$ pip install uwsgi
$ uwsgi --http-socket :8180 --master --module pacifica.proxy.wsgi
```

### NGINX Acceleration

The Proxy service supports
[NGINX Acceleration](https://www.nginx.com/resources/wiki/start/topics/examples/x-accel/),
an example
[NGINX Configuration](https://raw.githubusercontent.com/pacifica/pacifica-proxy/master/travis/nginx.conf.in)
is used in the Travis CI pipeline. The setup is to have the Proxy
service tell NGINX to redirect the request to the Archiveinterface
internally. This configuration bypasses transferring the data through
the Proxy service. This configuration requires the Archiveinterface
and Proxy services to be accessible through the same border NGINX
endpoint exposed to users.
