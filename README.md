# Swiss-Tournament-Simulator

Project to simulate a swiss style sports tournament.

## Running the code 

### Dependencies

1. To run, you will need PostGreSQL installed on your system. 
2. Python is needed
3. Python Dependencies: bleach, psycopg2

## Running the code

1. To initialize the database, at a command line prompt, type:

```python
$ psql
psqlPrompt => \i tournament.sql
```

2. To run the tests now, simply type:

```
$ python tournament_test.py
```

## Issues

The following issues exist (where I say that I did not do the extra credit portions):

1. Multiple tournaments are not supported. There is preliminary support in that matches are linked to a tournament ID, but this is not reflected in the player standings
2. Only even numbers of players are supported. Nothing has been done in this regard.
