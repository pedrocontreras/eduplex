from numpy import loadtxt


def load_array(f_in, d_type):
    data = loadtxt(f_in, dtype=d_type)
    data = data[:, 1:]  # remove first column that contains query index
    return data


def compare_array(array_a, array_b):
    r, c = array_a.shape
    cnt = 0
    mtc_acc = 0
    for i in range(r):
        cnt += 1
        print(cnt, end="\t")
        row_a = array_a[i]
        row_b = array_b[i]
        dict_row_b = dict(enumerate(row_b.flatten(), 1))
        dict_values = dict_row_b.values()

        cnt_match = 0
        for x in row_a:
            if x in dict_values:
                cnt_match += 1
                print("{:>8}".format(x), end="\t")

        mtc = (cnt_match/c)*100
        print("{:>8}%".format(mtc), "\r")
        mtc_acc = mtc_acc + mtc

    print("Avg {:>8}%".format(mtc_acc/r))  # average matching percentage
    return 0


if __name__ == "__main__":
    # files contains the text uses for the queries, always the query is one string, but we can cocatenate it
    f_titles = "matches_minilm/titles.csv"
    f_desc = "matches_minilm/desc.csv"
    f_goals = "matches_minilm/goals.csv"
    f_title_desc = "matches_minilm/title-desc.csv"
    f_title_goals = "matches_minilm/title-goals.csv"
    f_desc_goals = "matches_minilm/desc-goals.csv"
    f_goals_desc = "matches_minilm/goals-desc.csv"
    f_title_desc_goals = "matches_minilm/title-desc-goals.csv"

    arr_title = load_array(f_titles, "int")
    arr_desc = load_array(f_desc, "int")
    arr_goals = load_array(f_goals, "int")
    arr_title_desc = load_array(f_title_desc, "int")
    arr_title_goals = load_array(f_title_goals, "int")
    arr_desc_goals = load_array(f_desc_goals, "int")
    arr_goal_desc = load_array(f_goals_desc, "int")
    arr_title_desc_goals = load_array(f_title_desc_goals, "int")

    # this is for the all-mpnet-base-v2 LLM
    f_desc_bge_large = "matches_bge_large/desc.csv"
    f_goals_bge_large = "matches_bge_large/goals.csv"
    f_desc_goals_bge_larget = "matches_bge_large/desc-goals.csv"

    arr_desc_bge_large = load_array(f_desc_bge_large, "int")
    arr_goals_bge_large = load_array(f_goals_bge_large, "int")
    arr_desc_goals_bge_large = load_array(f_desc_goals_bge_larget, "int")

    f_goals_mpnet = "matches_mpnet/goals.csv"
    arr_goals_mpnet = load_array(f_goals_mpnet, "int")
    f_desc_mpnet = "matches_mpnet/desc.csv"
    arr_desc_mpnet = load_array(f_desc_mpnet, "int")

    f_desc_gte = "matches_gte-large/desc.csv"
    arr_desc_gte = load_array(f_desc_gte, "int")
    f_goals_gte = "matches_gte-large/goals.csv"
    arr_goals_gte = load_array(f_goals_gte, "int")
    f_desc_goals_gte = "matches_gte-large/desc-goals.csv"
    arr_desc_goals_gte = load_array(f_desc_goals_gte, "int")

    f_desc_marco = "matches_msmarco/desc.csv"
    arr_desc_marco = load_array(f_desc_marco, "int")
    f_goals_marco = "matches_msmarco/goals.csv"
    arr_goals_marco = load_array(f_goals_marco, "int")
    f_desc_goals_marco = "matches_msmarco/desc-goals.csv"
    arr_desc_goals_marco = load_array(f_desc_goals_marco, "int")

    f_desc_e5_large = "matches_e5_large/desc.csv"
    arr_desc_e5_large = load_array(f_desc_e5_large, "int")
    f_goals_e5_large = "matches_e5_large/goals.csv"
    arr_goals_e5_large = load_array(f_goals_e5_large, "int")
    f_desc_goals_e5_large = "matches_e5_large/desc-goals.csv"
    arr_desc_goals_e5_large = load_array(f_desc_goals_e5_large, "int")

    # f_desc_e5_large_xxl = "matches_e5_large_xxl/desc.csv"
    # arr_desc_e5_large_xxl = load_array(f_desc_e5_large_xxl, "int")
    # f_goals_e5_large_xxl = "matches_e5_large_xxl/goals.csv"
    # arr_goals_e5_large_xxl = load_array(f_goals_e5_large_xxl, "int")
    # f_desc_goals_e5_large_xxl = "matches_e5_large/desc-goals.csv"
    # arr_desc_goals_e5_larg_xxl = load_array(f_desc_goals_e5_large_xxl, "int")

    # print("--------------- arr_desc_gte Matching Description vs Learning Goals------------------------")
    # compare_array(arr_desc_gte, f_goals_gte)
    # print("--------------- arr_desc_gte Matching Description vs Descriptions & Learning Goals----------------------")
    # compare_array(arr_desc_e5_large, arr_desc_goals_e5_large)
    # print("--------------- arr_desc_gte Matching Learning Goals vs Descriptions & Learning Goals-------------------")
    # compare_array(arr_goals_e5_large, arr_desc_goals_e5_large)

    # print("--------------- marco Matching Description vs Learning Goals------------------------")
    # compare_array(arr_desc_marco, arr_goals_marco)
    # print("--------------- marco Matching Description vs Descriptions & Learning Goals------------------------")
    # compare_array(arr_desc_marco, arr_desc_goals_marco)
    # print("--------------- marco Matching Learning Goals vs Descriptions & Learning Goals------------------------")
    # compare_array(arr_goals_marco, arr_desc_goals_marco)

    # this pair-wise comparition check how overpose the two result set are
    print("---------------Matching Titles vs Descriptions------------------------")
    compare_array(arr_title, arr_desc)
    print("---------------Matching Titles vs Learning Goals------------------------")
    compare_array(arr_title, arr_goals)
    print("---------------Matching Description vs Learning Goals------------------------")
    compare_array(arr_desc, arr_goals)
    print("---------------Matching Description vs Descriptions & Learning Goals------------------------")
    compare_array(arr_desc, arr_desc_goals)
    print("---------------Matching Learning Goals vs Descriptions & Learning Goals------------------------")
    compare_array(arr_goals, arr_desc_goals)
    print("---------------Matching Titles vs [Title + Description + Learning Goal]------------------------")
    compare_array(arr_title, arr_title_desc_goals)
    print("---------------Matching Description vs [Title + Description + Learning Goal]------------------------")
    compare_array(arr_desc, arr_title_desc_goals)
    print("---------------Matching Learning Goals vs [Title + Description + Learning Goal]------------------------")
    compare_array(arr_goals, arr_title_desc_goals)
    print("---------------CONTROL------------------------")
    compare_array(arr_goal_desc, arr_goal_desc)

    # print("--------------- mpnet Matching Description vs Learning Goals------------------------")
    # compare_array(arr_desc_mpnet, arr_goals_mpnet)
    # print("--------------- mpnetMatching Description vs Descriptions & Learning Goals------------------------")
    # compare_array(arr_desc_mpnet, arr_desc_goals_mpnet)
    # print("--------------- mpnet Matching Learning Goals vs Descriptions & Learning Goals------------------------")
    # compare_array(arr_goals_mpnet, arr_desc_goals_mpnet)
    # print("--------------- all-mpnet-base-v2 vs bge-large-en-v1.5 desc------------------------")
    # compare_array(arr_desc_bge_large, arr_desc_mpnet)
    # print("--------------- all-mpnet-base-v2 vs bge-large-en-v1.5 goal------------------------")
    # compare_array(arr_goals_bge_large, arr_goals_mpnet)
