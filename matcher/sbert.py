import sqlite3
import torch
from quart import jsonify
from sentence_transformers import util
from include.utils import edit_distance, json_course_checker
from db.esco import get_desc_from_skillname, get_id_from_skillname, get_skills_record_conn
# from test.wbs.recommender.recommender import esco_recommender


def sbert_skills_desc_matcher(ctx, lang, query):
    """
    Uses Sentence BERT to match a query  to ESCO's skill's description
    @param ctx: contexter
    @param lang: language from the json request (ISO 639)
    @param query: query to match
    @return: json object with sequencial number, esco skill description, and esco skill
    """
    skills_desc = ""
    embedding = ""
    db_esco = ""
    if lang == "en":
        db_esco = ctx["location_db_esco_en"]
        skills_desc = ctx["esco_skills_list_desc_en"]
        embedding = ctx["inmem_trained_desc_en"]
    elif lang == "de":
        db_esco = ctx["location_db_esco_de"]
        skills_desc = ctx["esco_skills_list_desc_de"]
        embedding = ctx["inmem_trained_desc_de"]

    logger = ctx["logger"]
    embedder = ctx["st_object_model"]
    num_matches = ctx["num_matches"]
    device = ctx["torch_device"]

    top_k = min(int(num_matches), len(skills_desc))
    query_embedding = embedder.encode(query, device=device, show_progress_bar=False)

    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.cos_sim(query_embedding, embedding)[0]
    top_results = torch.topk(cos_scores, k=top_k)

    match = {}
    cnt = 0
    conn = sqlite3.connect(db_esco)
    for score, idx in zip(top_results[0], top_results[1]):
        sco = "{:.4f}".format(score)
        esco_record = get_skills_record_conn(conn, int(idx))[0]
        esco_id = int(idx + 1)
        skill_desc = str("".join(skills_desc[idx][0]))
        esco_uri = str(esco_record[1])
        esco_skill = str(esco_record[4])
        match[cnt] = {
            'skill': esco_skill,
            'score': sco,
            'skill_id': str(esco_id),
            'description': skill_desc,
            'uri': esco_uri
        }
        cnt = cnt + 1
    conn.close()
    logger.debug(match)
    return match


def sbert_skills_label_matcher(ctx, lang, query):
    """
    Uses Sentence BERT to match a query  to ESCO's skill's concadenated labels
    @param ctx: context to use for matching
    @param lang: language from the json request (ISO 639)
    @param query: query to match
    @return: json object with sequencial number, esco skill description, and esco skill
    """
    skills_label = ""
    embedding = ""
    db_esco = ""
    if lang == "en":
        db_esco = ctx["location_db_esco_en"]
        skills_label = ctx["esco_skills_list_label_en"]
        embedding = ctx["inmem_trained_label_en"]
    elif lang == "de":
        db_esco = ctx["location_db_esco_de"]
        skills_label = ctx["esco_skills_list_label_de"]
        embedding = ctx["inmem_trained_label_de"]

    logger = ctx["logger"]
    embedder = ctx["st_object_model"]
    num_matches = ctx["num_matches"]
    device = ctx["torch_device"]

    top_k = min(int(num_matches), len(skills_label))
    query_embedding = embedder.encode(query, device=device, show_progress_bar=False)

    # We use cosine-similarity and torch.topk to find the highest 5 scores
    embedding = embedding.to("cpu")  # @todo move all models to mac
    cos_scores = util.cos_sim(query_embedding, embedding)[0]
    top_results = torch.topk(cos_scores, k=top_k)

    match = {}
    cnt = 0
    conn = sqlite3.connect(db_esco)
    for score, idx in zip(top_results[0], top_results[1]):
        sco = "{:.4f}".format(score)
        esco_record = get_skills_record_conn(conn, int(idx))[0]
        esco_id = int(idx+1)
        esco_uri = str(esco_record[1])
        esco_skill = str(esco_record[4])
        ed, nor_ed = edit_distance(query, esco_skill)
        match[cnt] = {
            'skill': esco_skill,
            'skill_id': str(esco_id),
            'distance': str(ed),
            'score': sco,
            'uri': esco_uri
        }
        cnt = cnt + 1
    conn.close()
    logger.debug(match)
    return match


def sbert_get_vector(ctx, json_payload):
    """
    This method returns the vector representation of a string for a given model
    @param ctx: contexter
    @param json_payload: string to vectorise
    @return: json with componenys language_model, dimension, vector
    """
    logger = ctx["logger"]
    llm_name = ctx["llm_name"]
    embedder = ctx["st_object_model"]
    device = ctx["torch_device"]
    lang = json_payload["language"].strip().lower()
    logger.debug('GET /sbert_get_vector/{}'.format(json_payload))

    match = {}
    cnt = 0
    for query in json_payload['vectorise']:
        query_embedding = embedder.encode(query, device=device, show_progress_bar=False)
        dim = len(query_embedding)
        vector = query_embedding.tolist()
        match[cnt] = {
            'llm': llm_name,
            'dimension': dim,
            'language': lang,
            'text': query,
            'vector': vector
        }
        cnt += 1
        logger.debug('{0}'.format(match))

    return match


