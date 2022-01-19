import os
from flask import Flask, request, Response
from werkzeug.exceptions import BadRequest
from get_param import get_param

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.post("/perform_query")
def perform_query() -> Response:
    try:
        query_param = request.args["query_param"]
        file_name = request.args["file_name"]
    except KeyError:
        raise BadRequest

    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return Response(f"{file_name} was not found")

    with open(file_path, encoding='utf-8') as f:
        result = '\n'.join(get_param(f, str(query_param)))
    return app.response_class(result, content_type="text/plain")


if __name__ == '__main__':
     app.run(debug=True)