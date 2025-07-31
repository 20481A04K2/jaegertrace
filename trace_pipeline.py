from otel_config import configure_tracer
from opentelemetry import trace
import time

configure_tracer()
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("build-pipeline"):
    with tracer.start_as_current_span("clone-source"):
        time.sleep(2)

    with tracer.start_as_current_span("run-tests"):
        time.sleep(3)

    with tracer.start_as_current_span("build-image"):
        time.sleep(1)

    with tracer.start_as_current_span("deploy"):
        time.sleep(2)
