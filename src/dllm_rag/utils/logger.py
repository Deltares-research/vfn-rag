import sys
import logging


class Logger:
    def __init__(self, name: str, level: int = logging.INFO, file_name: str = None):
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filename=file_name if file_name is not None else "dllm-rag.log",
        )
        self.logger = logging.getLogger(name)
        self.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
