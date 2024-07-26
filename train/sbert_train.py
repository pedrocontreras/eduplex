import pickle
from sentence_transformers import SentenceTransformer
from db.esco import *
from include.config import env_config
import torch


# @todo add logger
def train_model_description(db_esco, model, trained_model):
    """
    Trains a LLM using SBERT and the description from the skills in the ESCO database
    @param db_esco: path to ESCO database location
    @param model: SBERT larnguage mode name
    @param trained_model: output file contained the trained serialised language model
    @return:
    """
    if torch.backends.mps.is_available():
        torch_device = torch.device('mps')
    elif torch.cuda.is_available():
        torch_device = 'cuda'
    else:
        torch_device = 'cpu'
    esco_skills = get_skills_description(db_esco)  # retrieves ESCO's skills description
    flat_skills = [item for sublist in esco_skills for item in sublist]

    try:
        embedder = SentenceTransformer(model)
        #  save model to disk
        with open(trained_model, "wb") as fo:
            pickle.dump(embedder.encode(flat_skills, device=torch_device, convert_to_tensor=True), fo)
    except IOError as err:
        print(err)

    return 0


def train_model_merged_label(db_esco, model, trained_model):
    """
    Trains a LLM using SBERT and the merged preferred and alternative labels  from the skills in the ESCO database
    @param db_esco: ESCO database location
    @param model:  language model to use
    @param trained_model: output trained and serialised languaged model
    @return:
    """
    # check best torch_device

    if torch.backends.mps.is_available():
        torch_device = torch.device('mps')
    elif torch.cuda.is_available():
        torch_device = 'cuda'
    else:
        torch_device = 'cpu'

    esco_skill_labels = get_skills_merged_labels(db_esco)  # retrieves ESCO's skills labels
    flat_skills_labels = [item for sublist in esco_skill_labels for item in sublist]

    try:
        embedder = SentenceTransformer(model)
        #  save model to disk
        with open(trained_model, "wb") as fo:
            pickle.dump(embedder.encode(esco_skill_labels, device=torch_device, convert_to_tensor=True), fo)
    except IOError as err:
        print(err)

    return 0


if __name__ == "__main__":
    # demonstration of how to call the training functions
    conf = env_config("config_sbert_train.env")
    # train model in German
    # train_model_description(conf.get('ESCO_DB_DE'), conf.get('SBERT_LANG_MODEL'), conf.get('SBERT_TRAINED_MODEL_DE'))
    # train model in English
    train_model_description(conf.get('LOCATION_ESCO_DB_EN'), conf.get('LLM_NAME'), conf.get('LOCATION_TRAINED_MODEL_DESC_EN'))
    # train label models
    # print(conf.get("LLM_NAME"))
    # train_model_merged_label(conf.get("LOCATION_ESCO_DB_EN"), conf.get("LLM_NAME"),
    #                        conf.get("LOCATION_TRAINED_MODEL_LABEL_EN"))

