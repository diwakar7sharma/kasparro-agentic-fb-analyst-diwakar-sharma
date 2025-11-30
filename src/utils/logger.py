import logging
import os
from datetime import datetime

def setup_logger(name="kasparro_logger"):
    # 1. Create logs directory if it doesn't exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # 2. Define filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"trace_{timestamp}.log")

    # 3. Configure Logging
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding handlers multiple times if function is called often
    if not logger.handlers:
        # File Handler (Writes to logs/trace_DATE.log)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        formatter = logging.Formatter(
            '\n%(asctime)s [%(levelname)s] ----------------------\n%(message)s\n'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger