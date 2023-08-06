## Soc - A Python websocket micro-framework

> Work in progress

```py3
from soc import Soc, jsonify


def create_app() -> Soc:

    app: Soc = Soc()

    @app.route("/foo")
    def foo(request):
        return jsonify({"hello": "world"})

    return app


if __name__ == "__main__":
    app: Soc = create_app()
    app.run(host="localhost", port=8765)
```