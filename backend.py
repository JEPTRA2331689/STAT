# Backend/ApiControl.py

import pymysql
from flask import g


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="sql5.freesqldatabase.com",  # Serveur local
            user="sql5755343",  # Utilisateur par défaut
            password="jt6JRIJgJB",  # Mot de passe vide par défaut (remplacez si modifié)
            database="sql5755343",  # Nom de votre base de données
            port=3306,  # Port MySQL par défaut (modifiable dans XAMPP)
            charset="utf8mb4",  # Encodage des caractères
            cursorclass=pymysql.cursors.DictCursor  # Pour recevoir les résultats sous forme de dictionnaired
        )
    return g.db


def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def get_all_players():
    try:
        db = get_db()
        with db.cursor() as cursor:
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
            players = [
                {
                    "full_name": f"{row['AthleteFirstName']} {row['AthleteLastName']}",
                    "athletesId": row['athletesId'],
                    "teamId": row['teamId'],
                    "AthleteImage": row['AthleteImage'],
                    "TeamName": row['TeamName'],
                    "sportName": row['SportName'],
                    "division": row['DivisionName']
                }
                for row in results
            ]
        return players
    except Exception as e:
        print(f"Error fetching players: {e}")
        return []
    finally:
        close_db()


def get_all_teams():
    try:
        db = get_db()
        with db.cursor() as cursor:
            sql = """
                SELECT 
                    t.teamId AS teamId,
                    t.teamName AS TeamName,
                    t.sportName AS SportName,
                    t.division AS DivisionName,
                    t.primaryColor AS PrimaryColor,
                    t.secondaryColor AS SecondaryColor
                FROM 
                    team AS t
            """
            print("Exécution de la requête SQL...")
            cursor.execute(sql)
            results = cursor.fetchall()
            print(f"Résultats bruts : {results}")

            teams = [
                {
                    "teamId": row['teamId'],
                    "TeamName": row['TeamName'],
                    "sportName": row['SportName'],
                    "division": row['DivisionName'],
                    "primaryColor": row['PrimaryColor'],
                    "secondaryColor": row['SecondaryColor']
                }
                for row in results
            ]
            print(f"Résultats formatés : {teams}")
        return teams

    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête : {e}")
        return {"error": str(e)}

    finally:
        close_db()


def get_athlete_stats(athlete_id):
    tables = [
        "StatQB", "StatRB", "StatWR",
        "StatDef", "StatPunt", "StatPuntReturn",
        "StatKickoff", "StatKickoffReturn"
    ]
    total = []

    db = get_db()
    with db.cursor() as cursor:  # Utiliser des dictionnaires pour un accès facile
        for table in tables:
            # Vérifier si des statistiques existent pour l'athlète dans la table actuelle
            sql = f"SELECT athletesId FROM {table} WHERE athletesId = %s AND hasStats = 1"
            cursor.execute(sql, (athlete_id,))
            result = cursor.fetchone()

            if result:
                # Récupérer toutes les colonnes pour l'athlète dans la table actuelle
                sql = f"SELECT * FROM {table} WHERE athletesId = %s"
                cursor.execute(sql, (athlete_id,))
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        for key, value in row.items():
                            # Ignorer les colonnes qui ne sont pas des statistiques
                            if key not in ["athletesId", "hasStats"]:
                                total.append({
                                    "stateName": key,
                                    "stat": value
                                })

    return total


def get_game(team_id, order="DESC"):
    db = get_db()
    try:
        with db.cursor() as cursor:
            sql = f"""
                SELECT 
                    tg.gameId,
                    DATE_FORMAT(tg.gameDate, '%%Y-%%m-%%d %%H:%%i:%%s') AS gameDate,
                    tg.visitingTeamId,
                    tg.homeTeamId,
                    tg.visitingTeamScore,
                    tg.homeTeamScore,
                    t1.teamName AS visitingTeamName,
                    t2.teamName AS homeTeamName,
                    gs.*
                FROM 
                    TeamGames tg
                LEFT JOIN 
                    GameStat gs ON tg.gameId = gs.GameId
                LEFT JOIN 
                    team t1 ON tg.visitingTeamId = t1.teamId
                LEFT JOIN 
                    team t2 ON tg.homeTeamId = t2.teamId
                WHERE 
                    tg.visitingTeamId = %s OR tg.homeTeamId = %s
                ORDER BY 
                    tg.gameDate {order};
            """
            cursor.execute(sql, (team_id, team_id))
            results = cursor.fetchall()
            print(results)
            return results

    except Exception as e:
        print(f"Erreur : {e}")
        return None

def get_players(athlete_id):
    try:
        db = get_db()
        with db.cursor() as cursor:
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
                    team t ON a.teamId = t.teamId
                WHERE 
                    a.athletesId = %s;
            """
            cursor.execute(sql, (athlete_id,))
            results = cursor.fetchall()

            # Si la requête retourne des résultats, récupérer le premier élément
            if results:
                player = results[0]
                players = {
                    "full_name": f"{player['AthleteFirstName']} {player['AthleteLastName']}",
                    "athletesId": player['athletesId'],
                    "teamId": player['teamId'],
                    "AthleteImage": player['AthleteImage'],
                    "TeamName": player['TeamName'],
                    "sportName": player['SportName'],
                    "division": player['DivisionName']
                }
                return players
            else:
                print("Aucun joueur trouvé pour cet ID.")
                return None
    except Exception as e:
        print(f"Error fetching players: {e}")
        return None
    finally:
        close_db()
def get_athlete(athlete_id):
    db = get_db()  # Connexion à la base de données
    try:
        with db.cursor() as cursor:
            # Requête pour récupérer les informations de l'athlète
            sql = """
            SELECT 
                a.athletesId,
                a.firstName,
                a.lastName,
                a.position,
                a.number,
                a.height,
                a.weight,
                a.img,
                t.teamId,
                t.teamName,
                t.sportName,
                t.division,
                t.primaryColor,
                t.secondaryColor
            FROM 
                athletes a
            LEFT JOIN 
                team t ON a.teamId = t.teamId
            WHERE 
                a.athletesId = %s
            """
            cursor.execute(sql, (athlete_id,))
            result = cursor.fetchone()

            if not result:
                return {"error": "Athlete not found"}
            return result
    except Exception as e:
        print(f"Erreur : {e}")
        return {"error": str(e)}


def get_team_players(team_id):
    db = get_db()  # Connexion à la base de données
    try:
        with db.cursor() as cursor:
            # Requête pour récupérer les athlètes d'une équipe
            sql = """
            SELECT 
                a.athletesId,
                a.firstName,
                a.lastName,
                a.position,
                a.number,
                a.height,
                a.weight,
                a.img,
                t.teamName,
                t.sportName,
                t.division,
                t.primaryColor,
                t.secondaryColor
            FROM 
                athletes a
            LEFT JOIN 
                team t ON a.teamId = t.teamId
            WHERE 
                a.teamId = %s
            """
            cursor.execute(sql, (team_id,))
            result = cursor.fetchall()

            if not result:
                return {"error": "No players found for this team"}
            return result

    except Exception as e:
        print(f"Erreur : {e}")
        return {"error": str(e)}
