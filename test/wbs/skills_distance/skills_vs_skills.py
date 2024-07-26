import pickle

from db.esco import get_skills_description
from sentence_transformers import SentenceTransformer, util


def train_model_description(db_esco, model, trained_model):
    # prepare data
    print("train model with skills descriptions: {0}\t{1}\t{2}".format(db_esco, model, trained_model))
    esco_skills = get_skills_description(db_esco)  # retrieves ESCO's skills description
    flat_skills = [item for sublist in esco_skills for item in sublist]

    try:
        embedder = SentenceTransformer(model)
        #  save model to disk
        with open(trained_model, "wb") as fo:
            pickle.dump(embedder.encode(flat_skills, convert_to_tensor=True), fo)
    except IOError as err:
        print(err)

    return 0


def skills2skills_scores(sbert_serialised, file_out):
    """
    calculates skills to skills cosine distance for all data within a pretrained model
    for example, if we have trained a model with ESCO' descriptions, there are total of
    13896 skills columns, and 13896 rows,  then aprox. 193 millions of data points
    @param sbert_serialised: pre-trained model
    @param file_out: file with all skills agaist all skills
    @return: 0 if succefull
    """
    with open(sbert_serialised, "rb") as fIn:
        trained_embedding = pickle.load(fIn)

    f = open(file_out, "w")

    size = trained_embedding.shape[0]

    for i in range(size):
        for j in range(size):
            cos_score = util.cos_sim(trained_embedding[i], trained_embedding[j])
            score = cos_score.item()
            val = str(round(float(score), 6))
            f.write(val+' ')
            if val == "1.0":
                break
        f.write("\n")
    f.close()
    return 0


if __name__ == "__main__":
    sbert_serialised = "../../data/models/all-MiniLM-L12-v2_desc_en.pkl"
    skills2skills_scores(sbert_serialised, "skills_vs_skills.txt")


