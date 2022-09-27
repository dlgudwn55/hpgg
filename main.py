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
    if entry == None:
        return render_template('search.html', user_name=user_name, tier="Unranked", rank="")
    else:
        info = extract_entries(summoner_id)
        if info[0] == "Solo-only":
            solo_tier, solo_rank, solo_wins, solo_losses = info[1:]
            return render_template('search.html', user_name=user_name, solo_tier=solo_tier.title(), solo_rank=solo_rank,
                solo_wins=solo_wins, solo_losses=solo_losses)
        if info[0] == "Team-only":
            team_tier, team_rank, team_wins, team_losses = info[1:]
            return render_template('search.html', user_name=user_name, team_tier=team_tier.title(), team_rank=team_rank,
                team_wins=team_wins, team_losses=team_losses)
        if info[0] == "Both":
            solo_tier, solo_rank, solo_wins, solo_losses, team_tier, team_rank, team_wins, team_losses = info[1:]
            return render_template('search.html', user_name=user_name, solo_tier=solo_tier.title(), solo_rank=solo_rank,
                solo_wins=solo_wins, solo_losses=solo_losses, team_tier=team_tier.title(), team_rank=team_rank,
                team_wins=team_wins, team_losses=team_losses)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)