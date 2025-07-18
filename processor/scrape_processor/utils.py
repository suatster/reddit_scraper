from datetime import datetime, timezone
import logging

from . import config

def utc_to_str(utc_timestamp):
    """Convert UTC timestamp to formatted string."""
    dt = datetime.fromtimestamp(utc_timestamp, tz=timezone.utc)
    return dt.strftime('%d-%m-%Y %H:%M:%S')

def construct_mongo_uri():
    if not config.mongo_host or not config.mongo_username or not config.mongo_password or not config.mongo_port:
        logging.error("MongoDB connection parameters are not set in environment variables.")
        raise ValueError("MongoDB connection parameters are not set.")
    return f"mongodb://{config.mongo_username}:{config.mongo_password}@{config.mongo_host}:{config.mongo_port}/"