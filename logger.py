import logging
from rich.logging import RichHandler
from rich.console import Console

def setup_logger():
    logger = logging.getLogger()
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # RichHandler for colorful console output
        console_handler = RichHandler(markup=False, console=Console(force_terminal=True))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

