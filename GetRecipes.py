import requests
from bs4 import BeautifulSoup
import string
import time
import re




g = open('all_links.txt','r',encoding='utf8')

recipes_set = set()
for line in g:
    recipes_set.add(line.strip('\n'))

g.close()


recipes_set = sorted(list(recipes_set))
recipes_set.remove( 'http://www.bbc.co.uk/food/recipes/semolina_and_chilli_36534')
recipes_set.remove( 'http://www.bbc.co.uk/food/recipes/wild_mushroom_risotto_80784')

h = open('final_data.csv','w',encoding='utf8')

h.write('Recipe')
h.write('\t')
h.write('Author')
h.write('\t')
h.write('Preparation Time')
h.write('\t')
h.write('Cooking Time')
h.write('\t')
h.write('Serves')
h.write('\t')
h.write('Diet')
h.write('\t')
h.write('Ingredients')
h.write('\t')
h.write('Method')
h.write('\t')
h.write('Link')
h.write('\n')


itr = 0
for link in recipes_set:
    cnt = requests.get(link)
    while cnt.status_code != 200:
        time.sleep(2)
        cnt = requests.get(link)
    soup = BeautifulSoup(cnt.text, "lxml")


    h.write(soup.title.text.split(" - ")[-1])
    h.write('\t')


    dummy_author = 0
    for tag in soup.find_all(itemprop='author'):
        if len(tag.contents) < 2:
            h.write(tag.contents[0])
            dummy_author += 1
    if dummy_author == 0:
        h.write('No')
    h.write('\t')


    dummy_preptime = 0
    for tag in soup.find_all(itemprop='prepTime'):
        h.write(tag.contents[0])
        dummy_preptime += 1
    if dummy_preptime == 0:
        for p in soup.find_all('p'):
            try:
                if p.get("class")[0] == 'recipe-metadata__prep-time':
                    h.write(p.text)
                    dummy_preptime += 1
            except:
                TypeError
    if dummy_preptime == 0:
        h.write('No')
    h.write('\t')


    dummy_cooktime = 0
    for tag in soup.find_all(itemprop='cookTime'):
        h.write(tag.contents[0])
        dummy_cooktime += 1
    if dummy_cooktime == 0:
        for p in soup.find_all('p'):
            try:
                if p.get("class")[0] == 'recipe-metadata__cook-time':
                    h.write(p.text)
                    dummy_cooktime += 1
            except:
                TypeError
    if dummy_cooktime == 0:
        h.write('No')
    h.write('\t')


    dummy_yield = 0
    for tag in soup.find_all(itemprop='recipeYield'):
        h.write(tag.contents[0])
        dummy_yield += 1
    if dummy_yield == 0:
        h.write('No')
    h.write('\t')



    dummy_veg = 0
    for veg in soup.find_all('a'):
        if veg.get('href') == "/food/diets/vegetarian":
            dummy_veg += 1
    if dummy_veg == 0:
        h.write("No")
    else:
        h.write("Vegetarian")
    h.write('\t')


    dummy_ingredients = 0
    for tag in soup.find_all(itemprop='ingredients'):
        ing = tag.text
        ing = re.sub("\r\n","",ing)
        ing = re.sub("\r","",ing)
        ing = re.sub("\n","",ing)
        ing = re.sub("\t"," ",ing)
        h.write(ing)
        h.write(' ')
        dummy_ingredients += 1
    if dummy_ingredients == 0:
        h.write('No')
    h.write('\t')


    dummy_met = 0
    for tag in soup.find_all(itemprop='recipeInstructions'):
        met = tag.text
        met = re.sub("\r\n","",met)
        met = re.sub("\r","",met)
        met = re.sub("\n","",met)
        met = re.sub("\t"," ",met)
        h.write(met)
        h.write(" ")
        dummy_met += 1
    if dummy_met == 0:
        lst.append('No')
    h.write('\t')


    h.write(link)
    h.write('\n')
    print(itr)
    itr += 1

h.close()
