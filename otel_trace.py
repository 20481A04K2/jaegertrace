import subprocess
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Your Jaeger VM public IP and port
OTLP_JAEGER_ENDPOINT = "35.234.11.8"

# Set up tracer and OTLP exporter
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(
    endpoint=OTLP_JAEGER_ENDPOINT,
    insecure=True  # Don't use TLS
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Wrap commands in spans
def traced(name, command):
    with tracer.start_as_current_span(name):
        print(f"🔹 Running step: {name}")
        subprocess.run(command, shell=True, check=True)

print("🚀 Starting traced pipeline to Jaeger via OTLP gRPC...")
traced("build", "echo building app...")
traced("test", "echo running tests...")
traced("deploy", "echo deploying app...")
print("✅ Traces sent to Jaeger OTLP endpoint:", OTLP_JAEGER_ENDPOINT)
