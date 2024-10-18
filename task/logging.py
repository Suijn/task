import structlog
from django.conf import settings


def setup_logging():
    common_processors = [
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]
    specific_processors = []
    if settings.WORKING_MODE == "dev":
        specific_processors.extend(
            [structlog.dev.set_exc_info, structlog.dev.ConsoleRenderer()]
        )
    else:
        specific_processors.extend([structlog.processors.JSONRenderer()])

    structlog.configure(
        processors=[structlog.contextvars.merge_contextvars]
        + common_processors
        + specific_processors,
    )
