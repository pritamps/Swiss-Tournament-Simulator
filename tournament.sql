-- Table definitions for the tournament project.

-- Connect to the tournaments database. 

DROP DATABASE IF EXISTS tournaments;
CREATE DATABASE tournaments;
\c tournaments;

-- Create players database
CREATE TABLE players ( id SERIAL PRIMARY KEY,
                       name TEXT );

-- Table of all tournaments. 
CREATE TABLE tournaments ( id SERIAL PRIMARY KEY,
                           name TEXT,
                           sport TEXT,
                           year TEXT, 
                           UNIQUE ( name, year ) );

-- Create matches database
CREATE TABLE matches ( id SERIAL PRIMARY KEY,
                      winner SERIAL references players(id),
                      loser SERIAL references players(id),
                      tournament_id SERIAL references tournaments(id),
                      round SMALLINT );

-- Create view for wins and losses for players
CREATE VIEW player_wins AS 
                    ( SELECT players.name as name, players.id as id, count(matches.winner) AS wins 
                      FROM players LEFT JOIN matches ON players.id=matches.winner 
                      GROUP by players.id );

CREATE VIEW player_matches AS 
                    ( SELECT players.name as name, players.id as id, count(matches.winner) AS matches 
                      FROM players LEFT JOIN matches ON ( players.id=matches.winner OR players.id=matches.loser )
                      GROUP by players.id );

CREATE VIEW player_standings AS 
                    ( SELECT player_wins.id, player_wins.name, wins, matches 
                      FROM (player_wins INNER JOIN player_matches ON player_wins.id=player_matches.id) 
                      ORDER BY wins DESC);




