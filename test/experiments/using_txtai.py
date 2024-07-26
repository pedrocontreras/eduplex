from txtai.embeddings import Embeddings
from txtai.pipeline import Similarity

from db.esco import get_skills_description, get_skills_record
from parse.course_module import *


def save_embedding(embedding_model, index_file, data):
    mbds = Embeddings({"path": mdl_1})
    mbds.index([(uid, text, None) for uid, text in enumerate(skills)])
    mbds.save(index_file)
    logging.debug("saving embedding to disk: %s", index_file)

    return 0


def load_embedding(emb_file):
    emb_fromdisk = Embeddings()
    emb_fromdisk.load("index")

    embeddings = Embeddings()
    em = embeddings.load(emb_file)
    return em


def search(mbds, query, limit):
    return mbds.search(query, limit)


def stream(dataset, field, limit):
    index = 0
    for row in dataset:
        yield index, row[field], None
        index += 1

        if index >= limit:
            break


def search(mbdg, query, lmt):
    return [(result["score"], result["text"]) for result in mbdg.search(query, limit=lmt)]


def ranksearch(smlrt, query):
    results = [text for _, text in search(query)]
    return [(score, results[x]) for x, score in smlrt(query, results)]


def sentence_matcher(model, course_modules, skills):
    """
    Create embeddings model, backed by sentence-transformers & transformers
        see https://huggingface.co/sentence-transformers/nli-mpnet-base-v2
        this is a sentence-transformer BERT based embedding see https://www.sbert.net/

    :param model: language model to embed text
    :param course_modules: dataframe with course module
    :param skills: skill description

    :return:
    """
    embeddings = Embeddings({"path": model})

    print("%-20s %s" % ("Query", "Best Match"))
    print("-" * 50)
    course_description = course_modules[2]

    for query in course_description:
        # Get index of best section that best matches query

        uid = embeddings.similarity(query, skills)[0][0]
        print("----------------------")
        print(query)
        print(skills[uid])
        print("----------------------")

    return


def test(model, course_data, skills_data):
    course_description = course_data[2]
    print(type(course_description))
    print(course_description)
    print(type(skills_data))
    print(skills_data)


if __name__ == "__main__":
    # local variables
    # @TODO read these from a configuration file
    # ~450MB https://huggingface.co/sentence-transformers/nli-mpnet-base-v2
    mdl_1 = "sentence-transformers/nli-mpnet-base-v2"
    mdl_2 = "sentence-transformers/distiluse-base-multilingual-cased-v2"  # multi-language
    db_esco = "../data/db/esco_v1.1.0.sqlite"
    course_file_en = 'data/courses/imacs.docx'
    course_pickle = '../data/tmp/imacs.pkl'
    embedding_index = '../model/index.tar.gz'  # compressed index
    embedding_index2 = '../model/index2.tar.gz'  # compressed index

    # prepare data
    course_df = pickle2df(course_pickle)[2]   # retrieves only the course's descriptions
    skills = get_skills_description(db_esco)  # retrieves ESCO's skills description

    # create embedding with an index and save to disk
    save_embedding(mdl_1, embedding_index, skills)
    mbds = Embeddings({"path": mdl_1})
    mbds.index([(uid, text, None) for uid, text in enumerate(skills)])
    mbds.save("index")

    save_embedding(mdl_1, embedding_index, skills)

    course_module = pickle2df(course_pickle)
    course_name = course_module[0]
    qua_target = course_module[1]
    mod_contents = course_module[2]
    query = qua_target + mod_contents

    emb_fromdisk = Embeddings()
    emb_fromdisk.load("index")

    count = 0
    for q in query:

        uid = emb_fromdisk.search(q, 1)
        print("------------------------------------------------------")
        print("course name: ", course_name[count])
        print("course desc.: ", q)
        print("best esco match: ", uid)
        print("esco skill: ", get_skills_record(db_esco, uid[0][0])[0][4])  # get esco skill's name
        #  print(get_skills_record(db_esco, uid[0][0]))                     #  print esco record

        count += 1
