from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Party(db.Model):
    __tablename__ = 'parties'
    
    id = db.Column(db.Integer, primary_key=True)
    rows = db.Column(db.Integer, nullable=False)
    columns = db.Column(db.Integer, nullable=False)
    max_turn_time = db.Column(db.Integer, nullable=False)
    total_turns = db.Column(db.Integer, nullable=False)
    obstacles_count = db.Column(db.Integer, nullable=False)
    max_players = db.Column(db.Integer, nullable=False)
    wolves_count = db.Column(db.Integer, nullable=False)
    villagers_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    started = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)

class Player(db.Model):
    __tablename__ = 'players'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    role = db.Column(db.String(20), nullable=False)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'))
    joined_at = db.Column(db.DateTime, default=db.func.now())

class Obstacle(db.Model):
    __tablename__ = 'obstacles'
    
    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('parties.id'))
    row = db.Column(db.Integer, nullable=False)
    col = db.Column(db.Integer, nullable=False)