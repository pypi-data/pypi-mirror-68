
# Aeros Documentation
Aeros is a package containing wrappers for widely used Web and API functions.
The whole package is based on Quart/Flask.

```python
from Aeros import WebServer
from Aeros.misc import jsonify

app = WebServer(__name__, host="0.0.0.0", port=80)


@app.route("/")
async def home():
    return jsonify({"response": "ok"})


if __name__ == '__main__':
    app.start("-w 2")  # worker threads (for more arguments see hypercorn documentation)
```
