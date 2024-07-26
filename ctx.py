import pickle

import torch
from sentence_transformers import SentenceTransformer
from db.esco import get_skills_description, get_skills_merged_labels
from include.config import env_config
from include.logger import initialize_logger


def handler():
    """
    Context handler to manage all global variables
    @return: dictionary with global variables
    """
    context = {}
    PROCESSOR_CONFIG = "config.env"
    conf = env_config(PROCESSOR_CONFIG)

    llm_name = conf.get('LLM_NAME')
    location_trained_model_desc_en = conf.get('LOCATION_TRAINED_MODEL_DESC_EN')
    location_trained_model_desc_de = conf.get('LOCATION_TRAINED_MODEL_DESC_DE')
    location_trained_model_label_en = conf.get('LOCATION_TRAINED_MODEL_LABEL_EN')
    location_trained_model_label_de = conf.get('LOCATION_TRAINED_MODEL_LABEL_DE')
    location_db_esco_en = conf.get('LOCATION_ESCO_DB_EN')
    location_db_esco_de = conf.get('LOCATION_ESCO_DB_DE')
    location_log_folder = conf.get('LOCATION_LOG_FOLDER')
    log_level = conf.get('LOG_LEVEL')
    num_matches = conf.get('NUM_MATCHES')

    # --------------------------------------------------------

    logger = initialize_logger(location_log_folder, log_level)
    logger.debug('Server started')

    # check best torch_device
    if torch.backends.mps.is_available():
        torch_device = torch.device('mps')
    elif torch.cuda.is_available():
        torch_device = 'cuda'
    else:
        torch_device = 'cpu'
    print("torch_device:" + str(torch_device))
    # prepare global data, we may move this to the contexter
    esco_skills_list_desc_en = get_skills_description(location_db_esco_en)
    esco_skills_list_desc_de = get_skills_description(location_db_esco_de)
    esco_skills_list_label_en = get_skills_merged_labels(location_db_esco_en)
    esco_skills_list_label_de = get_skills_merged_labels(location_db_esco_de)

    st_object_model = SentenceTransformer(llm_name, device=torch_device)  # model object based on LLM

    with open(location_trained_model_desc_en, "rb") as fIn:
        inmem_trained_desc_en = pickle.load(fIn)
        logger.debug('Loading sbert model trained with ESCO descriptions in English')

    with open(location_trained_model_desc_de, "rb") as fIn:
        inmem_trained_desc_de = pickle.load(fIn)
        logger.debug('Loading sbert model trained with ESCO descriptions in German')

    with open(location_trained_model_label_en, "rb") as fIn:
        inmem_trained_label_en = pickle.load(fIn)
        logger.debug('Loading sbert model trained with ESCO merged labels in English')

    with open(location_trained_model_label_de, "rb") as fIn:
        inmem_trained_label_de = pickle.load(fIn)
        logger.debug('Loading sbert model trained with ESCO merged labels in German')

    logger.debug('Loading global variables into contexter')
    context.update({"llm_name": llm_name})
    context.update({"location_trained_model_desc_en": location_trained_model_desc_en})
    context.update({"location_trained_model_desc_de": location_trained_model_desc_de})
    context.update({"location_trained_model_label_en": location_trained_model_label_en})
    context.update({"location_trained_model_label_de": location_trained_model_label_de})
    context.update({"location_db_esco_en": location_db_esco_en})
    context.update({"location_db_esco_de": location_db_esco_de})
    context.update({"location_log_folder": location_log_folder})
    context.update({"log_level": log_level})
    context.update({"logger": logger})
    context.update({"num_matches": num_matches})
    context.update({"esco_skills_list_desc_en": esco_skills_list_desc_en})
    context.update({"esco_skills_list_desc_de": esco_skills_list_desc_de})
    context.update({"esco_skills_list_label_en": esco_skills_list_label_en})
    context.update({"esco_skills_list_label_de": esco_skills_list_label_de})
    context.update({"st_object_model": st_object_model})
    context.update({"inmem_trained_desc_en": inmem_trained_desc_en})
    context.update({"inmem_trained_desc_de": inmem_trained_desc_de})
    context.update({"inmem_trained_label_en": inmem_trained_label_en})
    context.update({"inmem_trained_label_de": inmem_trained_label_de})
    context.update({"torch_device": torch_device})

    return context
