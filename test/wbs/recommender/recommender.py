import json

import ctx
from include.utils import json_course_checker
from matcher.sbert import sbert_skills_label_matcher, sbert_skills_desc_matcher


def skill_matcher(ctx, json_payload):
    """
    @param ctx:
    @param json_payload:
    @return:
    """

    resp = json_course_checker(json_payload)
    if resp != 1:
        print('skills_matcher: please check JSON request')
    title = json_payload["title"]
    desc = json_payload["description"]
    goals = json_payload["learning_goals"]

    match = {}
    title_sugested_skills = sbert_skills_label_matcher(ctx, "en", title)
    desc_sugested_skills = sbert_skills_desc_matcher(ctx, "en", desc)
    goals_sugested_skills = sbert_skills_desc_matcher(ctx, "en", goals)

    match["title_skills"] = title_sugested_skills
    match["desc_skills"] = desc_sugested_skills
    match["goals_skills"] = goals_sugested_skills

    esco_recommender(title_sugested_skills, desc_sugested_skills, goals_sugested_skills)
    return 0


def esco_recommender(title_skills, desc_skills, goals_skills):
    skills_set = []
    recommendation = []
    newlist = []
    duplist = []

    for i in range(len(title_skills)):
        edit_distance = int(title_skills[i]['distance'])
        if edit_distance < 5:
            recommendation.append([title_skills[i]['skill'], int(title_skills[i]['skill_id']), float(title_skills[i]['score'])])

    print("\n1.-------- check exact title match -------")
    if len(recommendation) > 0:
        print(recommendation)
    else:
        print("No skill match for title name")

    for i in range(len(title_skills)):
        skills_set.append([title_skills[i]['skill'], int(title_skills[i]['skill_id']), float(title_skills[i]['score']), "T"])
        skills_set.append([desc_skills[i]['skill'], int(desc_skills[i]['skill_id']), float(desc_skills[i]['score']), "D"])
        skills_set.append([goals_skills[i]['skill'], int(goals_skills[i]['skill_id']), float(goals_skills[i]['score']), "G"])

    print("\n2.-------- check duplicated skills suggestions  -------")
    for i in range(len(skills_set)):
        id = int(skills_set[i][1])
        if id not in newlist:
            newlist.append(id)
        elif id not in duplist:
            duplist.append(id)
            print("recommended skill_id:", id)
            recommendation.append(skills_set[i])

    print("------------------ recommendation ------------")
    recommendation.sort(key=lambda x: x[2], reverse=True)
    for i in range(len(recommendation)):
        print("{2} \t {1} \t {0}".format(recommendation[i][0], recommendation[i][1], recommendation[i][2]))

    print("\n3.- checking highest scores  -------")
    # do we need linear scores?
    # perc_dist = round(((math.pi - math.acos(float(skills_set[i][2]))) * 100 / math.pi), 4)
    # print(perc_dist)
    skills_set.sort(key=lambda x: x[2], reverse=True)
    for i in range(len(skills_set)):
        print("{2} \t {1} \t {3} \t {0}".format(skills_set[i][0], skills_set[i][1], skills_set[i][2], skills_set[i][3]))
    # print("------------------ sorted by id ------------")
    # skills_set.sort(key=lambda x: x[1], reverse=True)
    # for i in range(len(skills_set)):
    #     print("{2} \t {1} \t {0}".format(skills_set[i][0], skills_set[i][1], skills_set[i][2]))

    # print("------------------ sorted by name ------------")
    # skills_set.sort(key=lambda x: x[0], reverse=False)
    # for i in range(len(skills_set)):
    #     print("{2} \t {1} \t {0}".format(skills_set[i][0], skills_set[i][1], skills_set[i][2]))
    return 0


if __name__ == '__main__':
    from timeit import default_timer as timer
    start = timer()
    ctx = ctx.handler()
    logger = ctx["logger"]

    with open('all_request.txt') as f:
        lines = f.readlines()

    cnt = 0
    for line in lines:
        cnt += 1
        print("-------------------- PROCESSING  --------------------")
        print(str(cnt) + "\t" + line.strip())
        json_data = json.loads(line.strip())
        skill_matcher(ctx, json_data)

    end = timer()
    print("{} seconds".format(round((end - start), 4)))
    # for i in range(0, 100):
    #     d = i /100
    #     perc_dist = round(((math.pi - math.acos(d))  / math.pi), 4)
    #     print(str(d) + "\t" + str(perc_dist))
