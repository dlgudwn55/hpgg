from requests import get
API_KEY = 'RGAPI-9870331e-9b22-4188-aa41-da34ca274d37'

def extract_id(summoner_name):
    base_url = 'https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
    response = get(f"{base_url}{summoner_name}", headers={"X-Riot-Token": API_KEY})
    return response.json()["id"]

def extract_entries(summoner_id):
    base_url = 'https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/'
    response = get(f"{base_url}{summoner_id}", headers={"X-Riot-Token": API_KEY})
    if response.json() == []:
        return None
    response_json = response.json()
    
    if len(response_json) == 1:
        if response_json[0]['queueType'] == 'RANKED_SOLO_5x5':
            return ["Solo-only", response_json[0]['tier'], response_json[0]['rank'], response_json[0]['wins'], response_json[0]['losses']]
        if response_json[0]['queueType'] == 'RANKED_TEAM_5x5':
            return ["Team-only", response_json[0]['tier'], response_json[0]['rank'], response_json[0]['wins'], response_json[0]['losses']]
    
    if len(response_json) == 2:
        ["Both", response_json[0]['tier'], response_json[0]['rank'], response_json[0]['wins'], response_json[0]['losses'],
        response_json[1]['tier'], response_json[1]['rank'], response_json[1]['wins'], response_json[1]['losses']]