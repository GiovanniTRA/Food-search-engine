import requests
from bs4 import BeautifulSoup
import string
import time
import re

f = open('all_links.txt','w')


for letter in string.ascii_lowercase:
    cnt = requests.get("http://www.bbc.co.uk/food/ingredients/by/letter/"+letter)
    while cnt.status_code != 200:
        time.sleep(2)
        cnt = requests.get("http://www.bbc.co.uk/food/ingredients/by/letter/"+letter)
    soup = BeautifulSoup(cnt.text, "lxml")
    print(soup.title)

    for ol in soup.find_all("ol"):
        if ol.get("id") == "foods-by-letter":
            for link in ol.find_all('a'):
                element = link.get('href').split('/')[-1]
                element = re.sub(r"\_","%20", element)
                if "related" not in element:
                    print("-----",element)
                    cnt2 = requests.get("http://www.bbc.co.uk/food/recipes/search?keywords="+element)
                    while cnt2.status_code != 200:
                        time.sleep(2)
                        cnt2 = requests.get("http://www.bbc.co.uk/food/recipes/search?keywords="+element)
                    soup2 = BeautifulSoup(cnt2.text, "lxml")
                    max_lst = []
                    for link in soup2.find_all('a'):
                        if (link.get('href').startswith("/food/recipes/") and len(link.get('href')) > len("/food/recipes/") and "search" in link.get('href')):
                            if link.contents[-1] != "Next" and link.contents[-1] != "Previous":
                                max_lst.append(link.contents[-1])
                    if max_lst:
                        max_page = max(max_lst)
                        for link in soup2.find_all('a'):
                            if (link.get('href').startswith("/food/recipes/") and len(link.get('href')) > len("/food/recipes/") and "search" not in link.get('href')):
                                recipes_links = link.get('href')
                                if recipes_links:
                                    f.write('http://www.bbc.co.uk')
                                    f.write(recipes_links)
                                    f.write('\n')

                        for i in range(2,int(max_page) + 1):
                            cnt4 = requests.get("http://www.bbc.co.uk/food/recipes/search?page="+str(i)+"&keywords="+element)
                            while cnt4.status_code != 200:
                                time.sleep(2)
                                cnt4 = requests.get("http://www.bbc.co.uk/food/recipes/search?page="+str(i)+"&keywords="+element)
                            soup4 = BeautifulSoup(cnt4.text, "lxml")
                            for link in soup4.find_all('a'):
                                if (link.get('href').startswith("/food/recipes/") and len(link.get('href')) > len("/food/recipes/") and "search" not in link.get('href')):
                                    recipes_links = link.get('href')
                                    if recipes_links:
                                        f.write('http://www.bbc.co.uk')
                                        f.write(recipes_links)
                                        f.write('\n')
                    else:
                        for link in soup2.find_all('a'):
                            if (link.get('href').startswith("/food/recipes/") and len(link.get('href')) > len("/food/recipes/") and "search" not in link.get('href')):
                                recipes_links = link.get('href')
                                if recipes_links:
                                    f.write('http://www.bbc.co.uk')
                                    f.write(recipes_links)
                                    f.write('\n')



f.close()
