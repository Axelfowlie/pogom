from .utils import get_pokemon_name
from pogom.utils import get_args
from datetime import datetime
import psycopg2
import random
import logging

args = get_args()

conn = psycopg2.connect(dbname="pokemon_go", user="pokemon_go_role", password=args.pokel_pass, host="127.0.0.1")
conn.autocommit = True
cursor = conn.cursor()

log = logging.getLogger(__name__)

def logPokemonDb(p):
    pokemon_id = int(p['pokemon_data']['pokemon_id'])
    pokemon_name = get_pokemon_name(str(pokemon_id)).lower().encode('ascii','ignore')

    last_modified_time = int(p['last_modified_timestamp_ms'])
    time_until_hidden_ms = int(p['time_till_hidden_ms'])

    hidden_time_unix_s = int((p['last_modified_timestamp_ms'] + p['time_till_hidden_ms']) / 1000.0)
    hidden_time_utc = datetime.utcfromtimestamp(hidden_time_unix_s)

    encounter_id = str(p['encounter_id'])
    spawnpoint_id = str(p['spawnpoint_id'])

    longitude = float(p['longitude'])
    latitude = float(p['latitude'])
    longitude_jittered = longitude + (random.gauss(0, 0.3) - 0.5) * 0.0005
    latitude_jittered = latitude + (random.gauss(0, 0.3) - 0.5) * 0.0005

    query =  "INSERT INTO spotted_pokemon (name, encounter_id, last_modified_time, time_until_hidden_ms, hidden_time_unix_s, hidden_time_utc, spawnpoint_id, longitude, latitude, pokemon_id, longitude_jittered, latitude_jittered) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    data = (pokemon_name, encounter_id, last_modified_time, time_until_hidden_ms, hidden_time_unix_s, hidden_time_utc, spawnpoint_id, longitude, latitude, pokemon_id, longitude_jittered, latitude_jittered)

    try:
        cursor.execute(query, data)
    except Exception,e:
        log.error('Postgresql error (%s)', str(e))
