# Text Analisys

Different AI experiments, NLP, etc...

## EduPlex

### Directory structure:

- The file called `server.py` is the main file to run the application
- `.env`  should be used to write down the initial parameters of the application. Logs should be automatically created.
- `requirements.txt` contains the requirements

### How to develop sbert with docker
- Run `docker-compose-socket-sbert.yml` (change the image version to force a rebuild)
- This will make the service available in [localhost:5000](http://localhost:5000/sbert_en/query=Examine%20images%20taken%20by%20telescopes%20in%20order%20to%20study%20phenomena%20and%20objects%20outside%20Earth%20atmosphere) without SSL

### How to build sbert service for production

- Change the image version in `docker-compose-socket-sbert.yml` (optionally use dockerfile `docker/child/Dockerfile` for a quick build without updating pip dependencies or `docker/Dockerfile` for a slower build from empty image)
- Run **docker-compose up** will create a new version tagged image
- Login to AWS ECR `aws ecr-public get-login-password --region us-east-1 --profile prdedupl | docker login --username AWS --password-stdin public.ecr.aws/eduplex_api` (change `prdedupl` with the name of your aws cli or `default` if you do not have many profiles)
- Push the image `docker push <image_tag>` (image_tag from yml file)

## Endpoints usage

- ### Find ESCO skill best match  based on a textual description in english 
    http://localhost:5000/match_desc_en/{string}

- ### Find ESCO skill best match  based on a textual description in german
    http://localhost:5000/match_desc_de/{string}

- ### Vectorise a text string based on the default LLM 
    http://localhost:5000/vectorise/{string}

- ### Compute skills similariry of existing skills in english

    http://localhost:5000/compute_compare_skills/

    Takes a JSON file with a pre-defined language and computes similarity scores for skills based on ESCO descriptions
    Similarity score is computed for each pair of skills. Currently only english is supported
 
    **Request:** 
    ```json
    {
        "language": "en",
        "skill": "Manage musical staff",
        "skills_eval": [
            "nage musical staff",
            "supervise correctional procedures",
            "apply anti-oppressive practices"
        ]
    }
    ```

    **Response:**
    ```json
    {
        "0": {
            "base_skill": "Manage musical staff",
            "base_skill_id": 1,
            "eval_skill": "nage musical staff",
            "eval_skill_id": -1,
            "score": -1
        },
        "1": {
            "base_skill": "Manage musical staff",
            "base_skill_id": 1,
            "eval_skill": "supervise correctional procedures",
            "eval_skill_id": 2,
            "score": 0.840195
        },
        "2": {
            "base_skill": "Manage musical staff",
            "base_skill_id": 1,
            "eval_skill": "apply anti-oppressive practices",
            "eval_skill_id": 3,
            "score": 0.788353
        }
    }
    ```

- ### Vectorise a text string based on the default LLM 
    
    http://localhost:5000/precomputed_compare_skills/

    Takes a JSON file with a pre-defined serialised LLM and retrieves similarity scores for skills based on ESCO
    descriptions. Scores are retrieved from a previously vectorised model containing all vectors for all ESCO's skills
    trained with ESCO descriptions. Thus, vector embeddings are not computed but retrieved, but semantic similarity is
    computed.
  
    **Request:** 
    ```json
    {
      "language": "en",
      "skill": "Manage musical staff",
      "skills_eval": [
          "nage musical staff",
          "supervise correctional procedures",
          "apply anti-oppressive practices"
      ]
    }
    ```




## License
The source code for the site is licensed under the **[MIT license](https://gitlab.com/eduplex-api)**, which you can find in the [LICENSE](https://gitlab.com/eduplex-api/text-analysis/-/blob/main/LICENSE) file.

