# Trained models 
This folder contains the trained models: this is as follws:

Sentence Transformers trained model (https://www.sbert.net/)

Models leaderboard can be seen here:
https://www.sbert.net/docs/pretrained_models.html
https://huggingface.co/spaces/mteb/leaderboard


Model to experiment which part of the course text is best. The all-MiniLM-L6-v2 model is used as benchmark because it is fastest.
Notice that the file name describes which part of the ESCO text was used to train the model.
For example: sbert_desc_de.pkl is a SBERT based LLM which was trained using the ESCO descriptions 

| file name                            | model                      | 
|--------------------------------------|----------------------------|
| sbert_desc_de.pkl                    | all-MiniLM-L6-v2           |
| sbert_label_desc_de.pkl              | all-MiniLM-L6-v2           |
| sbert_label_serialised_en.pkl        | all-MiniLM-L6-v2           |
| sbert_serialised_de.pkl              | all-MiniLM-L6-v2           |
| sbert_serialised_de.pkl              | all-MiniLM-L6-v2           |



| file name                            | model                      |
|--------------------------------------|----------------------------|
| sbert_mpnet_desc_de.pkl              | all-MiniLM-L6-v2           |
| sbert_mpnet_desc_de.pkl              | all-mpnet-base-v2          |
| sbert_multi-qa-mpnet_desc_de.pkl     | multi-qa-mpnet-base-dot-v1 |
| sbert_bge-large_desc_de.pkl          | BAAI/bge-large-en-v1.5     |

```
                     Name	 columns	    rows
   multi-qa-mpnet_desc_de	     768	   13896
            mpnet_desc_de	     768	   13896
          msmarco_desc_de	     768	   13896
      sbert_label_desc_de	     384	   13896
      sbert_serialised_en	     384	   13896
            sbert_desc_de	     384	   13896
        bge-large_desc_de	    1024	   13896
      sbert_serialised_de	     384	   13896
         e5-large_desc_de	    1024	   13896
                 gte-tiny	     384	   13896
sbert_label_serialised_en	     384	   13896
                gte-large	    1024	   13896
```
