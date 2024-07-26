import numpy as np
import requests
from test.wbs.wbs_matcher import get_semantic_title, get_semantic_description, get_semantic_goal


def sanitise(s):
    s = s.replace("\'", "")
    s = s.replace("`", "")
    s = s.replace("//", "")
    s = s.replace("\"", "")
    s = s.replace("“", "")
    s = s.replace("”", "")
    s = s.replace("\"", "")
    return s


def match_course_skills_request(data):
    url = "http://localhost:5000/match_course_skills/"
    print(data)
    try:
        response = requests.get(url, data=data, headers={"Content-Type": "application/json"})
        print(response.json())
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    print("-------------------------------------")


if __name__ == "__main__":
    query_file = "../dat/wbs_courses_en.xlsx"
    title = get_semantic_title(query_file)
    desc = get_semantic_description(query_file)
    goals = get_semantic_goal(query_file)
    arr = np.concatenate((title, desc, goals), axis=1)

    for i in arr:
        t = sanitise(str(i[0]))
        d = sanitise(str(i[1]))
        g = sanitise(str(i[2]))
        q = "{{\"language\": \"en\", \"title\":\"{0}\", \"description\": \"{1}\", \"learning_goals\": \"{2}\"}}".format(
            t, d, g)

        match_course_skills_request(q)