def sbert_skills_compare_matcher(ctx, json_payload):
    """
    Read a json file with containing a request to compare skills.
    Vectorisation and calculation are done diretly on the LLM.
    Only ENGLISH
    @param ctx: contexter
    @param json_payload: json with skills
    @return: JSON file, if exact match of skill is not found score = -1
    """
    logger = ctx["logger"]
    logger.debug('GET /sbert_skills_compare_matcher/{}'.format(json_payload))

    lang = json_payload["language"].strip().lower()

    if lang == "en":
        db_esco = ctx["location_db_esco_en"]
    elif lang == "de":
        db_esco = ctx["location_db_esco_de"]
    else:
        logger.debug("language no supported")
        return jsonify("{language no supported}")

    device = ctx["torch_device"]
    embedder = ctx["st_object_model"]

    # use only one connection object
    conn = sqlite3.connect(db_esco)
    cursor = conn.cursor()

    base_skill = json_payload['skill']
    base_desc = get_desc_from_skillname(cursor, base_skill)
    match = {}
    cnt = 0
    for i in json_payload['skills_eval']:
        eval_desc = get_desc_from_skillname(cursor, i)
        if base_desc == -1 or eval_desc == -1:
            logger.debug("skills do not match, please check that skill exist in ESCO. base skill: {0} || "
                         "evaluation: {1}".format(base_desc, eval_desc))
            match[cnt] = {
                'base_skill': base_skill,
                'eval_skill': i,
                'score': -1
            }

        else:
            base = embedder.encode(base_desc, device=device, show_progress_bar=False)
            eval = embedder.encode(eval_desc, device=device, show_progress_bar=False)
            score = util.cos_sim(base, eval)[0]
            match[cnt] = {
                'base_skill': base_skill,
                'eval_skill': i,
                'score': round(score.item(), 6)
            }
        cnt += 1
    conn.close()
    return match


def sbert_skills_compare_retriever(ctx, json_payload):
    """
    Read a json file with containing a request to compare skills.
    This method retreive the values from a pre-computed LLM
    Only ENGLISH
    @param ctx: contexter
    @param json_payload: json file with containing a request to compare skills
    @return: JSON file, if exact match of skill is not found score = -1
    """
    logger = ctx["logger"]
    logger.debug('GET /sbert_skills_compare_retriever/{}'.format(json_payload))

    lang = json_payload["language"].strip().lower()
    if lang == "en":
        db_esco = ctx["location_db_esco_en"]
        trained_embedding = ctx["inmem_trained_desc_en"]
    elif lang == "de":
        db_esco = ctx["location_db_esco_de"]
        trained_embedding = ctx["inmem_trained_desc_de"]
    else:
        logger.debug("language no supported")
        return jsonify("{language no supported}")

    # let's use only one connection object
    conn = sqlite3.connect(db_esco)
    cursor = conn.cursor()

    base_skill = json_payload['skill']
    base_id = get_id_from_skillname(cursor, base_skill)
    match = {}
    cnt = 0
    for i in json_payload['skills_eval']:
        eval_id = get_id_from_skillname(cursor, i)

        if base_id == -1 or eval_id == -1:
            logger.debug("skills do not match, please check that skill exist in ESCO. base skill: {0} || "
                         "evaluation: {1}".format(base_id, eval_id))
            match[cnt] = {
                'base_skill': base_skill,
                'base_skill_id': base_id,
                'eval_skill': i,
                'eval_skill_id': eval_id,
                'score': -1
            }
        else:
            # note that the database index starts from 1, but the LLM embedding index starts from 0
            cos_score = util.cos_sim(trained_embedding[base_id-1], trained_embedding[eval_id-1])

            match[cnt] = {
                'base_skill': base_skill,
                'base_skill_id': base_id,
                'eval_skill': i,
                'eval_skill_id': eval_id,
                'score': round(cos_score.item(), 6)
            }
        cnt += 1
    conn.close()
    return match


def skills_matcher(ctx, json_payload):
    """

    @param ctx:
    @param json_payload:
    @return:
    """
    logger = ctx["logger"]
    logger.debug('GET /skills_matcher/{}'.format(json_payload))

    resp = json_course_checker(json_payload)
    if resp != 1:
        logger.error('skills_matcher: please check JSON request')
    title = json_payload["title"]
    desc = json_payload["description"]
    goals = json_payload["learning_goals"]
    lang = json_payload["language"].strip().lower()
    if lang == "en" or lang == "de":
        pass
    else:
        logger.debug('Only English and German languages are supported')
        return "{Error: only English and German languages are supported}"

    match = {}
    logger.debug('Title suggested skills:')
    title_sugested_skills = sbert_skills_label_matcher(ctx, lang, title)
    logger.debug('Description suggested skills:')
    desc_sugested_skills = sbert_skills_desc_matcher(ctx, lang, desc)
    logger.debug('Learning Goals suggested skills:')
    goals_sugested_skills = sbert_skills_desc_matcher(ctx, lang, goals)

    match["title_skills"] = title_sugested_skills
    match["desc_skills"] = desc_sugested_skills
    match["goals_skills"] = goals_sugested_skills

    # esco_recommender(title_sugested_skills, desc_sugested_skills, goals_sugested_skills)
    return match
