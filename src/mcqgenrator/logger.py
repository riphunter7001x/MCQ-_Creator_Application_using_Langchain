import logging 
import os
from datetime import datetime

# Create a new file for logging
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Directory to save our log
log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)

LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILEPATH,
    format='%(asctime)s %(levelname)s %(message)s'
)
