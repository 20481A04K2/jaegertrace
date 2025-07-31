import os
import uvicorn
from fastapi import FastAPI
from otel_config import configure_tracer

app = FastAPI()
configure_tracer()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI with Jaeger Tracing"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Read the PORT from environment
    uvicorn.run(app, host="0.0.0.0", port=port)
