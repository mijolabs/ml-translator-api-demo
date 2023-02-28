from pathlib import Path

from box import box_from_file

CONFIG = box_from_file(f"{Path(__file__).parent}/config.yml")
