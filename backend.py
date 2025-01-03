# Backend/ApiControl.py

import pymysql
from flask import g

def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="sql5.freesqldatabase.com",
            user="sql5755343",
            password="jt6JRIJgJB",
            database="sql5755343",
            port=3306,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def get_all_players():
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
    return results

def get_athlete_stats(athlete_id):
    tables = [
        "StatQB", "StatRB", "StatWR",
        "StatDef", "StatPunt", "StatPuntReturn",
        "StatKickoff", "StatKickoffReturn"
    ]
    total = []

    db = get_db()
    with db.cursor() as cursor:
        for table in tables:
            sql = f"SELECT athletesId FROM {table} WHERE athletesId = %s AND hasStats = 1"
            cursor.execute(sql, (athlete_id,))
            result = cursor.fetchone()

            if result:
                sql = f"SELECT * FROM {table} WHERE athletesId = %s"
                cursor.execute(sql, (athlete_id,))
                exist = cursor.fetchone()
                if exist:
                    total.append(exist)
    return total
