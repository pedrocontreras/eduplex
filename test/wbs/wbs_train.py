import pickle

import torch
from sentence_transformers import SentenceTransformer
import sqlite3
from include.config import env_config
import time


# @todo add logger
def get_skills_description(db_file):
    """
    Connects to ESCO database and retrieves skills label, alternative label, hidden label and description
    :param db_file: database file location
    :return: list with description
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    statement = 'SELECT description FROM skills'
    cursor.execute(statement)
    records = cursor.fetchall()
    skills_desc = []
    for row in records:
        skills_desc.append([row[0]])
    conn.close()

    return skills_desc


def get_skills_preferred_label(db_file):
    """

    :param db_file: database file location
    :return: list with labels
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # statement = "SELECT  preferredLabel, altLabels FROM skills;"
    statement = "SELECT  preferredLabel FROM skills;"
    cursor.execute(statement)
    records = cursor.fetchall()
    skills_labels = []
    for row in records:
        '''''
        if row[0] == row[1]:
            labels = "{0}".format(row[0]).splitlines()
        else:
            labels = "{0}, {1}".format(row[0], row[1]).splitlines()
        '''
        labels = "{0}".format(row[0]).splitlines()
        skills_labels.append(labels)
    conn.close()

    return skills_labels


def get_skills_merged_labels_desc(db_file):
    """

    :param db_file: database file location
    :return: list with labels
    """
    print(db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    statement = ("SELECT  IFNULL(preferredLabel,'') ||'. '||  IFNULL(altLabels,'') ||'. '||  "
                 "IFNULL(hiddenLabels,'') ||'. '||  IFNULL(description,'')  as text FROM skills;")
    cursor.execute(statement)
    records = cursor.fetchall()
    skills = []
    for row in records:
        txt = "{0}".format(row)
        skills.append(txt)
    conn.close()

    return skills


def get_skills_record(db_file, rowid):
    """
    Connects to ESCO database and retrieves skills records for a given rowid
    :param rowid:
    :param db_file: database file location
    :return: list with description
    """
    rowid = str(rowid + 1)   # we offset 1 to rowid because models in the embedding start from 0, in sqlite start from 1
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    statement = 'SELECT  * FROM skills WHERE rowid = ' + rowid + ';'
    cursor.execute(statement)
    skills = cursor.fetchall()

    return skills


def train_model_description(db_esco, model, trained_model):
    # prepare data
    print("train model with skills descriptions: {0}\t{1}\t{2}".format(db_esco, model, trained_model))
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
            pickle.dump(embedder.encode(flat_skills,  device=torch_device), fo)
    except IOError as err:
        print(err)

    return 0


def train_model_labels(db_esco, model, trained_model):
    # prepare data
    print("train model with skills labels:{0}\t{1}\t{2}".format(db_esco, model, trained_model))
    if torch.backends.mps.is_available():
        torch_device = torch.device('mps')
    elif torch.cuda.is_available():
        torch_device = 'cuda'
    else:
        torch_device = 'cpu'

    esco_skills = get_skills_preferred_label(db_esco)  # retrieves ESCO's skills description
    flat_skills = [item for sublist in esco_skills for item in sublist]

    try:
        embedder = SentenceTransformer(model)
        #  save model to disk
        with open(trained_model, "wb") as fo:
            pickle.dump(embedder.encode(flat_skills,  device=torch_device), fo)
    except IOError as err:
        print(err)

    return 0


def train_model_merged_label_desc(db_esco, model, trained_model):
    """

    @param db_esco: database location
    @param model:  language model to use
    @param trained_model: output trained and serialised languaged model
    @return:
    """
    if torch.backends.mps.is_available():
        torch_device = torch.device('mps')
    elif torch.cuda.is_available():
        torch_device = 'cuda'
    else:
        torch_device = 'cpu'

    # prepare data
    esco_skill_labels_desc = get_skills_merged_labels_desc(db_esco)
    flat_skills_desc_labels = [item for sublist in esco_skill_labels_desc for item in sublist]
    try:
        embedder = SentenceTransformer(model)
        #  save model to disk
        with open(trained_model, "wb") as fo:
            pickle.dump(embedder.encode(esco_skill_labels_desc, device=torch_device, convert_to_tensor=True), fo)
    except IOError as err:
        print(err)

    return 0


if __name__ == "__main__":
    start = time.time()
    print("Start trainig")
    conf = env_config("config_sbert_train.env")

    llm = "intfloat/multilingual-e5-large-instruct"
    if llm.find('/') != -1:
        short_name = llm.partition("/")[2]
    else:
        short_name = llm

    # train model with ESCO's descriptions
    # train_model_description(conf.get('ESCO_DB_DE'), llm, '../../data/models/'+short_name+'_desc_de.pkl')
    train_model_description("../../data/db/esco_en_v1.1.1.sqlite", llm, '../../data/models/'+short_name+'_desc_en.pkl')

    end = time.time()
    run_time = round((end - start)/60, 4)
    print("Run time min: ", run_time)

    # train model with ESCO's labels
    # train_model_labels(conf.get('ESCO_DB_DE'), llm, '../../data/models/'+short_name+'_label_de.pkl')
    train_model_labels("../../data/db/esco_en_v1.1.1.sqlite", llm, '../../data/models/'+short_name+'_label_en.pkl')

    # train label + desc model in German
    # train_model_merged_label_desc(esco_db, conf.get("SBERT_LANG_MODEL"), "../../data/models/sbert_label_desc_de.pkl")

    end = time.time()
    run_time = round((end - start)/60,  4)
    print("Run time min: ", run_time)
