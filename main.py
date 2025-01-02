from flask import Flask, jsonify, request
import pymysql
from pymysql import cursors  # Correct import pour PyMySQL


# Configuration de la base de données
connection = pymysql.connect(
    host="sql5.freesqldatabase.com",  # Serveur local
    user="sql5755343",  # Utilisateur par défaut
    password="jt6JRIJgJB",  # Mot de passe vide par défaut (remplacez si modifié)
    database="sql5755343",  # Nom de votre base de données
    port=3306,  # Port MySQL par défaut (modifiable dans XAMPP)
    charset="utf8mb4",  # Encodage des caractères
    cursorclass=pymysql.cursors.DictCursor  # Pour recevoir les résultats sous forme de dictionnaire
)

app = Flask(__name__)

# Route pour récupérer les informations des athlètes
@app.route('/athletes', methods=['GET'])
def get_all_player_info():
    connection = pymysql.connect(
        host="sql5.freesqldatabase.com",
        user="sql5755343",
        password="jt6JRIJgJB",
        database="sql5755343",
        port=3306,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT 
                    a.firstName AS AthleteFirstName,
                    a.lastName AS AthleteLastName,
                    a.athletesId AS athletesId,
                    a.teamId AS teamId,
                    a.img AS AthleteImage,
                    t.teamName AS TeamName,
                    t.sportName AS SportName,
                    t.division AS DivisionName
                FROM 
                    athletes a
                LEFT JOIN 
                    team t ON a.teamId = t.teamId;
                """
            cursor.execute(sql)
            results = cursor.fetchall()
            return jsonify(results), 200  # Renvoie les résultats sous forme JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour vérifier les tables spécifiques pour un athlète donné
@app.route('/athlete/<athlete_id>/stats', methods=['GET'])
def my_home_screen(athlete_id):
    tables = [
        "StatQB", "StatRB", "StatWR",
        "StatDef", "StatPunt", "StatPuntReturn",
        "StatKickoff", "StatKickoffReturn"
    ]
    total = []

    try:
        with connection.cursor() as cursor:
            for table in tables:
                sql = f"SELECT athletesId FROM {table} WHERE athletesId = %s AND hasStats = 1"
                cursor.execute(sql, (athlete_id,))
                result = cursor.fetchone()

                if result:
                    sql = f"SELECT * FROM {table} WHERE athletesId = %s"
                    cursor.execute(sql, (athlete_id,))
                    exist = cursor.fetchone()
                    total.append(exist)  # Ajout des statistiques
            return jsonify(total), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(port=5000,)
