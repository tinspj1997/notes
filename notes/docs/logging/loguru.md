# Loguru logging

This page documents a small Loguru-based logging setup that configures
console output and rotating file logs. It also patches log records to include
the caller's class name (when applicable).

```python
import sys
from loguru import logger
from pathlib import Path
import inspect

def _add_class_name(record):
    """Patch logger records to include the caller's class name."""
    frame = inspect.currentframe()
    # Walk up the stack to find the actual caller (outside loguru internals)
    while frame:
        frame = frame.f_back
        if frame and frame.f_globals.get("__name__") not in ("loguru._logger", __name__):
            cls = frame.f_locals.get("self") or frame.f_locals.get("cls")
            record["extra"]["classname"] = type(cls).__name__ if cls else ""
            break
    else:
        record["extra"]["classname"] = ""


def setup_logging(log_path="logs") -> None:
    """Quick Loguru setup: Console + rotating files."""
    log_path = str(log_path) or "logs"
    Path(log_path).mkdir(exist_ok=True)

    logger.configure(patcher=_add_class_name)

    # Console logger configuration
    console_kwargs = {
        "level": "INFO",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{extra[classname]}:{function}:{line} | {message} | Context : {extra} ",
    }

    # File logger configuration
    file_kwargs = {
        "rotation": "1 day",
        "retention": "7 days",
        "level": "INFO",
        "compression": "zip",
        "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{extra[classname]}:{function}:{line} | {message} | Context : {extra}",
    }

    logger.remove()  # Remove default logger

    # Add console logger
    logger.add(sys.stderr, **console_kwargs)

    # Add file loggers
    logger.add(
        "logs/application_log_{time:YYYY-MM-DD}.log",
        filter=lambda record: record["extra"].get("type", "app") == "app",
        **file_kwargs,
    )

    logger.add(
        "logs/metering_log_{time:YYYY-MM-DD}.log",
        filter=lambda record: record["extra"].get("type") == "meter",
        **file_kwargs,
    )

```

Usage
-----
Call `setup_logging()` early in your application start-up. Example:

```python
from loguru import setup_logging

setup_logging()
logger.info("Logging started")
```
