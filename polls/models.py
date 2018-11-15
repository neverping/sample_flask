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
