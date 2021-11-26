from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_migrate import Migrate
from datetime import datetime
from random import randint

import snscrape.modules.twitter as sntwitter
import json




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.debug = True

class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable = False)
    polarity = db.Column(db.Float)
    subjectivity = db.Column(db.Float)

    def __repr__(self):
        return '<Tweet %r>' % self.content



@app.route('/', methods=['POST', 'GET'])
def index():
    tweets = Tweets.query.all()
    num = randint(0, len(tweets))
    tweet = tweets[num]
    if request.method == 'POST':
        keyword = request.form['content']
        search_item = Search(content=keyword)

        try:
            db.session.add(search_item)
            db.session.commit()
            return redirect('/search')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Search.query.order_by(desc(Search.date_created)).all()
        return render_template('index.html', tasks=tasks[1:10], tweet = tweet)

    

@app.route('/delete/<int:id>')
def delete(id):
    searches_to_delete = Search.query.get_or_404(id)

    try:
        db.session.delete(searches_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that item'

@app.route('/general_stats')
def general_stats():
    tweets=Tweets.query.all()


@app.route('/search')
def search():
    search_item = Search.query.order_by(Search.id.desc()).first()
    tweets = Tweets.query.all()
    tweets_containing = []

    counter = 0
    average_polarity = 0
    average_subjectivity = 0
    for tweet in tweets:
        if search_item.content in tweet.content:
            counter+=1
            tweets_containing.append(tweet.content)
            average_polarity += tweet.polarity
            average_subjectivity += tweet.subjectivity
    num = randint(0, len(tweets_containing))
    tweet_string = tweets_containing[num]
    average_polarity = average_polarity/counter
    average_subjectivity = average_subjectivity/counter


    return render_template('search.html', item = search_item.content, amount = counter, subjectivity = average_subjectivity, polarity = average_polarity, tweet = tweet_string)

if __name__ == "__main__":
    app.run(debug=True)