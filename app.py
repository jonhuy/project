from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

import snscrape.modules.twitter as sntwitter
import json



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), nullable=False)
    content = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return '<Tweet %r>' % self.content



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        account = request.form['content']
        new_task = User(content=account)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/search')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = User.query.order_by(User.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/search')
def search():
    search_item = User.query.order_by(User.id.desc()).first()
    tweets = Tweets.query.all()
    counter = 0
    for ele in tweets:
        if search_item.content in ele.content:
            counter+=1

    return 'number of tweets with %s in it is %d' % (search_item, counter)
if __name__ == "__main__":
    app.run(debug=True)