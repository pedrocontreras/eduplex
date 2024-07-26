import sqlite3
import time
import numpy
import numpy as np
import pandas as pd
import pickle
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import torch


def get_semantic_title(fin):
    df1 = pd.read_excel(fin)
    df2 = df1.reindex(columns=['semantic-title'])
    return df2.to_numpy()


def get_semantic_description(fin):
    df1 = pd.read_excel(fin)
    df2 = df1.reindex(columns=['semantic-description'])
    return df2.to_numpy()


def get_semantic_goal(fin):
    df1 = pd.read_excel(fin)
    df2 = df1.reindex(columns=['semantic-learning_goal'])
    return df2.to_numpy()


def get_semantic_title_desc(fin):
    df1 = pd.read_excel(fin)
    df_out = []
    cnt = 0
    for index, row in df1.iterrows():
        cnt += 1
        r = row["semantic-title"] + " " + row["semantic-description"]
        df_out.append(r)
    return numpy.array(df_out)


def get_semantic_title_goal(fin):
    df1 = pd.read_excel(fin)
    df_out = []
    cnt = 0
    for index, row in df1.iterrows():
        cnt += 1
        r = row["semantic-title"] + " " + row["semantic-learning_goal"]
        df_out.append(r)
    return numpy.array(df_out)


def get_semantic_desc_goal(fin):
    df1 = pd.read_excel(fin)
    df_out = []
    cnt = 0
    for index, row in df1.iterrows():
        cnt += 1
        r = row["semantic-description"] + " " + row["semantic-learning_goal"]
        df_out.append(r)
    return numpy.array(df_out)


def get_semantic_goal_desc(fin):
    df1 = pd.read_excel(fin)
    df_out = []
    cnt = 0
    for index, row in df1.iterrows():
        cnt += 1
        r = row["semantic-learning_goal"] + " " + row["semantic-description"]
        df_out.append(r)
    return numpy.array(df_out)


def get_semantic_title_desc_goal(fin):
    df1 = pd.read_excel(fin)
    df_out = []
    cnt = 0
    for index, row in df1.iterrows():
        cnt += 1
        r = row["semantic-title"] + " " + row["semantic-description"] + " " + row["semantic-learning_goal"]
        df_out.append(r)
    return numpy.array(df_out)


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
    statement = 'SELECT * FROM skills WHERE rowid = ' + rowid + ';'
    cursor.execute(statement)
    skills = cursor.fetchall()

    return skills


def sbert_skills_matcher_humanreadable(db_esco, skills, embedder, corpus_embeddings, q_num, query,  num_matches, pp):

    top_k = min(int(num_matches), len(skills))
    query_embedding = embedder.encode(query, convert_to_tensor=True)

    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)

    skill_idx = {}
    skill_score = {}
    cnt = 0

    for score, idx in zip(top_results[0], top_results[1]):
        sco = "{:.4f}".format(score)
        esco_record = get_skills_record(db_esco, int(idx))[0]
        esco_skill = str(esco_record[4])

        if not pp:
            print("{0}\tG\t0\t{1:>4}\t{2:>8}\t{3:>8}\t{4}".format(q_num, cnt, sco, idx, esco_skill))
        skill_idx[cnt] = "{0}".format(idx)
        skill_score[cnt] = "{0}".format(sco)
        cnt = cnt + 1

    return skill_idx, skill_score


def sbert_skills_matcher(db_esco, skills, embedder, corpus_embeddings, query, num_matches, pp):

    top_k = min(int(num_matches), len(skills))
    query_embedding = embedder.encode(query, convert_to_tensor=True)

    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)

    id = {}
    skill_idx = {}
    skill_score = {}
    skill_name = {}
    skill_desc = {}

    cnt = 0

    for score, idx in zip(top_results[0], top_results[1]):
        sco = "{:.4f}".format(score)
        esco_record = get_skills_record(db_esco, int(idx))[0]
        esco_skill = str(esco_record[4])
        esco_desc = str(esco_record[12]).rstrip()

        # if not pp:
        #     print("{0:>8}\t{1:>8}\t{2:>8}\t{3:>70}\t{4}".format(cnt, sco, idx, esco_skill, esco_desc))
        id[cnt] = "{0}".format(cnt)
        skill_idx[cnt] = "{0}".format(idx)
        skill_score[cnt] = "{0}".format(sco)
        skill_name[cnt] = "{0}".format(esco_skill)
        skill_desc[cnt] = "{0}".format(esco_desc)
        cnt = cnt + 1

    id_l = id.values()
    skills_id_l = skill_idx.values()
    skills_score_l = skill_score.values()
    skill_name_l = skill_name.values()
    skill_desc_l = skill_desc.values()
    res = zip(id_l, skills_id_l, skills_score_l, skill_name_l, skill_desc_l)
    df = pd.DataFrame(res, columns=['num', 'id', 'score', 'skill_name', 'desc'])

    # for ind in df.index:
    #     print(df['num'][ind], df['id'][ind], df['score'][ind], df['skill_name'][ind], df['desc'][ind])

    # return skill_idx, skill_score, skill_name, skill_desc
    return df


