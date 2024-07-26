import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import torch

from db.esco import get_skills_record


def read_file(fn):
    arr = np.loadtxt(fn, delimiter="|", dtype=str)
    return arr


def train_text(file_in, llm_model, out_trained_model_title, out_trained_model_desc):
    # prepare data
    dat = read_file(file_in)
    title = [row[0] for row in dat]
    desc = [row[1] for row in dat]

    try:
        embedder_t = SentenceTransformer(llm_model)
        embedder_d = SentenceTransformer(llm_model)
        #  save model to disk
        with open(out_trained_model_title, "wb") as fo_t:
            pickle.dump(embedder_t.encode(title, convert_to_tensor=True), fo_t)
        with open(out_trained_model_desc, "wb") as fo_d:
            pickle.dump(embedder_d.encode(desc, convert_to_tensor=True), fo_d)
    except IOError as err:
        print(err)

    return 0


def sbert_title_matcher(source_titles, embedder, corpus_embeddings, query, num_matches):
    top_k = num_matches
    query_embedding = embedder.encode(query, convert_to_tensor=True)

    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)

    match = {}
    cnt = 0
    for score, idx in zip(top_results[0], top_results[1]):
        sco = "{:.4f}".format(score)
        print("{0}\t{1}\t{2}".format(int(idx+1), sco,  str(source_titles[idx])))
        '''''
        match[cnt] = {
            'score': str(sco),
            'index': str(idx),
             title': str(source_titles[idx])
        }
        cnt = cnt + 1
        '''
    return 0


def sbert_description_matcher(source_desc, embedder, corpus_embeddings, query, num_matches):
    top_k = num_matches
    query_embedding = embedder.encode(query, convert_to_tensor=True)

    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    match = {}
    for score, idx in zip(top_results[0], top_results[1]):
        sco = "{:.4f}".format(score)
        print("{0}\t{1}\t{2}".format(int(idx+1), sco,  str(source_desc[idx])))
        '''''
        match[cnt] = {
            'score': str(sco),
            'index': str(idx),
             title': str(source_titles[idx])
        }
        cnt = cnt + 1
        '''
    return 0


def train():
    train_text('../data/courses/courses.psv',
               "all-MiniLM-L6-v2",
               "../data/models/sbert_title_en.pkl",
               "../data/models/sbert_desc_en.pkl")


def query_title(query, n_matches):
    sbert_mdl = "all-MiniLM-L6-v2"
    sbert_serialised_title_en = "../data/models/sbert_title_en.pkl"
    f_in = read_file('../data/courses/courses.psv')
    src_titles = [row[0] for row in f_in]

    # q = "Enhancing Customs Compliance and Traceability with Blockchain Technology"
    embedder = SentenceTransformer(sbert_mdl)
    with open(sbert_serialised_title_en, "rb") as fIn:
        trained_embedding_en = pickle.load(fIn)

    sbert_title_matcher(src_titles, embedder, trained_embedding_en, query, n_matches)


def query_labels(n_matches):
    sbert_mdl = "all-MiniLM-L6-v2"
    db_esco = "../../data/db/esco_en_v1.1.1.sqlite"
    serialised_merged_labels_en = "../../data/models/all-MiniLM-L6-v2_label_merged_en.pkl"
    f_in = read_file('../../data/courses/wbs_courses_titles.csv')
    src_titles = list(f_in)

    # q = "Enhancing Customs Compliance and Traceability with Blockchain Technology"
    embedder = SentenceTransformer(sbert_mdl)
    with open(serialised_merged_labels_en, "rb") as fIn:
        trained_embedding_en = pickle.load(fIn)

    for query in src_titles:
        print(query)
        query_embedding = embedder.encode(query, convert_to_tensor=True)

        # We use cosine-similarity and torch.topk to find the highest 5 scores
        cos_scores = util.cos_sim(query_embedding, trained_embedding_en)[0]
        top_results = torch.topk(cos_scores, k=n_matches)

        for score, idx in zip(top_results[0], top_results[1]):
            print(idx)
            sco = "{:.4f}".format(score)
            esco_record = get_skills_record(db_esco, int(idx))[0]
            print("{0}\t{1}\t{2}".format(int(idx + 1), sco, esco_record[4]))

            '''''
            match[cnt] = {
                'score': str(sco),
                'index': str(idx),
                 title': str(source_titles[idx])
            }
            cnt = cnt + 1
            '''
        print("-----------------------------------------")


def query_description(query, n_matches):
    sbert_mdl = "all-MiniLM-L6-v2"
    sbert_serialised_desc_en = "../data/models/sbert_desc_en.pkl"
    f_in = read_file('../data/courses/courses.psv')
    src_desc = [row[1] for row in f_in]

    embedder = SentenceTransformer(sbert_mdl)
    with open(sbert_serialised_desc_en, "rb") as fIn:
        trained_embedding_en = pickle.load(fIn)

    sbert_description_matcher(src_desc, embedder, trained_embedding_en, query, n_matches)


def test_accuracy_titles(hits):

    f_in = read_file('../data/courses/test_accuracy.txt')
    src_titles = [row for row in f_in]
    cnt = 0
    for i in src_titles:
        cnt += 1
        print("{0}\t\t\t{1}".format(cnt, i))
        query_title(i, hits)
        print("----------------")


def test_accuracy_desc(hits):

    f_in = read_file('../data/courses/test_accuracy.txt')
    src_desc = [row for row in f_in]
    cnt = 0
    for i in src_desc:
        cnt += 1
        print("{0}\t\t\t{1}".format(cnt, i))
        query_description(i, hits)
        print("----------------")


if __name__ == '__main__':
    print("---------------Matching against titles------------------------")
    query_labels(2)
    # test_accuracy_titles(10)
    #print("---------------Matching against descriptions------------------------")
    #test_accuracy_desc(10)

