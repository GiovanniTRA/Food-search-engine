import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib import pylab
from operator import itemgetter

# let's import the inverted index specifically built taking into account rcipes' ingredients 
InverInd_ing = json.load(open('Inverted_index_ing.json', 'r'))

# let's build a dictionary having ingredients as keys and the number of recipes in which they are as values 
more_freq_ing = {}
for i in InverInd_ing.keys():
    more_freq_ing[i] = len(InverInd_ing[i])

# let's sort the new dictionary from the bottom in order to have more frequent ingredients at the beginning 
more_freq_ing = sorted(more_freq_ing.items(), key=itemgetter(1))
more_freq_ing.reverse()

# histogram for more frequent terms 
fig = plt.figure(figsize=(9,6))

freq = [v for k,v in more_freq_ing[:25]]

plt.axis([-1, 26, 0, 8000])
color = [pylab.cm.jet(0.2+i/100) for i in range(len(freq))]

plt.bar(range(len(freq)), freq ,width = 1,  color=color)
plt.xticks([x for x in range(len(freq))], [name.capitalize() for name, freq in more_freq_ing[:25]], size='medium')
fig.autofmt_xdate()
plt.show()

print("The histogram shows the 25 most frequent terms appearing in the specific inverted index built for recipes' ingrediets: as we expected, many of them are either verbs, adverbs or attributes, nevertheless it's very informative as regards most used ingredients in bbc recipes!")    