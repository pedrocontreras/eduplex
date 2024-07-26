import IPython
import spacy
# load default skills data base
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
from spacy.matcher import PhraseMatcher

# import skill extractor


# init params of skill extractor
nlp = spacy.load('en_core_web_lg')
# init skill extractor


skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

# extract skills from job_description
job_description = """
- Training to become an administrative clerk, lawyer or
Notary clerk, judicial clerk or a comparable one
commercial qualification
- Independent, result-oriented and structured way of working
- Enjoy dealing with audience and team spirit
- Confident demeanor, negotiation skills and assertiveness
- High sense of responsibility and the ability to be appreciative
and empathetic handling of the interlocutors
- Good IT skills, especially in MS Office

"""

annotations = skill_extractor.annotate(job_description)
skill_extractor.describe(annotations)
print(annotations)