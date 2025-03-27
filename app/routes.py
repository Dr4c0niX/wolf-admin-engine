from flask import Blueprint, jsonify, request
from .models import db, Party, Player, Obstacle
import random
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/create_party', methods=['POST'])
def create_party():
    data = request.get_json()
    
    required_params = ['rows', 'columns', 'max_turn_time', 'total_turns',
                     'obstacles_count', 'max_players', 'wolves_count']
    
    if not all(param in data for param in required_params):
        return jsonify({'status': 'KO', 'message': 'Missing parameters'}), 400
    
    villagers_count = data['max_players'] - data['wolves_count']
    
    new_party = Party(
        rows=data['rows'],
        columns=data['columns'],
        max_turn_time=data['max_turn_time'],
        total_turns=data['total_turns'],
        obstacles_count=data['obstacles_count'],
        max_players=data['max_players'],
        wolves_count=data['wolves_count'],
        villagers_count=villagers_count
    )
    
    db.session.add(new_party)
    db.session.commit()
    
    return jsonify({
        'status': 'OK',
        'party_id': new_party.id,
        'message': 'Game created successfully'
    })

@admin_bp.route('/list_parties', methods=['GET'])
def list_parties():
    parties = Party.query.filter_by(started=False, completed=False).all()
    
    result = [{
        'id': party.id,
        'rows': party.rows,
        'columns': party.columns,
        'max_players': party.max_players,
        'current_players': Player.query.filter_by(party_id=party.id).count(),
        'created_at': party.created_at.isoformat()
    } for party in parties]
    
    return jsonify({'status': 'OK', 'parties': result})