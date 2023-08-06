# gevent-ws

A fast, MIT-licensed alternative to the abandoned non-free (as in freedom) [gevent-websocket](https://gitlab.com/noppo/gevent-websocket).


## Why?

It's MIT-licensed, so it can be included to almost all software (both open-source and closed-source) without any licensing issues, as opposed to *gevent-websocket*. And it's several times faster!


## Installation

*gevent-ws* can be installed from PyPI and GitHub.


### PyPI

```shell
$ pip3 install gevent-ws
```


### GitHub

```shell
$ git clone https://github.com/imachug/gevent-ws.git
$ cd gevent-ws
$ python3 setup.py install
```


## Example

### A simple echo server

```python3
from gevent.pywsgi import WSGIServer
from gevent_ws import WebSocketHandler


def app(env, start_response):
    ws = env["wsgi.websocket"]
    while True:
        msg = ws.receive()
        if msg is None:
            break
        ws.send(msg)
    return [b"Bye"]


server = WSGIServer(("", 8080), app, handler_class=WebSocketHandler)
server.serve_forever()
```


### Both HTTP and websocket on a single port

```python3
from gevent.pywsgi import WSGIServer
from gevent_ws import WebSocketHandler


def app(env, start_response):
    if "wsgi.websocket" in env:
        ws = env["wsgi.websocket"]
        while True:
            msg = ws.receive()
            if msg is None:
                break
            ws.send(msg)
        return [b"Bye"]
    else:
        start_response("200 OK", [
            ("Content-Type", "text/html, charset=utf-8")
        ])

        return [
            b"""
                <script>
                    const ws = new WebSocket("ws://127.0.0.1:8080/");
                    ws.onopen = () => {
                        ws.send("Hello, world!");
                    };
                    ws.onmessage = e => {
                        ws.send(e.data);
                    };
                </script>
            """
        ]


server = WSGIServer(("", 8080), app, handler_class=WebSocketHandler)
server.serve_forever()
```


## Docs

### `gevent_ws.WebSocketHandler`

The main class. Pass it to `gevent.pywsgi.WSGIServer` as `handler_class`.


### `gevent_ws.WebSocket`

You get this object by accessing `wsgi.websocket` property of the environment object. If it exists, it's a websocket connection; if it doesn't, it's an HTTP request. You can use `"wsgi.websocket" in env` to check this and route the request correctly.


### `gevent_ws.WebSocket.receive()`

Waits for a message and returns it, either as `str` or `bytes`. Blocks. May return `None` if the connection is closed or an `OSError` if the socket can't be read from.


### `gevent_ws.WebSocket.receive_nowait()`

Returns the message if it's available (the format is the same as in `receive()`) or `None` if no message is in the queue. May return `None` or raise `OSError` (see `receive()`).


### `gevent_ws.WebSocket.send(message)`

Sends a message to the other party. `message` can be either `str` or `bytes`. May raise `EOFError` if the connection is closed or `OSError` if the message can't be sent for some other reason.


### `gevent_ws.WebSocket.close(status=1000)`

Closes the websocket. Status `1000` (the default one) means that the connection is closed cleanly. Check [RFC](https://tools.ietf.org/html/rfc6455#section-7.4) for more status codes.


### `gevent_ws.WebSocket.set_max_message_length(length)`

Set maximum incoming message size (in bytes). 10 MiB is the default value.


### `gevent_ws.WebSocket.closed`

A boolean showing whether the connection is closed (by any of the two parties) or is being closed.


### `gevent_ws.WebSocket.status`

The close status code sent by the other party. `None` if the socket was closed by the client, the server didn't return the error code or the connection was aborted abnormally.
