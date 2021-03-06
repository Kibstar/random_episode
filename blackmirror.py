from main import BlackMirror,saveJSON
import bs4, requests, os, random, webbrowser

url = 'https://en.wikipedia.org/wiki/List_of_Black_Mirror_episodes'
headers = {'Accept-Language': 'en-UK,en;q=0.8'}

def bm_episode_finder(url):
    episode_list =[]
    res = requests.get(url,headers=headers)

    try:
        res.raise_for_status()
    except:
        return('The page could not be loaded')

    soup = bs4.BeautifulSoup(res.text,'html.parser')

    div = soup.find('div',{'class': 'mw-parser-output'})

    rows = div.find_all('tr',{'class':'vevent'})
    counter = 1
    for i in range(len(rows)):

        number = rows[i].contents[0].text
        title = rows[i].contents[2].text
        episode = rows[i].contents[1].text

        try:
            date = rows[i].contents[5].text
        except:
            date = ''

        if len(rows[i - 1].contents[0].text) > 1 and len(number) / 2 == len(rows[i - 1].contents[0].text):
            number = counter
            f = BlackMirror(number+1,episode,date,title,BlackMirror.base_score)
            episode_list.append(f)
            counter += 1
        if title[0] == '"':
            f = BlackMirror(number,episode,date,title,BlackMirror.base_score)
            episode_list.append(f)
            counter += 1
    return episode_list

list = bm_episode_finder(url)

title = 'blackmirror'

for i in list:
    print(i)

