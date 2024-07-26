import csv


def read_file(fn):

    with open(fn, 'r') as file:
        f_list = []
        reader = csv.reader(file, delimiter='|')
        for r in reader:
            f_list.append(r)
    return f_list


def clean_query(q):
    q = q.replace("/", " ")
    q = q.replace("\\", " ")
    q = q.replace("//", " ")
    q = q.replace("-", " ")
    return q


if __name__ == '__main__':
    l_fi = read_file("request.csv")
    base_url = 'http://127.0.0.1:5000/sbert_desc_de_analysis/'
    import requests as req
    cnt = 0
    for row in l_fi:
        cnt += 1
        id = clean_query(str(row[0]))
        query = clean_query(str(row[1]))

        print("{0} {1}".format(id, query))
        if query is not None or query != "":
            resp = req.get(base_url+str(row[1]))
            print('\t' + resp.text)  # Printing response
        else:
            print("Empty query")
