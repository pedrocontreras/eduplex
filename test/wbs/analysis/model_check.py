import os
import pickle
import glob

f_list = glob.glob("../../../data/models/*.pkl")

print("{0:>25}\t{1:>8}\t{2:>8}".format("Name", "columns", "rows"))
for i in f_list:
    f = str(i)
    with open(f, "rb") as fIn:
        trained_embedding = pickle.load(fIn)
        base = os.path.basename(f)
        f_name = os.path.splitext(base)[0]
    print("{0:>25}\t{1:>8}\t{2:>8}".format(f_name, trained_embedding.size()[1], trained_embedding.size()[0]))



