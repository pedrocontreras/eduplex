"""
@author: Pedro Contreras
"""
import configparser


# ----------------------------------------------------------------
#                   Configuration file
# ----------------------------------------------------------------

# @todo add logger instead of print
def env_config(config_file):
    import os
    from dotenv import load_dotenv

    load_dotenv(config_file)
    config_dict = {}

    # General Config
    try:
        llm_name = os.getenv('LLM_NAME')
        location_trained_model_desc_en = os.getenv('LOCATION_TRAINED_MODEL_DESC_EN')
        location_trained_model_desc_de = os.getenv('LOCATION_TRAINED_MODEL_DESC_DE')
        location_trained_model_label_en = os.getenv('LOCATION_TRAINED_MODEL_LABEL_EN')
        location_trained_model_label_de = os.getenv('LOCATION_TRAINED_MODEL_LABEL_DE')
        location_db_esco_en = os.getenv('LOCATION_ESCO_DB_EN')
        location_db_esco_de = os.getenv('LOCATION_ESCO_DB_DE')
        location_log_folder = os.getenv('LOCATION_LOG_FOLDER')
        log_level = os.getenv('LOG_LEVEL')
        nun_matches = os.getenv('NUM_MATCHES')

        config_dict.update([('LLM_NAME', llm_name)])
        config_dict.update([('LOCATION_TRAINED_MODEL_DESC_EN', location_trained_model_desc_en)])
        config_dict.update([('LOCATION_TRAINED_MODEL_DESC_DE', location_trained_model_desc_de)])
        config_dict.update([('LOCATION_TRAINED_MODEL_LABEL_EN', location_trained_model_label_en)])
        config_dict.update([('LOCATION_TRAINED_MODEL_LABEL_DE', location_trained_model_label_de)])
        config_dict.update([('LOCATION_ESCO_DB_EN', location_db_esco_en)])
        config_dict.update([('LOCATION_ESCO_DB_DE', location_db_esco_de)])
        config_dict.update([('LOCATION_LOG_FOLDER', location_log_folder)])
        config_dict.update([('LOG_LEVEL', log_level)])
        config_dict.update([('NUM_MATCHES', nun_matches)])

    except Exception as error:
        print("please check configuration file: %s", error)
        return -1

    return config_dict
