from flask import Flask, render_template, request, redirect
from requests import get
from search import *
from PIL import Image

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    user_name = request.args.get('user-name')
    if user_name == None:
        return redirect('/')
    summoner_id = extract_id(user_name)
    entry = extract_entries(summoner_id)
    matche_ids = extract_matches(user_name)
    matches = []
    for match_id in matche_ids:
        matches.append(extract_match_info(match_id))
        
    my_idxs = []
    for match in matches:
        for participant in match["info"]["participants"]:
            if participant["summonerName"] == user_name:
                my_idxs.append(participant["participantId"]-1)
    
    match_data = []
    for match in matches:
        match_data.append({"mode": match["info"]["gameMode"], "gameDuration": match["info"]["gameDuration"]})
    for i in range(len(my_idxs)):
        match_data[i]["champion"] = matches[i]["info"]["participants"][my_idxs[i]]["championName"]
        match_data[i]["kills"] = matches[i]["info"]["participants"][my_idxs[i]]["kills"]
        match_data[i]["deaths"] = matches[i]["info"]["participants"][my_idxs[i]]["deaths"]
        match_data[i]["assists"] = matches[i]["info"]["participants"][my_idxs[i]]["assists"]
        # match_data[i]["win"] = matches[i]["info"]["participants"][my_idxs[i]]["win"]
        if matches[i]["info"]["participants"][my_idxs[i]]["win"]:
            match_data[i]["wl"] = "Win"
        else:
            match_data[i]["wl"] = "Loss"
        
    if entry == None:
        return render_template('search.html', user_name=user_name, tier="Unranked", rank="", match_data=match_data)
    else:
        info = extract_entries(summoner_id)
        if info[0] == "Solo-only":
            solo_tier, solo_rank, solo_wins, solo_losses = info[1:]
            return render_template('search.html', user_name=user_name, solo_tier=solo_tier.title(), solo_rank=solo_rank,
                solo_wins=solo_wins, solo_losses=solo_losses, match_data=match_data)
        if info[0] == "Team-only":
            team_tier, team_rank, team_wins, team_losses = info[1:]
            return render_template('search.html', user_name=user_name, team_tier=team_tier.title(), team_rank=team_rank,
                team_wins=team_wins, team_losses=team_losses, match_data=match_data)
        if info[0] == "Both":
            solo_tier, solo_rank, solo_wins, solo_losses, team_tier, team_rank, team_wins, team_losses = info[1:]
            return render_template('search.html', user_name=user_name, solo_tier=solo_tier.title(), solo_rank=solo_rank,
                solo_wins=solo_wins, solo_losses=solo_losses, team_tier=team_tier.title(), team_rank=team_rank,
                team_wins=team_wins, team_losses=team_losses, match_data=match_data)
            
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)