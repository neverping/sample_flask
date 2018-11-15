# Original source: https://github.com/kalise/flask-vote-app.git
import os
import random
import json
import socket

from datetime import datetime
from flask import Flask, request, make_response, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

def create_app(test_config=None, debug_state=False):
    """Create and configure an instance of the Flask application."""
    hostname = socket.gethostname()
    app = Flask(__name__, instance_relative_config=True)
    app.debug = debug_state
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        DATABASE=None
    )

    # BEGIN: DATABASE local
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbhost  = os.environ.get('DB_HOST', '')
    dbport  = os.environ.get('DB_PORT', '')
    dbname  = os.environ.get('DB_NAME', '')
    dbuser  = os.environ.get('DB_USER', '')
    dbpass  = os.environ.get('DB_PASS', '')
    dbtype  = os.environ.get('DB_TYPE', '')

    # TODO: it can be improved
    if dbtype == 'mysql':
        dburi  = dbtype + '://' + dbuser + ':' + dbpass + '@' + dbhost + ':' + dbport + '/' + dbname
    elif dbtype == 'postgresql':
        dburi  = dbtype + '://' + dbuser + ':' + dbpass + '@' + dbhost + ':' + dbport + '/' + dbname
    else:
        dburi = 'sqlite:///' + os.path.join(basedir, 'data/app.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = dburi
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False

    db = SQLAlchemy(app)

    class Poll(db.Model):
        id       = db.Column(db.Integer, primary_key=True)
        name     = db.Column(db.String(30), unique=True)
        question = db.Column(db.String(90))
        stamp    = db.Column(db.DateTime)
        options  = db.relationship('Option', backref='option', lazy='dynamic')

        def __init__(self, name, question, stamp=None):
            self.name  = name
            self.question = question
            if not stamp:
                stamp = datetime.utcnow()
            self.stamp = stamp

    class Option(db.Model):
        id      = db.Column(db.Integer, primary_key=True)
        text    = db.Column(db.String(30))
        poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
        poll    = db.relationship('Poll', backref=db.backref('poll', lazy='dynamic'))
        votes   = db.Column(db.Integer)

        def __init__(self, text, poll, votes):
            self.text = text
            self.poll = poll
            self.votes = votes
    # END: DATABASE local
    # BEGIN: Creating local database

    db.create_all()
    db.session.commit()
    hostname = socket.gethostname()
         
    print("Checking if a poll already exists into db")
    poll = Poll.query.first()
    
    if poll:
        print("Restarting the poll")
        poll.stamp = datetime.utcnow()
        db.session.commit()
    else:
        print("Loading seed data from file")
        try: 
            with open(os.path.join(basedir, 'seeds/seed_data.json')) as file:
                seed_data = json.load(file)
                print("Starting a new poll")
                poll = Poll(seed_data['poll'], seed_data['question'])
                db.session.add(poll)
                for i in seed_data['options']:
                    option = Option(i, poll, 0)
                    db.session.add(option)
                db.session.commit()
        except:
            print("Cannot load seed data from file")
            poll = Poll('', '')
    # END: Creating local database

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(404)
    def not_found(error):
        return 'Unfortunately, not found!'

    @app.route('/')

    @app.route('/index.html')
    def index():
        return render_template('index.html', hostname=hostname, poll=poll)

    @app.route('/vote.html', methods=['POST','GET'])
    def vote():
        if request.method == 'POST':
            vote = request.form['vote']
            voted_option = Option.query.filter_by(poll_id=poll.id,id=vote).first()
            voted_option.votes += 1
            db.session.commit()
            return redirect(url_for('results'), code=302)

        options = Option.query.filter_by(poll_id=poll.id).all()
        resp = make_response(render_template('vote.html', hostname=hostname, poll=poll, options=options))

        return resp

    @app.route('/results.html')
    def results():
        results = Option.query.filter_by(poll_id=poll.id).all()
        return render_template('results.html', hostname=hostname, poll=poll, results=results)

    return app
