###################################################################################################
# Note: Application will not run this code, this is to upload existing log information and images #
###################################################################################################

import sqlite3
import argparse
import pandas as pd
from datetime import datetime
import os 

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--logfile', help='Upload new log file to migrate', required=False)
args = vars(parser.parse_args())

path = "api/database/app.db"
conn = sqlite3.connect(path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS log_information (
    photo_id CHAR(6) PRIMARY KEY,
    building_name CHAR(12),
    latitude TEXT,
    longitude TEXT,
    building_side CHAR(5),
    time DATE,
    observed_temp NUMERIC,
    min_temp NUMERIC,
    max_temp NUMERIC,
    frame CHAR(12),
    distance NUMERIC,
    outdoor_temp NUMERIC,
    sun_direction CHAR(12),
    position CHAR(8),
    floor TEXT
    )
''')
conn.commit()

logfiles = os.listdir('migrations/')
logfiles = ['migrations/' + x for x in logfiles if ".csv" in x]

if args['logfile']:
    logfiles.append(args['logfile'])
    
for logfile in logfiles:
    logfile_df = pd.read_csv(logfile)
    logfile_df = logfile_df.dropna()
    logfile_df.columns = logfile_df.iloc[0]
    logfile_df = logfile_df[1:]
    for index, row in logfile_df.iterrows():
        dt_obj = datetime.strptime(row[6], '%m/%d/%Y %H:%M:%S')
        formatted_datetime = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO log_information 
            (photo_id, building_name, latitude, longitude, building_side, time, observed_temp, min_temp, 
            max_temp, frame, distance, outdoor_temp, sun_direction, position, floor)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(photo_id) DO NOTHING
            ''', (row[1], row[2], row[3], row[4], row[5], formatted_datetime, float(row[7]), 
                  float(row[8]), float(row[9]), row[10], float(row[11]), float(row[12]), row[13], row[14], row[15]))
conn.commit()
conn.close()