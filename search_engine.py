import pandas as pd
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import numpy as np
from collections import defaultdict
import json
from scipy import spatial


def prelVectorQuery(df,processed):
    vQ = np.zeros(df.shape[0])
    for i in processed:
        try:
            vQ[df.index.get_loc(i)] += 1
        except:
            KeyError
    return vQ


def vectorQuery(prelVQ, df, InvertedIndex):
    vecQ = prelVQ.copy()
    for i in range(len(vecQ)):
        if vecQ[i] != 0:
            vecQ[i] = (vecQ[i]/sum(vecQ))*(np.log(df.shape[1]/len(InvertedIndex[dataframe.index[i]])))
    return vecQ

def getMatch(processed):
    result = []
    for i in processed:
        try:
            result.extend(InverInd[i])
        except:
            KeyError
    return sorted(list(set(result)))

def getCosSimilarities(vQ, matches, df):
    similarCoeff = []
    for i in matches:
        ### spatial distance cosine computes 1 - the cosine similarity, i.e. the distance
        similarCoeff.append(spatial.distance.cosine(vQ,df.iloc[:,i]))
    return similarCoeff


def returnId_recipe(similarCoeffList, matches, data_table , processedQuery, dummy_veg):
    lst = []
    len_sim = len(similarCoeffList)
    count = 0
    while len(lst) < 5 and (len_sim - count) > 1:
        #Since we have distances, we take the minimum distaneces and set it to max distance
        m = min(similarCoeffList)
        mId = similarCoeffList.index(m)
        ind = matches[mId]
        if dummy_veg == 1:
            if data_table.iloc[ind,5] == "Vegetarian":
                lst.append(data_table.iloc[ind,:])
        else:
            lst.append(data_table.iloc[ind,:])
        similarCoeffList[mId] = 1.1
        count += 1
    return lst


def valid_veg(query_veg):
    dummy_veg = 0
    if query_veg.lower() == "yes":
        dummy_veg = 1
    elif query_veg.lower() == "no":
            dummy_veg = 2
    return dummy_veg

ps = PorterStemmer()
def cleanQuery(stop,measure,query):
    processQuery = []
    ps = PorterStemmer()
    for char in query:
        if char in '“<>”/?;:,."\'’‘[]{}|=+-_()*&^%$#@!`~\\\t\n\r–¼½¾⅛⅓⅔⅙⅝⅜—°…⁄£' or char.isdigit():
                query = query.replace(char, ' ')

    for i in query.split():
        i = ps.stem(i)
        if i not in stop and i not in measure:
            processQuery.append(i.lower())
    return processQuery

dataframe = pd.read_csv('dataframe.csv',delimiter = '\t',index_col = 0)
newDf = pd.read_csv('newDf.csv',delimiter = '\t', index_col = 0)
data_table = pd.read_csv('data_table.csv',delimiter = '\t',index_col = 0)
InverInd = json.load(open('Inverted_index.json','r'))
D = json.load(open('D_dict_json.txt','r'))


stop = get_stop_words('english')
measure = set(['ml', 'fl', 'oz', 'c', 'f', 'g', 't','kg', 'lb', 'tbsp', 'tsp','pt'])


def search_engine():
    query = input("Please insert your query: ")

    while not getMatch(cleanQuery(stop,measure,query)):
        query = input("Insert a valid query: ")

    query_veg = input("Are you vegetarian? (yes or no): " )

    while not valid_veg(query_veg):
        query_veg = input("Please just type 'yes' or 'no' ")
    dummy_veg = valid_veg(query_veg)
    processQuery = cleanQuery(stop,measure,query)
    matches = getMatch(processQuery)
    vecQ = prelVectorQuery(dataframe, processQuery)
    vecQuery = vectorQuery(vecQ, dataframe, InverInd)
    similarities = getCosSimilarities(vecQuery, matches, newDf)
    print(returnId_recipe(similarities, matches, data_table ,processQuery,dummy_veg))

search_engine()
