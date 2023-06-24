import logging
from pathlib import Path

from box import box_from_file



class AccessLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] not in CONFIG.api.no_access_log

logging.getLogger("uvicorn.access").addFilter(AccessLogFilter())

cwd = Path(__file__).parent

CONFIG = box_from_file(f"{cwd}/config.yml")
CONFIG.translator.models.base_directory = f"{cwd.parent}/{CONFIG.translator.models.base_directory}"
