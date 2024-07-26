"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging

import uvicorn
from fastapi import FastAPI

import ctx
from quart_cors import *
from quart import Quart, request, jsonify
from pyfiglet import Figlet
from matcher.sbert import (sbert_skills__desc_matcher, sbert_get_vector, sbert_skills_compare_matcher,
                           skills_compare_retriever)
from include import logger

logging.getLogger('asyncio').setLevel(logging.ERROR)  # remove asyncio logging
# --------------------------------------------------------
app = FastAPI()

f = Figlet(font='slant')
print(f.renderText('E d u P l e x'))
# --------------------------------------------------------------------------
# GLOBAL CONTEXT
ctx = ctx.handler()
logger = ctx["logger"]
# --------------------------------------------------------------------------


@app.get('/match_desc_en/<string:query>')
async def match_desc_en(query):
    logger.debug('GET /sbert_desc_en/{}'.format(query))
    resp = sbert_skills__desc_matcher(ctx, "en", query)
    return resp


@app.get('/match_desc_de/<string:query>')
async def match_desc_de(query):
    logger.debug('GET /sbert_desc_de/{}'.format(query))
    resp = sbert_skills__desc_matcher(ctx, "de", query)
    return resp


@app.get('/vectorise/<string:query>')
async def vectorise(query):
    logger.debug('GET /vectorise/{}'.format(query))
    rsp = sbert_get_vector(ctx, query)
    return rsp


@app.get('/compute_compare_skills/')
async def compute_compare_skills():
    """
    Takes a JSON file with a pre-defined language and computes similarity scores for skills based on ESCO descriptions
    Similarity score is computed for each pair of skills. Currently only english is supported
    {
        "language": "en",
        "skill": "Manage musical staff",
        "skills_eval": [
            "nage musical staff",
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


@app.get('/precomputed_compare_skills/')
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
            "nage musical staff",
            "supervise correctional procedures",
            "apply anti-oppressive practices"
        ]
    }
    @return: JSON file with cosine similarity scores
    """
    if request.is_json:
        data_json = await request.get_json()
        resp = skills_compare_retriever(ctx, data_json)
    else:
        resp = jsonify('{Well formed JSON is requiered, please check request}')
        logger.debug('{}'.format(resp))
    return resp

# do not use this in production, run the app as follows: $ hypercorn mains:app

uvicorn.run(app, host="127.0.0.1", port=5000)
