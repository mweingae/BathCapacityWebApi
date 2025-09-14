import logging
import sys
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

def setup_logging(
    log_level: str = "INFO",
    log_file: str = "app.log"
):
    """
    Set up application logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
    """
    
    # Create logs directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger("app")
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # File handler with rotation
    file_handler = TimedRotatingFileHandler(
        log_file,
        when="D",
        backupCount=7
    )
    file_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Set formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')
    
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return root_logger