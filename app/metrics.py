from prometheus_client import Counter, Histogram, generate_latest
from fastapi import FastAPI, Request
from starlette.responses import Response

# Counters for request counts
REQUEST_COUNT = Counter('request_count', 'Request Count', ['endpoint', 'method', 'http_status'])

# Histograms for request latencies
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds', ['endpoint', 'method'])

def init_metrics(app: FastAPI):
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        method = request.method
        endpoint = request.url.path
        with REQUEST_LATENCY.labels(endpoint=endpoint, method=method).time():
            response = await call_next(request)
            status_code = response.status_code
            REQUEST_COUNT.labels(endpoint=endpoint, method=method, http_status=status_code).inc()
            return response

    @app.get("/metrics")
    async def metrics():
        return Response(content=generate_latest(), media_type="text/plain; version=0.0.4; charset=utf-8")

    return app