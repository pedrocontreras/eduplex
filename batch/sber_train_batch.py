import pickle
from sentence_transformers import SentenceTransformer
import sqlite3
import torch
from batch.parse_toml import *
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
    esco_skills = get_skills_description(db_esco)  # retrieves ESCO's skills description
    flat_skills = [item for sublist in esco_skills for item in sublist]

    try:
        embedder = SentenceTransformer(model)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        #  save model to disk
        with open(trained_model, "wb") as fo:
            pickle.dump(embedder.encode(flat_skills, device=device), fo)
    except IOError as err:
        print(err)

    return 0


def train_model_labels(db_esco, model, trained_model):
    # prepare data
    print("train model with skills labels:{0}\t{1}\t{2}".format(db_esco, model, trained_model))

    esco_skills = get_skills_preferred_label(db_esco)  # retrieves ESCO's skills description
    flat_skills = [item for sublist in esco_skills for item in sublist]

    try:
        embedder = SentenceTransformer(model)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        #  save model to disk
        with open(trained_model, "wb") as fo:
            pickle.dump(embedder.encode(flat_skills, device=device), fo)
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

    # prepare data
    esco_skill_labels_desc = get_skills_merged_labels_desc(db_esco)
    flat_skills_desc_labels = [item for sublist in esco_skill_labels_desc for item in sublist]
    try:
        embedder = SentenceTransformer(model)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        #  save model to disk
        with open(trained_model, "wb") as fo:
            pickle.dump(embedder.encode(esco_skill_labels_desc, device=device), fo)
    except IOError as err:
        print(err)

    return 0


if __name__ == "__main__":

    print("Start trainig")

    esco_db_en = "../data/db/esco_en_v1.1.1.sqlite"
    esco_db_de = "../data/db/esco_de_v1.1.1.sqlite"

    models_name = get_models('models.toml')

    for model in models_name:
        if model.find('/') != -1:
            short_name = model.partition("/")[2]
        else:
            short_name = model

        model_out_label_de = '../data/models/batch/{0}_label_de.pkl'.format(short_name)
        model_out_desc_de = '../data/models/batch/{0}_desc_de.pkl'.format(short_name)
        model_out_label_en = '../data/models/batch/{0}_label_en.pkl'.format(short_name)
        model_out_desc_en = '../data/models/batch/{0}_desc_en.pkl'.format(short_name)


        # train model in German
        start = time.time()
        train_model_labels(esco_db_de, model, model_out_label_de)
        train_model_description(esco_db_de, model, model_out_desc_de)
        end = time.time()
        run_time = round((end - start) / 60, 4)
        print("Model: {0} run time DE min:{1} ".format(model, run_time))

        # train model in English
        start = time.time()
        train_model_labels(esco_db_en, model, model_out_label_en)
        train_model_description(esco_db_en, model, model_out_desc_en)
        end = time.time()
        run_time = round((end - start) / 60, 4)
        print("Model: {0} run time EN min:{1} ".format(model, run_time))


