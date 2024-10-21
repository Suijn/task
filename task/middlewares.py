import uuid

import structlog

logger = structlog.get_logger()


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If X-Request-ID doesn't exist, generate one.
        correlation_id = request.META.get("X-Correlation-ID")
        if not correlation_id:
            correlation_id = uuid.uuid4()

        # Inject request_id in the log context.
        structlog.contextvars.bind_contextvars(correlation_id=str(correlation_id))

        response = self.get_response(request)
        return response
