import requests
import json
from creds import *


def search(summoner):
    cred = cred()
    lst = []
    summonertag = summoner.split("#")
    queue = 420 #440 = flex
    PUUID = "".join(list((requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summonertag[0]}/{summonertag[1]}?api_key={cred}")).text.split(",")[0])[10:-1])
    matchList = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{PUUID}/ids?queue={queue}&start=0&count=1&api_key={cred}").text[1:-1].split(",")
    for i in matchList:
        i = i[1: -1]
                
        game = json.loads(requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{i}?api_key={cred}").text)
        
        players = game['metadata']['participants']
        i = 0
        while p != i:
            i += 1
            if players[i] == PUUID:
                p = i
            
        info = game['info']['participants']

        champion = info[p]['championId']
        kills = info[p]['kills']
        deaths = info[p]['deaths']
        assists = info[p]['assists']
        
        if info[p]['win']:
            win = "Victory"
        else:
            win = "Defeat"
        
        if deaths:
            print(f"{champion}: {kills,deaths,assists} ({(kills+assists)/deaths}) {win}")
        else:
            print(f"{champion}: {kills,deaths,assists} (PERFECT) {win}")
    return False