from waitress import serve
from app import app

if __name__ == "__main__":
    print("Starting production server on http://127.0.0.1:8080")
    serve(app, host='0.0.0.0', port=8080, threads=4)
