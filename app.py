# wolf-admin-engine/app.py
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import socket
import json
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wolf_admin:motdepasse_secure@db/wolf_game'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configuration de la connexion TCP
HTTP_SERVER_HOST = os.environ.get('HTTP_SERVER_HOST', 'http_server')  # Nom du service dans docker-compose
HTTP_SERVER_PORT = int(os.environ.get('HTTP_SERVER_PORT', 9000))  # Port TCP dédié pour les notifications

class Party(db.Model):
    __tablename__ = 'parties'
    
    id_party = db.Column(db.Integer, primary_key=True, name='id_party')
    title_party = db.Column(db.String(100), name='title_party', nullable=False) 
    grid_rows = db.Column(db.Integer, name='grid_rows', nullable=False, default=10)  # Modifié
    grid_cols = db.Column(db.Integer, name='grid_cols', nullable=False, default=10)  # Modifié
    obstacles_count = db.Column(db.Integer, name='obstacles_count', nullable=False, default=0)  # Ajouté
    max_players = db.Column(db.Integer, name='max_players', nullable=False, default=8)  
    max_turns = db.Column(db.Integer, name='max_turns', nullable=False, default=30)  
    turn_duration = db.Column(db.Integer, name='turn_duration', nullable=False, default=60) 
    created_at = db.Column(db.DateTime, name='created_at', server_default=db.func.now())
    is_started = db.Column(db.Boolean, name='is_started', default=False)
    is_finished = db.Column(db.Boolean, name='is_finished', default=False)

def notify_http_server(party_data):
    """
    Notifie le serveur HTTP d'une nouvelle partie via TCP
    """
    try:
        # Création d'une socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connexion au serveur
            sock.connect((HTTP_SERVER_HOST, HTTP_SERVER_PORT))
            
            # Préparation du message
            message = {
                "action": "new_party",
                "data": party_data
            }
            
            # Envoi du message
            sock.sendall(json.dumps(message).encode('utf-8'))
            
            # Attente de la réponse (optionnel)
            response = sock.recv(1024)
            print(f"Réponse du serveur HTTP: {response.decode('utf-8')}")
            
        print(f"Notification envoyée au serveur HTTP: {party_data}")
        return True
    except Exception as e:
        print(f"Erreur lors de la notification au serveur HTTP: {e}")
        return False

@app.route('/admin')
def admin_dashboard():
    parties = Party.query.all()
    return render_template('admin.html', parties=parties)

@app.route('/create_party', methods=['POST'])
def create_party():
    new_party = Party(
        title_party=request.form['title_party'],
        grid_rows=int(request.form['grid_rows']),  # Modifié
        grid_cols=int(request.form['grid_cols']),  # Modifié
        obstacles_count=int(request.form['obstacles_count']),  # Ajouté
        turn_duration=int(request.form['turn_duration']),
        max_turns=int(request.form['max_turns']),
        max_players=int(request.form['max_players'])
    )
    
    db.session.add(new_party)
    db.session.commit()
    
    # Notifier le serveur HTTP via TCP
    party_data = {
        "id_party": new_party.id_party,
        "title_party": new_party.title_party,
        "grid_rows": new_party.grid_rows,  # Modifié
        "grid_cols": new_party.grid_cols,  # Modifié
        "obstacles_count": new_party.obstacles_count,  # Ajouté
        "max_players": new_party.max_players,
        "max_turns": new_party.max_turns,
        "turn_duration": new_party.turn_duration
    }
    notify_http_server(party_data)
    
    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)