from pathlib import Path

from box import box_from_file



cwd = Path(__file__).parent
CONFIG = box_from_file(f"{cwd}/config.yml")
CONFIG.polyglot.models.base_directory = f"{cwd.parent}/{CONFIG.polyglot.models.base_directory}"
