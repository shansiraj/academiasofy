import yaml
import logging

def get_config():
    """
    Loads configuration parameters from a YAML file.
    """
    config_file = 'conf/config.yaml'
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
            logging.info(f"Configuration loaded from {config_file}")
            return config
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        raise

def get_research_paper_repository():
    config = get_config()
    return config['data']['research_paper_repository']

def get_research_paper_file_map():
    config = get_config()
    return config['data']['research_paper_file_map']

def get_positional_index():
    config = get_config()
    return config['index']['positional_index']

def get_total_docs():
    config = get_config()
    return config['data']['total_docs']

def is_scheduler_enabled():
    config = get_config()
    return config['search_engine']['is_scheduler_enabled']






