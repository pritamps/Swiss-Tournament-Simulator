#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
import math

DB_NAME = "tournaments"
TOURNAMENT_NAME = "Wimbledon"
TOURNAMENT_YEAR = "2017"
TOURNAMENT_SPORT = "TENNIS"


def connect(database_name="tournaments"):
    """
    Connects to DB and returns DB and cursor
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Could not connect to database. Aborting!")


def createTournament(tournament_name=TOURNAMENT_NAME,
                     year=TOURNAMENT_YEAR, sport=TOURNAMENT_SPORT):
    """Creates a new tournament and returns its ID"""
    DB, c = connect()
    # Safe insert into DB. USE QUERY PARAMETERS INSTEAD OF STRING SUBSTITUTION
    c.execute("INSERT INTO tournaments (name, year, sport ) VALUES (%s, %s, %s) \
               RETURNING id", (bleach.clean(tournament_name),
                               bleach.clean(year),
                               bleach.clean(sport), ))
    tournament_id = c.fetchone()
    DB.commit()
    DB.close()
    return tournament_id


def getTournamentID(tournament_name=TOURNAMENT_NAME,
                    year=TOURNAMENT_YEAR, sport=TOURNAMENT_SPORT):

    DB, c = connect()
    c.execute("SELECT id from tournaments WHERE name=%s AND year=%s",
              (tournament_name, TOURNAMENT_YEAR))
    rows = c.fetchone()
    if rows is None:
        return None
    else:
        return rows[0]


def deleteMatches():
    """Remove all the match records from the database."""
    DB, c = connect()
    c.execute("TRUNCATE matches")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB, c = connect()
    c.execute("TRUNCATE players CASCADE")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB, c = connect()
    c.execute("SELECT count(*) FROM players")
    count = c.fetchone()[0]
    DB.close()

    return count


def registerPlayer(name, tournament_name=TOURNAMENT_NAME,
                   year=TOURNAMENT_YEAR):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB, c = connect()

    # Get tournament ID for given tournament. If it doesn't exist, create it
    c.execute("SELECT id from tournaments WHERE name=%s AND year=%s",
              (tournament_name, TOURNAMENT_YEAR))
    rows = c.fetchone()
    if rows is None:
        tournament_id = createTournament()[0]
    else:
        tournament_id = rows[0]

    # Add new player (if they don't exist already) and get their ID
    c.execute("INSERT into players (name) VALUES (%s) RETURNING id",
              (bleach.clean(name),))
    player_id = c.fetchone()[0]

    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    list_of_tuples = []
    DB, c = connect()
    c.execute("SELECT * FROM player_standings")
    rows = c.fetchall()
    tournament_id = getTournamentID(tournament_name=TOURNAMENT_NAME,
                                    year=TOURNAMENT_YEAR,
                                    sport=TOURNAMENT_SPORT)
    for row in rows:
        list_of_tuples.append(row)
    DB.close()
    return list_of_tuples


def reportMatch(winner, loser,
                tournament_name=TOURNAMENT_NAME,
                year=TOURNAMENT_YEAR,
                round=-1):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = psycopg2.connect("dbname=" + DB_NAME)
    c = DB.cursor()

    # Get tournament ID for given tournament. If it doesn't exist, create it
    c.execute("SELECT id from tournaments WHERE name=%s AND year=%s",
              (tournament_name, TOURNAMENT_YEAR))
    rows = c.fetchone()

    if rows is None:
        tournament_id = createTournament()[0]
    else:
        tournament_id = rows[0]

    c.execute("INSERT INTO matches (winner, loser, tournament_id, round) VALUES \
              (%s, %s, %s, %s)", (winner, loser, tournament_id, round))

    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    DB, c = connect()
    standings = playerStandings()

    list_of_tuples = []
    for i in range(0, len(standings), 2):
        list_of_tuples.append((standings[i][0], standings[i][1],
                              standings[i+1][0], standings[i+1][1]))

    return list_of_tuples
