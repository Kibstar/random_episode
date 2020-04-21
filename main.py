import json, requests, os, bs4, re, random, webbrowser, sys

url = 'https://en.wikipedia.org/wiki/List_of_Friends_episodes'
headers = {'Accept-Language': 'en-UK,en;q=0.8'}

title = sys.argv[1]

class Episode:

    netflix_url = 'https://www.netflix.com/watch/'

    def __init__(self,number,episode,date,title,score):
        self.title = title
        self.episode = episode # episode number in that season i.e ep.12
        self.number = number # overall episode number i.e ep.134
        self.date = date

        self.score = score

    def add_score(self):
        self.score += self.not_played_score

    def minus_score(self):
        self.score = 0

    def reset_score(self):
        self.score = self.base_score

    def chance_func(self,episode_list):
        total_score = 0
        for i in episode_list:
            total_score += int(i.score)

        self.chance = round((self.score / total_score) * 100, 2)

class Friends(Episode):

    id = 70273996

    base_score = 100
    not_played_score = 1

    def __init__(self, number,episode,date,title,score):
        self. netflix_id = (self.id + int(number))
        self. link = f'{self.netflix_url}{self.netflix_id}'
        super(Friends, self).__init__(number,episode,date,title,score)

    def __str__(self):
        return(f'Friends:\n'
               f'{self.title}\n'
               f'Episode: {self.number}\n')

class BlackMirror(Episode):

    id = 70264856

    base_score = 20
    not_played_score = 1

    def __init__(self, number,episode,date,title,score,link):
        self. link = link
        super(BlackMirror, self).__init__(number,episode,date,title,score)


    def __str__(self):
        return(f'Black Mirror:\n'
               f'{self.title}\n'
               f'Episode: {self.number}\n')

def saveJSON(list,title):
    data = []
    for i in list:
        d = i.__dict__
        data.append(d)

    with open(f'{title}.json','w') as f:
        json.dump(data,f,indent=2)


def importJSON(title):
    episode_list = []
    with open(f'{title}.json','r') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            print('Empty file')
            return
    if title == 'friends':
        for i in data:
            f = Friends(title=i['title'],
                        episode=i['episode'],
                        number=i['number'],
                        date=i['date'],
                        score=i['score'],
                        )
            episode_list.append(f)
    elif title == 'blackmirror':
        for i in data:
            f = BlackMirror(title=i['title'],
                        episode=i['episode'],
                        number=i['number'],
                        date=i['date'],
                        score=i['score'],
                        link=i['link'],

                        )
            episode_list.append(f)
    return episode_list


list = importJSON(title)

if __name__ == '__main__':
    list = importJSON(title)
    for i in list:
        i.chance_func(list)
    chance_pot = []
    for y in list:
        for j in range(int(y.chance * 100)):
            chance_pot.append(str(y.number))
    while True:
        pot_pull = random.choice(chance_pot)
        for i in list:
            if i.number == pot_pull:
                choice = i
        print(choice)
        print('Do you want to watch this episode? Y or N?')
        i = input()
        if i.upper() == 'N':
            command = 'clear'
            os.system(command)
            continue
        elif i.upper() == 'Y':
            webbrowser.open(choice.link, new=2)
            choice.minus_score()
            print(choice.score)
            for x in list:
                if x.number != choice.number:
                    x.add_score()
            saveJSON(list,title)
            break