def sbert_skills_vs_skills_matcher(db_esco, skills, embedder, corpus_embeddings, query, num_matches):
    top_k = min(int(num_matches), len(skills))
    query_embedding = embedder.encode(query, convert_to_tensor=True)   # run this for cuda

    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)

    id = {}
    skill_idx = {}
    skill_score = {}
    skill_name = {}

    cnt = 0
    for score, idx in zip(top_results[0], top_results[1]):
        sco = "{:.4f}".format(score)
        esco_record = get_skills_record(db_esco, int(idx))[0]
        esco_skill = str(esco_record[4])
        id[cnt] = "{0}".format(cnt)
        skill_idx[cnt] = "{0}".format(idx+1)
        skill_score[cnt] = "{0}".format(sco)
        skill_name[cnt] = "{0}".format(esco_skill)
        cnt = cnt + 1

    id_l = id.values()
    skills_id_l = skill_idx.values()
    skills_score_l = skill_score.values()
    skill_name_l = skill_name.values()
    res = zip(id_l, skills_id_l, skills_score_l, skill_name_l)
    df = pd.DataFrame(res, columns=['num', 'id', 'score', 'skill_name'])

    return df


def wbs_skills_vs_skills_query(df_query, db_esco, sbert_mdl, sbert_serialised, n_matches):
    esco_skills = get_skills_description(db_esco)
    embedder = SentenceTransformer(sbert_mdl)
    with open(sbert_serialised, "rb") as fIn:
        trained_embedding = pickle.load(fIn)
    f = open('analysis/skills_vs_skills/skills_vs_skills.tsv', 'w')

    f.write("skill_id\tskill_name\tranking\tscore\tskill_id_match\tskils_name_match\tflag\n")
    count = 0
    for i in df_query:
        count += 1
        query = ' '.join(i)
        match_results = sbert_skills_vs_skills_matcher(db_esco, esco_skills, embedder, trained_embedding, query,
                                                       n_matches)
        # columns=['num', 'id', 'score', 'skill_name']
        for index, row in match_results.iterrows():
            num = row["num"]
            skill_id = row["id"]
            cos_score = row["score"]
            skill_name = row["skill_name"]
            if num == "0":
                base_skill_id = skill_id
                base_skill_name = skill_name
                continue

            f.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t0\n".format(base_skill_id, base_skill_name, num, skill_id,
                                                               cos_score, skill_name,))
    f.close()
    return 0


def wbs_query(df_query, db_esco, sbert_mdl, sbert_serialised, n_matches, p_overview, p_switch):
    esco_skills = get_skills_description(db_esco)
    embedder = SentenceTransformer(sbert_mdl)
    with open(sbert_serialised, "rb") as fIn:
        trained_embedding = pickle.load(fIn)

    count = 0
    for i in df_query:
        count += 1
        query = ' '.join(i)
        if not p_overview:
            print("==========================")
            print("{0}\t{1}".format(count, query))
        # skills_idx, skills_score, skills_name, skills_desc = sbert_skills_matcher(db_esco, esco_skills, embedder,
        #                                                                           trained_embedding, query, n_matches,
        #                                                                           p_overview)
        match_results = sbert_skills_matcher(db_esco, esco_skills, embedder, trained_embedding, query, n_matches,
                                             p_overview)
        # cross-encoder for re-ranking
        re_rank = cross_encoder(query, match_results)

        # @TODO fix the print function to adapted to the new return structure of the sbert_skills_matcher
        if p_overview:
            print_results(p_switch, count, match_results)


# @TODO change this function to use the new "results" structure instead of individual columns
def print_results(swtc, cnt, skills_idx, skills_score):
    print("{0}".format(cnt), end="\t")
    match swtc:
        case 1:  # print skill_id/score
            for k in skills_idx:
                print("{:>8}/{}".format(skills_idx[k], skills_score[k]), end="\t")
            print("\r")
        case 2:  # print skill_id
            for k, v in skills_idx.items():
                print("{:>8}".format(v), end="\t")
            print("\r")
        case 3:  # print score
            for k, v in skills_score.items():
                print("{:>8}".format(v), end="\t")
            print("\r")


