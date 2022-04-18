#!/usr/bin/env python3
"""
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
import sqlite3
import click
import os
from datetime import datetime
from flask import current_app, g
from flask.cli import with_appcontext
import shutil
import csv


def insertIntoDB(col_names, data, username, filepath, table):
    db = get_db()
    insert_statement = '''INSERT INTO {} ({})
    VALUES ({});'''.format(table, col_names, ', '.join(['?'] * (len(data))))
    db.execute(insert_statement, data)
    db.commit()

def parseFile(dir_path, file, user, table, upload_time):
    filename = os.path.basename(file.name)
    filepath = dir_path+"/"+filename
    shutil.copyfile(file.name, filepath)


    if table == "text":
        text = file.read()
        data = [user, filepath, text, upload_time]
        headers = "username, filepath, file_text, upload_time"

        insertIntoDB(headers, data, user, filepath, table)
    else:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if table == "pos_programming":
                headers = "username, filepath, timestamp, Timestamp_Realtime, target_q_0, target_q_1, target_q_2, target_q_3, target_q_4, target_q_5, upload_time"
                data = [user, filepath, row["timestamp"], row["Timestamp_Realtime"], row["target_q_0"], row["target_q_1"], row["target_q_2"], row["target_q_3"], row["target_q_4"], row["target_q_5"], upload_time]
            elif table == "programming":
                headers = "username, filepath, timestamp, Timestamp_Realtime, target_TCP_speed_0, target_TCP_speed_1, target_TCP_speed_2, target_TCP_speed_3, target_TCP_speed_4, target_TCP_speed_5, upload_time"
                data = [user, filepath, row["timestamp"], row["Timestamp_Realtime"], row["target_TCP_speed_0"], row["target_TCP_speed_1"], row["target_TCP_speed_2"], row["target_TCP_speed_3"], row["target_TCP_speed_4"], row["target_TCP_speed_5"], upload_time]
            elif table == "front":
                headers = "username, filepath, timestamp, Timestamp_Realtime, front_score, upload_time"
                data = [user, filepath, row["timestamp"], row[" Timestamp_Realtime"], row[" Engagement score"], upload_time]
            elif table == "back":
                headers = "username, filepath, timestamp, Timestamp_Realtime, back_score, upload_time"
                data = [user, filepath, row["timestamp"], row[" Timestamp_Realtime"], row[" Engagement score"], upload_time]

            insertIntoDB(headers, data, user, filepath, table)


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(upload_files_command)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@click.command('upload-files')
@with_appcontext
def upload_files_command():
    upload_filepath = 'Data'
    dir_list = os.listdir(upload_filepath)
    user_directories = {}
    for f in dir_list:
        if not f.startswith('.'):
            user_directories[f] = []

    for user in user_directories:
        upload_time = datetime.now()
        dir_path = current_app.config['UPLOAD_FOLDER']+user+str(upload_time)
        os.mkdir(dir_path)

        user_files = os.listdir(upload_filepath+'/'+user)
        user_directories[user].extend(user_files)
        for filename in user_directories[user]:
            with open(upload_filepath+'/'+user+'/'+filename) as file:
                if 'pos_programming' in filename:
                    parseFile(dir_path, file, user, 'pos_programming', upload_time)

                elif 'programming' in filename:
                    parseFile(dir_path, file, user, 'programming', upload_time)

                elif 'back' in filename:
                    parseFile(dir_path, file, user, 'back', upload_time)

                elif 'front' in filename:
                    parseFile(dir_path, file, user, 'front', upload_time)

                elif 'txt' in filename:
                    parseFile(dir_path, file, user, 'text', upload_time)
