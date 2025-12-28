import uuid

from opentelemetry import trace

TRACEID_MASK = 0xFFFFFFFFFFFFFFFF


def generate() -> str:
    return str(uuid.uuid4())


def get_trace_id() -> str:
    # return hex(trace.get_current_span().get_span_context().trace_id)[2:].zfill(32)
    return trace.format_trace_id(trace.get_current_span().get_span_context().trace_id)