def cross_encoder(query, matches_df):
    # matches_df columns=['num', 'id', 'score', 'skill_name', 'desc'])
    start_time = time.time()

    model = CrossEncoder('cross-encoder/ms-marco-TinyBERT-L-2')

    # Concatenate the query and all passages and predict the scores for the pairs [query, passage]
    model_inputs = [[query, desc] for desc in matches_df['desc'].tolist()]

    rerank_scores = model.predict(model_inputs)
    # add rerank score as a new column matches_df columns=['num', 'id', 'score', 'rerank' 'skill_name', 'desc'])
    matches_df.insert(loc=3, column='rerank', value=rerank_scores)
    print(matches_df.iloc[:, 1:6].to_string())

    print("---- re-rank ----")
    rerank_df = matches_df.sort_values(by=['rerank'], ascending=False)
    print(rerank_df.iloc[:, 1:6].to_string())
    return rerank_df


if __name__ == '__main__':
    # Load variables
    print_overview = True
    # only active when print_overview = True
    p_switch = 2    # 1: print skill_idx/score; 2: print skill_idx; 3: print score
    n_matches = 11
    TRAIN_LANGUAGE = 'EN'

    train_model = 'gte-large'
    llm_base_name = "thenlper/gte-large"
    db_esco = ""
    if TRAIN_LANGUAGE == 'DE':
        query_file = "../dat/wbs_courses_de.xlsx"
        db_esco = "../../data/db/esco_de_v1.1.1.sqlite"
        trained_mdl_desc = "../../data/models/" + train_model + "_desc_de.pkl"  # trained with esco descriptions
        trained_mdl_label = "../../data/models/" + train_model + "_label_de.pkl"  # trained with esco descriptions
    elif TRAIN_LANGUAGE == 'EN':
        query_file = "../dat/wbs_courses_en.xlsx"
        db_esco = "../../data/db/esco_en_v1.1.1.sqlite"
        trained_mdl_desc = "../../data/models/" + train_model + "_desc_en.pkl"  # trained with esco descriptions
        trained_mdl_label = "../../data/models/" + train_model + "_label_en.pkl"  # trained with esco descriptions

    # this produces a skills vs skills table for lookup
    # skills_query = get_skills_description(db_esco)
    # wbs_skills_vs_skills_query(skills_query, db_esco, llm_base_name, trained_mdl_desc, n_matches)

    skills_query = get_skills_description(db_esco)
    query = skills_query[0]
    print(query)
    embedder = SentenceTransformer(llm_base_name)
    query_embedding = embedder.encode(query)

    s = query_embedding[0]
    print(str(s))
    # for x in np.nditer(s):
    #     print(x)
    # print(s.split())
    # Load queries
    # semantic_title = get_semantic_title(query_file)
    # semantic_desc = get_semantic_description(query_file)
    # semantic_goal = get_semantic_goal(query_file)

    # queries with merged text
    # semantic_title_desc = get_semantic_title_desc(query_file)
    # semantic_title_goal = get_semantic_title_goal(query_file)
    # semantic_desc_goal = get_semantic_desc_goal(query_file)
    # semantic_goal_desc = get_semantic_goal_desc(query_file)
    # semantic_title_desc_goal = get_semantic_title_desc_goal(query_file)

    # print("---------------Matching Semantic Titles------------------------")
    # wbs_query(semantic_title, db_esco, llm_base_name, trained_mdl_label, n_matches, print_overview, p_switch)
    # print("---------------Matching Semantic Descriptions------------------------")
    # wbs_query(semantic_desc, db_esco, llm_base_name, trained_mdl_desc, n_matches, print_overview, p_switch)
    # print("---------------Matching Semantic Learning Goals------------------------")
    # wbs_query(semantic_goal, db_esco, llm_base_name, trained_mdl_desc, n_matches, print_overview, p_switch)

    # print("---------------Matching Semantic Description + Learning Goals------------------------")
    # wbs_query(semantic_desc_goal, db_esco, llm_base, trained_mdl, n_matches, print_overview, p_switch)

    # print("---------------Matching Semantic Title + Description------------------------")
    # wbs_query(semantic_title_desc, db_esco, llm_base, trained_mdl, n_matches, print_overview, p_switch)
    # print("---------------Matching Semantic Title + Learning Goals------------------------")
    # wbs_query(semantic_title_goal, db_esco, llm_base, trained_mdl, n_matches, print_overview, p_switch)

    # print("---------------Matching Semantic Learning Goals +  Description------------------------")
    # wbs_query(semantic_goal_desc, db_esco, llm_base, trained_mdl, n_matches, print_overview, p_switch)
    # print("---------------Matching Semantic Title + Description + Learning Goal------------------------")
    # wbs_query(semantic_title_desc_goal, db_esco, llm_base, trained_mdl, n_matches, print_overview, p_switch)
