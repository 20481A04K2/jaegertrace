import subprocess
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

logging.basicConfig(level=logging.DEBUG)

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
        print(f"🔹 Running step: {name}")
        subprocess.run(command, shell=True, check=True)

print("🚀 Starting traced pipeline...")
traced("build", "echo building app...")
traced("test", "echo running tests...")
traced("deploy", "echo deploying app...")
print("✅ Traces should be sent to Jaeger at", JAEGER_VM_HOST)
