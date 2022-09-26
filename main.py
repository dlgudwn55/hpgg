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
        tier, rank, wins, losses = extract_entries(summoner_id)
        tier = tier.title()
        return render_template('search.html', user_name=user_name, tier=tier, rank=rank)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)