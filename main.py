# app.py
from flask import Flask, jsonify,request

from backend import get_all_players, get_athlete_stats, close_db, get_all_teams, get_game, get_athlete
from flask import g

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

# Route pour récupérer les informations des athlètes
@app.route('/athletes', methods=['POST','GET'])
def athletes():
    try:
            players = get_all_players()
            return jsonify(players), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/team', methods=['POST','GET'])
def teams():
    try:
            players = get_all_teams()
            return jsonify(players), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route pour récupérer les statistiques d'un athlète spécifique
@app.route('/athlete/stats',methods=['POST'])
def athlete_stats():
    print(request.get_json())

    data = request.get_json()

    if not data or 'athlete_id' not in data:
        return jsonify({"error": "Missing athlete_id"}), 400
    athlete_id = data['athlete_id']
    try:

        stats = get_athlete_stats(athlete_id)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/game',methods=['POST'])
def athlete_game():
    print(request.get_json())

    data = request.get_json()

    if not data or 'team_id' not in data:
        return jsonify({"error": "Missing athlete_id"}), 400
    athlete_id = data['team_id']
    try:

        stats = get_game(athlete_id)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/athlete',methods=['POST'])
def athlete():
    print(request.get_json())

    data = request.get_json()

    if not data or 'athlete_id' not in data:
        return jsonify({"error": "Missing athlete_id"}), 400
    athlete_id = data['athlete_id']
    try:

        stats = get_athlete(athlete_id)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
