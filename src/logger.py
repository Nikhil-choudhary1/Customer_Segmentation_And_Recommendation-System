import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
LOG_PATH = os.path.join("logs", LOG_FILE)

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    level=logging.INFO
)