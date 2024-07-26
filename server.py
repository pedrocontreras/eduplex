"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging

import ctx
from quart_cors import *
from quart import Quart, request, jsonify
from pyfiglet import Figlet
from matcher.sbert import (sbert_skills_desc_matcher, sbert_get_vector, sbert_skills_compare_matcher,
                           sbert_skills_label_matcher, sbert_skills_compare_retriever,
                           skills_matcher)

logging.getLogger('asyncio').setLevel(logging.ERROR)  # remove asyncio logging
# --------------------------------------------------------
app = Quart(__name__)
app = cors(app, allow_origin="*")

f = Figlet(font='slant')
print(f.renderText('E d u P l e x'))
# --------------------------------------------------------------------------
# GLOBAL CONTEXT
ctx = ctx.handler()
logger = ctx["logger"]
# --------------------------------------------------------------------------


@app.route('/match_desc_en/<string:query>')
async def match_desc_en(query):
    logger.debug('GET /sbert_desc_en/{}'.format(query))
    resp = sbert_skills_desc_matcher(ctx, "en", query)
    return jsonify(resp)


@app.route('/match_desc_de/<string:query>')
async def match_desc_de(query):
    logger.debug('GET /sbert_desc_de/{}'.format(query))
    resp = sbert_skills_desc_matcher(ctx, "de", query)
    return jsonify(resp)


@app.route('/match_label_en/<string:query>')
async def match_label_en(query):
    logger.debug('GET /match_label_en/{}'.format(query))
    resp = sbert_skills_label_matcher(ctx, "en", query)
    return jsonify(resp)


@app.route('/match_label_de/<string:query>')
async def match_label_de(query):
    logger.debug('GET /match_label_de/{}'.format(query))
    resp = sbert_skills_label_matcher(ctx, "de", query)
    return jsonify(resp)


@app.route('/vectorise/', methods=['GET'])
async def vectorise():
    """
    {
        "language": "en",
        "vectorise": [
            "Text A to vectorise",
            "Text B to vectorise",
            "Text C to vectorise"
        ]
    }
    @return: a JSON file with dimension, llm model, text to vectorise, and the numerical vector for eact text within
    the vectorise array
    """
    if request.is_json:
        data_json = await request.get_json()
        resp = sbert_get_vector(ctx, data_json)
    else:
        resp = jsonify('{Well formed JSON is requiered, please check request}')
        logger.debug('{}'.format(resp))
    return resp


@app.route('/compute_compare_skills/', methods=['GET'])
async def compute_compare_skills():
    """
    Takes a JSON file with a pre-defined language and computes similarity scores for skills based on ESCO descriptions
    Similarity score is computed for each pair of skills. Currently only english is supported
    {
        "language": "en",
        "skill": "Manage musical staff",
        "skills_eval": [
            "Manage musical staff",
            "supervise correctional procedures",
            "apply anti-oppressive practices"
        ]
    }
    @return: JSON file with cosine similarity scores
    """
    if request.is_json:
        data_json = await request.get_json()
        resp = sbert_skills_compare_matcher(ctx, data_json)
    else:
        resp = jsonify('{Well formed JSON is requiered, please check request}')
        logger.debug('{}'.format(resp))
    return resp


@app.route('/precomputed_compare_skills/', methods=['GET'])
async def precomputed_compare_skills():
    """
    Takes a JSON file with a pre-defined serialised LLM and retrieves similarity scores for skills based on ESCO
    descriptions. Scores are retrieved from a previously vectorised model containing all vectors for all ESCO's skills
    trained with ESCO descriptions. Thus vector embeddings are not computed but retrieved, but semantic similarity is
    computed.
    {
        "language": "en",
        "skill": "Manage musical staff",
        "skills_eval": [
            "manage musical staff",
            "supervise correctional procedures",
            "apply anti-oppressive practices"
        ]
    }
    @return: JSON file with cosine similarity scores
    """
    if request.is_json:
        data_json = await request.get_json()
        resp = sbert_skills_compare_retriever(ctx, data_json)
    else:
        resp = '{Well formed JSON is requiered, please check request}'
        logger.debug('{}'.format(resp))
    return jsonify(resp)


@app.route('/match_course_skills/', methods=['GET'])
async def match_course_skills():
    """
    {
        "language": "en",
        "title": "course tittle, e.g. Manage musical staff",
        "description": "course description",
        "learning_goals": "course learning goals"
    }
    @return: JSON file with top k matches for title, description, and learning goals
    """
    if request.is_json:
        data_json = await request.get_json()
        resp = skills_matcher(ctx, data_json)
    else:
        resp = '{Well formed JSON is requiered, please check request}'
        logger.debug('{}'.format(resp))
    return jsonify(resp)

# do not use this in production, run the app as follows: $ hypercorn server:app
app.run(host="0.0.0.0", debug=False, port=5000)
