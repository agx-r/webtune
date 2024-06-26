# config_updater.py
from dbcontroller import DatabaseConnector
from logger import setup_logger
import json

config_file = "/external/config.json"
logger = setup_logger()

def load_config():
    """
    Load configuration from config.json file.
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        logger.debug(config)
    except FileNotFoundError:
        config = {
            "stream_url": "https://rdi-cast.uz/listen/restaurant/promo",
            "preview_url": "https://rdi-cast.uz/public/promo",
            "db_host": "176.96.243.38",
            "db_user": "webtune",
            "db_password": "webtune@2024",
            "client_id": "promo",
            "device_id": "restaurant",
            "password": "webtune",
            "db_name": "stream_linker"
        }
        
        with open('/external/config.json', 'w') as f:
            json.dump(config, f, indent=4)
        
        logger.info("Creating config file.")
    return config

def replace_duplicates(original_object, mask_object):
    result = original_object.copy()

    for key, value in mask_object.items():
        if key in result:
            result[key] = value

    return result

def upload_config(config_object):
    original_config = load_config()
    
    updated_config = replace_duplicates(original_config, config_object)

    with open(config_file, 'w') as f:
        json.dump(updated_config, f)

def update_by_database(controller=None):
    logger.info("Updating by DB")
    config = load_config()
    maria_client = DatabaseConnector(host=config["db_host"],
                                 user=config["db_user"],
                                 password=config["db_password"],
                                 database=config["db_name"])

    row_data = maria_client.retrieve_data(config["client_id"], config["device_id"])

    if row_data:
        logger.debug("Row retrieved successfully:")
        logger.debug(row_data)
        
        # 0 ID
        # 1 device_id
        # 2 client_id
        # 3 stream_url
        # 4 preview_url
        stream_url, preview_url = row_data[3], row_data[4]
        config["stream_url"], config["preview_url"] = stream_url, preview_url

        if controller:
            controller.change_source(stream_url)
        logger.debug("Source URL changed successfully")
        with open(config_file, 'w') as f:
            json.dump(config, f)
        logger.debug("New config saved")
        return True
    else:
        logger.warning("Row not found or error occurred")
        return False
