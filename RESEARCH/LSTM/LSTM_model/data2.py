import pandas as pd
import string

with open('testSet-qualifiedBatch-fixed.txt', 'r', encoding='utf-8') as txt_file:
    data = txt_file.read()

data = data.splitlines()

data_classify = {'yes' : [1, 0], 'no' : [0, 1]}

final_dataset = []

for i in range(len(data)):
    data[i] = data[i].split('\t')
    data[i][1] = out = "".join(c for c in data[i][1] if c not in ('!','.',':', '>', '$', '?', '[', ']'))
    # print(data[i][0].lower())
    final_dataset.append([str(data[i][1]).lower(), data_classify[str(data[i][0]).lower()][0], data_classify[str(data[i][0]).lower()][1]])

df = pd.DataFrame(final_dataset, columns=['sentence', 'yes','no'])

df.to_csv('testing.csv', index = False, encoding='utf-8')