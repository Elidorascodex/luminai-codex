"""
TEC TGCR CLI Interface with Tracing
"""

import typer
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Initialize tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4317",
    insecure=True,
)

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = typer.Typer()

@app.command()
def chat():
    """Start chat interface"""
    with tracer.start_as_span("chat_command"):
        typer.echo("Chat interface not implemented yet")

@app.command()
def evaluate():
    """Run resonance evaluation"""
    with tracer.start_as_span("evaluate_command"):
        from ..evaluation import Evaluator
        evaluator = Evaluator()
        # Placeholder session data
        evaluator.add_session_data({"id": "test", "integrated_info": 1.2, "temporal_patterns": 0.8, "resonance_strength": 0.9})
        result = evaluator.run_evaluation()
        typer.echo(f"Evaluation result: {result}")

if __name__ == "__main__":
    app()
