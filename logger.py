import logging
import json
from datetime import datetime
from config import LOG_LEVEL, DEBUG

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
        }
        return json.dumps(log_data)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    
    if DEBUG:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    else:
        formatter = JSONFormatter()
    
    console_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    return logger

logger = get_logger(__name__)
