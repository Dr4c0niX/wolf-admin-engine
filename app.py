# wolf-admin-engine/app.py
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db/wolfgame'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Party(db.Model):
    __tablename__ = 'parties'
    
    id = db.Column(db.Integer, primary_key=True)
    nb_rows = db.Column(db.Integer, nullable=False)
    nb_cols = db.Column(db.Integer, nullable=False)
    max_turn_time = db.Column(db.Integer, nullable=False)
    total_turns = db.Column(db.Integer, nullable=False)
    nb_obstacles = db.Column(db.Integer, nullable=False)
    max_players = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

@app.route('/admin')
def admin_dashboard():
    parties = Party.query.all()
    return render_template('admin.html', parties=parties)

@app.route('/create_party', methods=['POST'])
def create_party():
    new_party = Party(
        nb_rows=int(request.form['nb_rows']),
        nb_cols=int(request.form['nb_cols']),
        max_turn_time=int(request.form['max_turn_time']),
        total_turns=int(request.form['total_turns']),
        nb_obstacles=int(request.form['nb_obstacles']),
        max_players=int(request.form['max_players'])
    )
    
    db.session.add(new_party)
    db.session.commit()
    
    # TODO: Notifier le moteur de jeu via gRPC/TCP
    
    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)