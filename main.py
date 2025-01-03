# app.py

from flask import Flask, jsonify
from backend import get_all_players, get_athlete_stats, close_db
from flask import g

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

# Route pour récupérer les informations des athlètes
@app.route('/athletes', methods=['GET'])
def athletes():
    try:
        players = get_all_players()
        return jsonify(players), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour récupérer les statistiques d'un athlète spécifique
@app.route('/athlete/<athlete_id>/stats', methods=['GET'])
def athlete_stats(athlete_id):
    try:
        stats = get_athlete_stats(athlete_id)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
