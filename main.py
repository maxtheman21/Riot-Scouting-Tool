import requests
import json
from creds import *
cred = cred()
summoner = summoner()
summoner = summoner.split("#")
summonerPUUIDUrl = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner[0]}/{summoner[1]}?api_key={cred}"
PUUID = "".join(list((requests.get(summonerPUUIDUrl)).text.split(",")[0])[10:-1])
print(PUUID)

matchListUrl = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{PUUID}/ids?start=0&count=100&api_key={cred}"
matchList = requests.get(matchListUrl).text
matchList = matchList[1:-1]
matchList = matchList.split(",")

i = matchList[0]
i = i[1: -1]
game = json.loads(requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{i}?api_key={cred}").text)
with open("./test.json", "w", encoding="utf-8") as outfile:
    json.dump(game, outfile, indent=4)
print("LOADING")


#my K/D/A, W/L