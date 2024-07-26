import pandas as pd

fi = "dat/matching_desc_agaist_title_10.tsv"

df = pd.read_csv(fi, sep='\t', header=0)

res = df.iloc[::, :1]
arr = res.to_numpy()
num_data = len(arr)

top_1 = 0
top_2 = 0
top_3 = 0
top_4 = 0
top_5 = 0
top_6 = 0
top_7 = 0
top_8 = 0
top_9 = 0
top_10 = 0
no_match = 0

for i in range(0, len(arr), 11):
    # print("{0} {1}".format(i, arr[i]))

    if i >= 0:
        print(int(i/11)+1)

    if i > (len(arr)-2):
        break

    if arr[i] == arr[i+1]:
        top_1 = top_1 + 1
        print("\ttop_1")
    elif arr[i] == arr[i+2]:
        top_2 = top_2 + 1
        print("\ttop_2")
    elif arr[i] == arr[i+3]:
        top_3 = top_3 + 1
        print("\ttop_3")
    elif arr[i] == arr[i+4]:
        top_4 = top_4 + 1
        print("\ttop_4")
    elif arr[i] == arr[i+5]:
        top_5 = top_5 + 1
        print("\ttop_5")
    elif arr[i] == arr[i+6]:
        top_6 = top_6 + 1
        print("\ttop_6")
    elif arr[i] == arr[i+7]:
        top_7 = top_7 + 1
        print("\ttop_7")
    elif arr[i] == arr[i+8]:
        top_8 = top_8 + 1
        print("\ttop_8")
    elif arr[i] == arr[i+9]:
        top_9 = top_9 + 1
        print("\ttop_9")
    elif arr[i] == arr[i+10]:
        top_10 = top_10 + 1
        print("\ttop_10")
    else:
        no_match = no_match + 1
        print("\tNONE")

    i = i + 10

print("RESULTS")
print("top 1: ", top_1)
print("top 2: ", top_2)
print("top 3: ", top_3)
print("top 4: ", top_4)
print("top 5: ", top_5)
print("top 6: ", top_6)
print("top 7: ", top_7)
print("top 8: ", top_8)
print("top 9: ", top_9)
print("top 10: ", top_10)
print("no_match: ", no_match)
