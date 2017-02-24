import pandas as pd
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import numpy as np
from collections import defaultdict
import json

def tf(datafra, x, y):
    #take the absolute frequencies
    return datafra.loc[x, y]

def idf(word, InvertedIndex, datafra):
    return np.log(datafra.shape[1]/len(InvertedIndex[word]))



data_table = pd.read_csv('final_data.csv', delimiter = '\t')

D = {}
x = 0

stop = get_stop_words('english')
measure = set(['ml', 'fl', 'oz', 'c', 'f', 'g', 't','kg', 'lb', 'tbsp', 'tsp'])

ps = PorterStemmer()

for line in data_table[['Recipe', 'Author', 'Diet', 'Ingredients', 'Method']].values:
    doc = ' '.join(line)
    for char in doc:
        if char in '“<>”/?;:,."\'’‘[]{}|=+-_()*&^%$#@!`~\\\t\n\r–¼½¾⅛⅓⅔⅙⅝⅜—°…⁄£' or char.isdigit():
            doc = doc.replace(char, ' ')
    doc = (doc.lower()).split()

    for i in doc:
        if i in stop or i in measure:
            doc = doc[:doc.index(i)]+doc[(doc.index(i)+1):]
    doc = [ps.stem(word) for word in doc]
    D[x] = doc
    x += 1


word = []
doc = [x for x in range(data_table.shape[0])]

dataframe = pd.DataFrame(index=word, columns = doc)

for k in D.keys():
    for w in D[k]:
        if w not in dataframe.index:
            dataframe.loc[w] = np.zeros(len(doc))
            dataframe.loc[w,k] = 1
        else:
            dataframe.loc[w,k] +=1


InverInd = defaultdict(list)

for row in dataframe.index:
    for col in dataframe.columns:
        if dataframe.loc[row,col] != 0:
            InverInd[row].append(col)

newDf = dataframe.copy()

for i in newDf.index:
    for j in newDf.columns:
        if newDf.loc[i,j] != 0:
            tF = tf(dataframe, i, j)
            iDf = idf(i, InverInd, dataframe)
            newDf.loc[i,j] = tF*iDf

D_ing = {}
x = 0

stop = get_stop_words('english')
measure = set(['ml', 'fl', 'oz', 'c', 'f', 'g', 't','kg', 'lb', 'tbsp', 'tsp'])

ps = PorterStemmer()

for line in data_table[['Ingredients']].values:
    doc = ' '.join(line)
    for char in doc:
        if char in '“<>”/?;:,."\'’‘[]{}|=+-_()*&^%$#@!`~\\\t\n\r–¼½¾⅛⅓⅔⅙⅝⅜—°…⁄£' or char.isdigit():
            doc = doc.replace(char, ' ')
    doc = (doc.lower()).split()

    for i in doc:
        if i in stop or i in measure:
            doc = doc[:doc.index(i)]+doc[(doc.index(i)+1):]
    doc = [ps.stem(word) for word in doc]
    D_ing[x] = doc
    x += 1



word = []
doc = [x for x in range(data_table.shape[0])]

dataframe_ing = pd.DataFrame(index=word, columns = doc)

for k in D_ing.keys():
    for w in D_ing[k]:
        if w not in dataframe_ing.index:
            dataframe_ing.loc[w] = np.zeros(len(doc))
            dataframe_ing.loc[w,k] = 1
        else:
            dataframe_ing.loc[w,k] +=1

InverInd_ing = defaultdict(list)

for row in dataframe_ing.index:
    for col in dataframe_ing.columns:
        if dataframe_ing.loc[row,col] != 0:
            InverInd_ing[row].append(col)


### Dictionary key:docs, values : bag of words
json.dump(D,open('D_dict_json.txt','w'))
json.dump(D_ing,open('D_ing_dict_json.txt','w'))


InverInd_final = pd.Series(InverInd)
InverInd_final.to_json('Inverted_index.json')

InverInd_final_ing = pd.Series(InverInd_ing)
InverInd_final_ing.to_json('Inverted_index_ing.json')

data_table.to_csv('data_table.csv', sep='\t')
dataframe.to_csv('dataframe.csv', sep='\t')
newDf.to_csv('newDf.csv', sep='\t')
dataframe_ing.to_csv('dataframe_ing.csv', sep='\t')
