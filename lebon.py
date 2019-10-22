from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
sapo = "https://www.leboncoin.fr/recherche/?category=10&locations=Villeurbanne_69100,Lyon&zlat=45.77088&zlng=4.88219&zdefradius=3719"
response = get(sapo, headers=headers)
print(response)
#print(response.text[:1000])
html_soup = BeautifulSoup(response.text, 'html.parser')
house_containers = html_soup.find_all('li', class_="_3DFQ-")
#house_containers = html_soup.find_all('section', class_="_2EDA9")
#prima casa
first = house_containers[1]
#sapte = house_containers[2]
#pw = sapte.find_all('span')[1].text
#print(pw)
#fara poze titlu e pe 1 iar pretul e pe 2
#aici  e 
#p = sapte.find_all('span')[2].text
#print(p)
#pr = sapte.find_all('span')[3].text
#print(pr)
#pt = sapte.find_all('span')[4].text
#print(pt)

#print(first)



title = first.find_all('span')[5].text
print(title)
#price = first.find_all('span')[6].text
#print(price)
data = first.find_all('p')[3].text
print(data)
link = 'https://www.leboncoin.fr/' + first.find_all('a')[0].get('href')[1:-1]
print(link)



titles = []
areas = []
prices = []
urls = []

n_pages = 0

for page in range(0,100):
    n_pages += 1
    sapo_url = 'https://www.leboncoin.fr/recherche/?category=10&locations=Villeurbanne_69100,Lyon&zlat=45.77088&zlng=4.88219&zdefradius=3719&owner_type=private&rooms=min-2&price=500-900&square=25-max'+'&pn='+str(page)
    r = get(sapo_url, headers=headers)
    page_html = BeautifulSoup(r.text, 'html.parser')
    house_containers = html_soup.find_all('li', class_="_3DFQ-")
    if house_containers != []:
        for container in house_containers:
            
            # Price
            price = container.find_all('span')[1].text
            if price == '':
                price = container.find_all('span')[6].text
                if price > 600 and price < 1000:
                    print(price)
                    prices.append(price)
                
            else:
                price = container.find_all('span')[2].text
                if price > 600 and price < 1000:
                    print(price)
                    prices.append(price)         
            
           

           
            # Title
            name = container.find_all('span')[1].text
            if name == '':
                name = container.find_all('span')[5].text
                titles.append(name)
                print(name)
            else:
                name = container.find_all('span')[1].text
                titles.append(name)
                print(name)
            


            # Data
            m2 = container.find_all('p')[3].text
            areas.append(m2)
            
           

            # url
            link = 'https://www.leboncoin.fr/' + container.find_all('a')[0].get('href')[1:-1] + 'l'
            urls.append(link)



    else:
        break
    
    #sleep(randint(1,2))
    
print('You scraped {} pages containing {} properties.'.format(n_pages, len(titles)))


cols = ['Title', 'Price', 'Data', 'URL']

lyon = pd.DataFrame({'Title': titles,
                           'Price': prices,
                           'Data': areas,
                           'URL': urls,})[cols]

lyon.to_excel('lyon.xls')
