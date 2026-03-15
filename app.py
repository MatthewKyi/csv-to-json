import os
from io import BytesIO

import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_ORIENT = frozenset({"records", "columns", "index", "split", "table"})

MAX_ROWS = 500_000


def _get_bool_param(name: str, default: bool = True) -> bool:
    """Parse optional boolean query parameter. Default True for 'pretty'."""
    raw = request.args.get(name, "").strip().lower()
    if not raw:
        return default
    return raw in ("1", "true", "yes", "on")


def _get_orient_param() -> str:
    """Parse and validate 'orient' query parameter. Default 'records'."""
    raw = request.args.get("orient", "records").strip().lower()
    if raw not in ALLOWED_ORIENT:
        return "records"
    return raw


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "CSV to JSON Converter API running"})


@app.route("/process", methods=["POST"])
def process():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if not file or not file.filename or file.filename.strip() == "":
        return jsonify({"error": "Filename is empty"}), 400

    base, ext = os.path.splitext(file.filename)
    if ext.lower() != ".csv":
        return jsonify({"error": "File is not .csv"}), 400

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": f"CSV parsing failed: {str(e)}"}), 400

    row_count = len(df)
    if row_count > MAX_ROWS:
        return jsonify({"error": "CSV too large"}), 400

    pretty = _get_bool_param("pretty", default=True)
    orient = _get_orient_param()

    if pretty:
        json_str = df.to_json(orient=orient, indent=2)
    else:
        json_str = df.to_json(orient=orient)

    print(f"Rows: {row_count} | orient: {orient} | pretty: {pretty}")

    buffer = BytesIO(json_str.encode("utf-8"))
    base_name = os.path.splitext(file.filename)[0]
    download_name = f"converted_{base_name}.json"

    return send_file(
        buffer,
        mimetype="application/json",
        as_attachment=True,
        download_name=download_name,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5002)))
