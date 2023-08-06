
# Aeros Documentation
Aeros is a package containing many wrappers for widely used Web and API functions.

```python
from Aeros import WebServer
from Aeros.misc import jsonify

app = WebServer(__name__)

app.route("/")
def home():
    return jsonify({"response":"ok"})

if __name__ == '__main__':
    app.start("-w 2") # worker threads (for more arguments see hypercorn documentation)
```


