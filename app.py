# wolf-admin-engine/app.py
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wolf_admin:motdepasse_secure@db/wolf_game'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Party(db.Model):
    __tablename__ = 'parties'
    
    id_party = db.Column(db.Integer, primary_key=True, name='id_party')
    title_party = db.Column(db.String(100), name='title_party', nullable=False) 
    grid_size = db.Column(db.Integer, name='grid_size', nullable=False, default=10) 
    max_players = db.Column(db.Integer, name='max_players', nullable=False, default=8)  
    max_turns = db.Column(db.Integer, name='max_turns', nullable=False, default=30)  
    turn_duration = db.Column(db.Integer, name='turn_duration', nullable=False, default=60) 
    created_at = db.Column(db.DateTime, name='created_at', server_default=db.func.now())
    is_started = db.Column(db.Boolean, name='is_started', default=False)
    is_finished = db.Column(db.Boolean, name='is_finished', default=False)

@app.route('/admin')
def admin_dashboard():
    parties = Party.query.all()
    return render_template('admin.html', parties=parties)

@app.route('/create_party', methods=['POST'])
def create_party():
    new_party = Party(
        title_party=request.form['title_party'],
        grid_size=int(request.form['grid_size']),
        turn_duration=int(request.form['turn_duration']),
        max_turns=int(request.form['max_turns']),
        max_players=int(request.form['max_players'])
    )
    
    db.session.add(new_party)
    db.session.commit()
    
    # TODO: Notifier le moteur de jeu via gRPC/TCP
    
    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)