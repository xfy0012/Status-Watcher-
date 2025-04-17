from app import create_app
from prometheus_client import start_http_server

app = create_app()

if __name__ == '__main__':
    start_http_server(8002)
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
