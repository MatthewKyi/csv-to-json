# CSV to JSON

---

Upload a CSV file to convert it to JSON. Choose how the data is structured (records, columns, index, split, or table). Optionally get pretty-printed output for readability.

## Features

---

- Convert CSV to JSON with a single upload
- Multiple output formats: `records`, `columns`, `index`, `split`, `table`
- Pretty-printed JSON by default (indent=2)
- Preserve column structure and types
- Simple file upload API for easy integration
- Health check endpoint

## API Usage

---

Send a `POST` request to the `/process` endpoint with a CSV file and optional query parameters.

Example with `curl`:

```bash
curl -X POST "http://localhost:5002/process?orient=records&pretty=true" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your.csv" \
  -o converted_your.json
```

### Endpoint

- `POST /process`

### Request

- **Body**: `multipart/form-data` containing:
  - `file`: CSV file to convert (must have `.csv` extension)
- **Query parameters** (all optional):
  - `orient` (default: `records`) — JSON structure: `records`, `columns`, `index`, `split`, or `table`
  - `pretty` (default: `true`) — Pretty-print JSON with indentation

### Response

- On success: JSON file returned as a download (`application/json`), filename `converted_<original_name>.json`.
- On error: JSON error message with an appropriate HTTP status code.

### Other

- `GET /` — Health check; returns `{"status": "CSV to JSON Converter API running"}`.
