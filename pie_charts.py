import pandas as pd
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
import numpy as np
from collections import defaultdict
import json
import matplotlib.pyplot as plt

data_table = pd.read_csv('data_table.csv',delimiter = '\t',index_col = 0)
dataframe = pd.read_csv('dataframe.csv',delimiter = '\t',index_col=0)
InverInd = json.load(open('Inverted_index.json','r'))
InverInd_ing = json.load(open('Inverted_index_ing.json','r'))
dataframe_ing = pd.read_csv('dataframe_ing.csv',delimiter = '\t',index_col=0)




ps = PorterStemmer()
def cleanIngredients(ing):
    ps = PorterStemmer()
    for char in ing:
        if char in '“<>”/?;:,."\'’‘[]{}|=+-_()*&^%$#@!`~\\\t\n\r–¼½¾⅛' or char.isdigit():
                ing = ing.replace(char, ' ')
    ing = ps.stem(ing)
    ing = ing.lower()
    return ing

def valid_search(query,ix = InverInd_ing):
    dummy = 0
    try:
        a = ix[cleanIngredients(query)]
        if a:
            dummy = 1
    except:
        KeyError
    return dummy


def plot_charts(df = dataframe,ix = InverInd_ing):
    c = input("Please type the name of an ingredient: ")
    while not valid_search(c):
        c = input("Please insert a valid ingredient: ")
    d = input("Please type the name of an other ingredient: ")
    while not valid_search(d):
        d = input("Please insert a valid ingredient: ")
    a = cleanIngredients(c)
    b = cleanIngredients(d)
    omega = df.shape[1]
    a_set = set(ix[a])
    b_set = set(ix[b])
    if a_set and b_set:
        ab_intersection = a_set.intersection(b_set)


    p_a = len(a_set) / omega *100

    print("I chart: The percentage of recipes containing "+c+" over all recipes is: " +str(p_a))
    
    plt.figure(1,figsize=(6,6))
    ax = plt.axes([0.1 , 0.1 , 0.8 , 0.8])
    labels = c.capitalize(), "Not "+c
    ratios = [len(a_set) / omega *100,(1 - len(a_set) / omega) *100]
    explode = (0.1,0)
    plt.pie(ratios,explode=explode,labels = labels, autopct = "%1.1f%%",shadow = True, startangle=270)
    plt.title("Prevalence of "+c+" in recipes")
    plt.show()

    

    p_b = len(b_set) / omega * 100
    p_inter = len(ab_intersection) / omega * 100
    p_not = (p_a - p_inter)
    p_neither = (1 - len(a_set) / omega) *100

    print("II chart: The percentage of recipes containing both ingredients over all recipes is: ", p_inter)
    print("If the ingredients are often used together, I will not have a significant reduction w.r.t the first chart, (see red slice).")
    print("Viceversa, the opposite will be true.")


    plt.figure(1,figsize=(6,6))
    ax = plt.axes([0.1 , 0.1 , 0.8 , 0.8])
    labels = c.capitalize()+" and "+d.capitalize(),"Percentage decrease w.r.t. the first graph" ,"Not "+c+" and "+d
    ratios = [p_inter,p_not,p_neither]
    explode = (0.05,0.1,0)
    plt.pie(ratios,explode=explode,labels = labels, autopct = "%1.1f%%",shadow = True, startangle=270, colors=["b","r","g"])
    plt.title("Prevalence of "+c+" and "+d+" in recipes")
    plt.show()

    p_a_b = (p_inter/p_b)*100
    variation = p_a_b-p_a
    if variation >= 0  :
        print("Having ingredient "+d+" in your recipe, increases the probability of having ingredient "+c,"by",variation,"percent")
    else:
        print("Having ingredient "+d+" in your recipe, decreases the probability of having ingredient "+c,"by",variation,"percent")
    print("("+str(p_a_b)+")% chance")

    plt.figure(1,figsize=(6,6))
    ax = plt.axes([0.1 , 0.1 , 0.8 , 0.8])
    labels = c+" in "+d, "not "+c+" in "+d
    ratios = [p_inter/p_b , 1-(p_inter/p_b)]
    explode = (0.05,0.1)
    plt.pie(ratios,explode=explode,labels = labels, autopct = "%1.1f%%",shadow = True, startangle=270, colors=["b","g"])
    plt.title("Recipes with "+d)
    plt.show()

plot_charts()
