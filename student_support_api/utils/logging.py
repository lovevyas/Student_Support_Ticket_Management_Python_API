import logging

logging.basicConfig(
    level= logging.INFO,
    formate = "%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
