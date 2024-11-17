###################################################################################################
# Note: Application will not run this code, this is to upload existing log information and images #
###################################################################################################

import sqlite3
import argparse
import pandas as pd
from datetime import datetime
import os 
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--logfile", help="Upload new log file to migrate", required=False)
parser.add_argument("-i", "--imagedirectory", help="Upload image folder to migrate", required=False)
args = vars(parser.parse_args())

log_path = "api/database/app.db"
image_path = "api/uploads/"
conn = sqlite3.connect(log_path)
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
    floor TEXT,
    notes TEXT
    )
''')
conn.commit()

migrations_dir = os.listdir('migrations/')
log_files = ["migrations/" + x for x in migrations_dir if ".csv" in x]
image_directories = ["migrations/" + x + "/" for x in migrations_dir if "_Hall" in x]

if args['logfile']:
    log_files.append(args['logfile'])
if args['imagedirectory']:
    image_directories.append(args['imagedirectory'])
    
for log in log_files:
    log_df = pd.read_csv(log)
    log_df = log_df.dropna()
    log_df.columns = log_df.iloc[0]
    log_df = log_df[1:]
    for index, row in log_df.iterrows():
        notes = " " if len(row) < 17 else row[16]
        dt_obj = datetime.strptime(row[6], '%m/%d/%Y %H:%M:%S')
        formatted_datetime = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO log_information 
            (photo_id, building_name, latitude, longitude, building_side, time, observed_temp, min_temp, 
            max_temp, frame, distance, outdoor_temp, sun_direction, position, floor, notes)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(photo_id) DO NOTHING
            ''', (row[1], row[2], row[3], row[4], row[5], dt_obj, float(row[7]), 
                  float(row[8]), float(row[9]), row[10], float(row[11]), float(row[12]), row[13], row[14], row[15], notes))
        
for dir in image_directories:
    for filename in os.scandir(dir):
        curr_directory = os.getcwd()
        shutil.copy(os.path.join(*[curr_directory, filename]), os.path.join(*[curr_directory, "api/uploads/"]))         
    
conn.commit()
conn.close()