import logging

from scan import settings

logger = logging.Logger("scan", level=logging.DEBUG)
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(
    settings.BASE_PATH.parent.parent / "logs" / "scan.log"
)
