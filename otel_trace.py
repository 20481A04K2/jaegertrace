# otel_trace.py
import subprocess
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

# Use your VM's IP or DNS name
JAEGER_VM_HOST = "35.234.11.8"  # Replace with real IP

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name=JAEGER_VM_HOST,
    agent_port=6831,
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

def traced(name, command):
    with tracer.start_as_current_span(name):
        print(f"Running step: {name}")
        subprocess.run(command, shell=True, check=True)

traced("build", "echo building app...")         # Replace with real build commands
traced("test", "echo running tests...")         # Replace with real tests
traced("deploy", "echo deploying...")           # Replace with gcloud deploy commands
