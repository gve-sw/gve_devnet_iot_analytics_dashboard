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
import os
import csv
from datetime import datetime
import pandas as pd
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from src.db import get_db
from src.auth import login_required
from pprint import pprint

bp = Blueprint('portal', __name__)


def insertIntoDB(col_names, data, username, filepath, table):
    db = get_db()
    insert_statement = '''INSERT INTO {} ({}) VALUES
        ({});'''.format(table, col_names, ', '.join(['?'] * (len(data))))
    db.execute(insert_statement, data)
    db.commit()


'''This function parses the file uploaded to add it to the database.
Depending on which file it is parsing, it pulls the data from the file
and formats it for adding to the database.'''
def parseFile(dir_path, file, user, table, upload_time):
    filename = secure_filename(file.filename)
    filepath = dir_path+"/"+filename
    file.save(filepath)

    with open(filepath, mode='r') as file:
        if table == "text":
            text = file.read()
            data = [user, filepath, text, upload_time]
            headers = 'username, filepath, file_text, upload_time'

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


'''This function calculates the maximum, minimum, and average front
and back scores for each user from the front.csv and back.csv files.
The data used to calculate these metrics is first cleaned by removing
the 0s from the dataset'''
def calculatePerformanceMetrics(db, users):
    scores = []

    for user in users:
        select_statement = '''SELECT MAX(back.back_score) AS max_back,
        MIN(back.back_score) AS min_back,
        AVG(back.back_score) AS avg_back,
        MAX(front.front_score) AS max_front,
        MIN(front.front_score) AS min_front,
        AVG(front.front_score) AS avg_front,
        back.upload_time AS upload_time,
        back.username AS username
        FROM back
        LEFT JOIN front ON back.username = front.username AND back.upload_time = front.upload_time
        WHERE back_score!=0.0 AND front_score!=0.0 AND back.username="{}"
        GROUP BY back.upload_time'''.format(user["username"])
        scores.extend(db.execute(select_statement).fetchall())

    return scores


'''This function calculates the programming times of each user
according the programming files they uploaded. The time to
program is calcuated by subtracting the end time from the start
time. The start time is the timestamp of the first row where all
target_TCP_speed values are 0. The end time is the first row
where all target_TCP_speed values are 0 when the remaining rows
also all have target_TCP_speed values of 0.'''
def calculateProgrammingTimes(db, users):
    users_time_to_program = []
    programming_dfs = []
    for user in users:
        upload_time_statement = '''SELECT DISTINCT upload_time
        FROM programming
        WHERE username="{}"'''.format(user["username"])
        upload_times = db.execute(upload_time_statement).fetchall()
        for time in upload_times:
            select_statement = '''SELECT *
            FROM programming
            WHERE username="{}" AND upload_time="{}"'''.format(user["username"], time["upload_time"])
            df = pd.read_sql_query(select_statement, db)
            programming_dfs.append(df)

    for df in programming_dfs:
        x = 0
        user = df.loc[0, 'username']
        upload_time = df.loc[0, 'upload_time']
        upload_date_unformatted = datetime.strptime(upload_time, '%Y-%m-%d %H:%M:%S.%f')
        upload_date = upload_date_unformatted.strftime('%Y-%m-%d %H:%M')

        for i, rows in df.iterrows():
            if (df.loc[i, 'target_TCP_speed_0'] == 0 and df.loc[i, 'target_TCP_speed_1'] == 0 and df.loc[i, 'target_TCP_speed_2'] == 0 and df.loc[i, 'target_TCP_speed_3'] == 0 and df.loc[i, 'target_TCP_speed_4'] == 0 and df.loc[i, 'target_TCP_speed_5'] == 0):
                inicio = df.iloc[i,0]
                ini_row = i
                break

        for i, rows in df.iterrows():
            if (df.loc[i, 'target_TCP_speed_0'] == 0 and df.loc[i, 'target_TCP_speed_1'] == 0 and df.loc[i, 'target_TCP_speed_2'] == 0 and df.loc[i, 'target_TCP_speed_3'] == 0 and df.loc[i, 'target_TCP_speed_4'] == 0 and df.loc[i, 'target_TCP_speed_5'] == 0):
                if x == 0:
                    x = 1
                elif x == 2:
                    final = df.iloc[i,0]
                    final_row = i
                    x = 3

            if (df.loc[i, 'target_TCP_speed_0'] != 0 and df.loc[i, 'target_TCP_speed_1'] != 0 and df.loc[i, 'target_TCP_speed_2'] != 0 and df.loc[i, 'target_TCP_speed_3'] != 0 and df.loc[i, 'target_TCP_speed_4'] != 0 and df.loc[i, 'target_TCP_speed_5'] != 0):
                x = 2

        init_time = df.loc[ini_row, 'timestamp']
        end_time = df.loc[final_row, 'timestamp']
        time_to_program = end_time - init_time

        new_programming_time = {"user": user, "time_to_program": time_to_program, "upload_time": upload_date}
        users_time_to_program.append(new_programming_time)


    return users_time_to_program


'''This function calculates the decision time to program. This value
is calculated from the data within the programming csv file the user
uploaded. The decision time to program is the sum of intervals when
target_TCP_speed values are zero.'''
def calculateDecisionTimes(db, user_query):
    user_decision_times = []
    programming_dfs = []
    for user in user_query:
        upload_time_statement = '''SELECT DISTINCT upload_time
        FROM programming
        WHERE username="{}"'''.format(user["username"])
        upload_times = db.execute(upload_time_statement).fetchall()
        for time in upload_times:
            select_statement = '''SELECT *
            FROM programming
            WHERE username="{}" AND upload_time="{}"'''.format(user["username"], time["upload_time"])
            df = pd.read_sql_query(select_statement, db)
            programming_dfs.append(df)

    for df in programming_dfs:
        x = 0
        user = df.loc[0, 'username']
        upload_time = df.loc[0, 'upload_time']
        upload_date = datetime.strptime(upload_time, '%Y-%m-%d %H:%M:%S.%f')
        upload_date = upload_date.strftime('%Y-%m-%d %H:%M')

        for i, rows in df.iterrows():
            if (df.loc[i, 'target_TCP_speed_0'] == 0 and df.loc[i, 'target_TCP_speed_1'] == 0 and df.loc[i, 'target_TCP_speed_2'] == 0 and df.loc[i, 'target_TCP_speed_3'] == 0 and df.loc[i, 'target_TCP_speed_4'] == 0 and df.loc[i, 'target_TCP_speed_5'] == 0):
                inicio = df.iloc[i,0]
                ini_row = i
                break

        for i, rows in df.iterrows():
            if (df.loc[i, 'target_TCP_speed_0'] == 0 and df.loc[i, 'target_TCP_speed_1'] == 0 and df.loc[i, 'target_TCP_speed_2'] == 0 and df.loc[i, 'target_TCP_speed_3'] == 0 and df.loc[i, 'target_TCP_speed_4'] == 0 and df.loc[i, 'target_TCP_speed_5'] == 0):
                if x == 0:
                    x = 1
                elif x == 2:
                    final = df.iloc[i,0]
                    final_row = i
                    x = 3

            if (df.loc[i, 'target_TCP_speed_0'] != 0 and df.loc[i, 'target_TCP_speed_1'] != 0 and df.loc[i, 'target_TCP_speed_2'] != 0 and df.loc[i, 'target_TCP_speed_3'] != 0 and df.loc[i, 'target_TCP_speed_4'] != 0 and df.loc[i, 'target_TCP_speed_5'] != 0):
                x = 2

        y = 0
        init_time = df.loc[ini_row, 'timestamp']
        time_sum = 0

        for i, rows in df.iterrows():
            if (i>ini_row and i<=final_row and df.loc[i, 'target_TCP_speed_0'] == 0 and df.loc[i, 'target_TCP_speed_1'] == 0 and df.loc[i, 'target_TCP_speed_2'] == 0 and df.loc[i, 'target_TCP_speed_3'] == 0 and df.loc[i, 'target_TCP_speed_4'] == 0 and df.loc[i, 'target_TCP_speed_5'] == 0):
                if y == 0:
                    counter = df.loc[i, 'timestamp']
                elif y == 1:
                    init_time = df.loc[i,'timestamp']
                    y = 0

            if (i>ini_row and i<=final_row and df.loc[i, 'target_TCP_speed_0'] != 0 and df.loc[i, 'target_TCP_speed_1'] != 0 and df.loc[i, 'target_TCP_speed_2'] != 0 and df.loc[i, 'target_TCP_speed_3'] != 0 and df.loc[i, 'target_TCP_speed_4'] != 0 and df.loc[i, 'target_TCP_speed_5'] != 0):
                if y == 0:
                    time_sum += (counter - init_time)
                    y = 1

        new_decision_time = {"user": user, "decision_time": time_sum, "upload_time": upload_date}
        user_decision_times.append(new_decision_time)

    return user_decision_times


'''This function calculates the time to command for each user
according to the data from the programming csv files they
uploaded. The time to command is calculated by subtracting the
decision time to program from the total time to program.'''
def calculateCommandTimes(programming_times, decision_times):
    command_times = []
    for prog_time in programming_times:
        for decision_time in decision_times:
            if prog_time["user"] == decision_time["user"] and prog_time["upload_time"] == decision_time["upload_time"]:
                new_command_time = {"user": prog_time["user"], "command_time": prog_time["time_to_program"] - decision_time["decision_time"], "upload_time": prog_time["upload_time"]}
                command_times.append(new_command_time)

    return command_times


'''This function calculates the cycle times for each user
according to the data from the pos_programming csv files
they uplaoded. The cycle time is determined by the amount of
time it takes from when the leaving the home position for
the first time to returning returning to the home position
for the first time. The home position is given by the
coordinates [0.0, -1.57, 0.0, -1.57, 0.0, 0.0].'''
def calculateCycleTimes(db, users):
    cycle_times = []
    pos_programming_dfs = []
    home = [0.0, -1.57, 0.0, -1.57, 0.0, 0.0]

    for user in users:
        upload_time_statement = '''SELECT DISTINCT upload_time
        FROM pos_programming
        WHERE username="{}"'''.format(user["username"])
        upload_times = db.execute(upload_time_statement).fetchall()
        for time in upload_times:
            select_statement = '''SELECT *
            FROM pos_programming
            WHERE username="{}" AND upload_time="{}"'''.format(user["username"], time["upload_time"])
            df = pd.read_sql_query(select_statement, db)
            pos_programming_dfs.append(df)

    for df in pos_programming_dfs:
        x = 0
        start = df.loc[0,'timestamp']
        end = len(df.index)
        user = df.loc[0, 'username']
        upload_time = df.loc[0, 'upload_time']
        upload_date = datetime.strptime(upload_time, '%Y-%m-%d %H:%M:%S.%f')
        upload_date = upload_date.strftime('%Y-%m-%d %H:%M')
        for i, rows in df.iterrows():
            if (round(df.loc[i,'target_q_0'], 3) == home[0] and round(df.loc[i,'target_q_1'], 2) == home[1] and round(df.loc[i,'target_q_2'], 2) == home[2] and round(df.loc[i,'target_q_3'], 2) == home[3] and round(df.loc[i,'target_q_4'], 3) == home[4] and round(df.loc[i,'target_q_5'],2) == home[5]):
                if x == 0 or x == 1:
                    start = df.loc[i,'timestamp']
                    x = 1
                elif x == 2:
                    end = df.loc[i,'timestamp']
                    x = 3
            if (x != 3 and round(df.loc[i,'target_q_0'], 3) != home[0] and round(df.loc[i,'target_q_1'], 2) != home[1] and round(df.loc[i,'target_q_2'], 2) != home[2] and round(df.loc[i,'target_q_3'], 2) != home[3] and round(df.loc[i,'target_q_4'], 3) != home[4] and round(df.loc[i,'target_q_5'],2) != home[5]):
                x = 2

        new_cycle_time = {"user": user, "cycle_time": end - start, "upload_time": upload_date}
        cycle_times.append(new_cycle_time)

    return cycle_times


'''The home page displays the scores calculated in the
functions above for each user.'''
@bp.route('/', methods=('GET',))
def home():
    db = get_db()

    user_select_statement = '''SELECT DISTINCT username FROM user'''
    users = db.execute(user_select_statement).fetchall()

    scores = calculatePerformanceMetrics(db, users)
    user_scores = []
    for score in scores:
        upload_date = datetime.strptime(score["upload_time"], '%Y-%m-%d %H:%M:%S.%f')
        user_score = {
            "username": score["username"],
            "upload_time": upload_date.strftime('%Y-%m-%d %H:%M'),
            "max_back": score["max_back"],
            "min_back": score["min_back"],
            "avg_back": score["avg_back"],
            "max_front": score["max_front"],
            "min_front": score["min_front"],
            "avg_front": score["avg_front"]
        }
        user_scores.append(user_score)

    user_programming_times = calculateProgrammingTimes(db, users)
    user_decision_times = calculateDecisionTimes(db, users)
    user_command_times = calculateCommandTimes(user_programming_times, user_decision_times)
    user_cycle_times = calculateCycleTimes(db, users)

    return render_template('portal/home.html', user_scores=user_scores, programming_times=user_programming_times, decision_times=user_decision_times, command_times=user_command_times, cycle_times=user_cycle_times)


'''The upload page is how users are able to upload
their score files to the database to receive scores
calculated in the functions above. The user must upload
a programming csv file, a pos_programming csv file, a
front csv file, a back csv file, and a text file.'''
@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    if request.method == 'POST':
        db = get_db()
        user = g.user[1]
        upload_time = datetime.now()

        dir_path = current_app.config['UPLOAD_FOLDER']+user+str(datetime.now())
        os.mkdir(dir_path)

        if request.files['programming_file'] != '':
            programming_file = request.files['programming_file']
            table = 'programming'
            parseFile(dir_path, programming_file, user, table, upload_time)

        if request.files['pos_programming_file'] != '':
            pos_programming_file = request.files['pos_programming_file']
            table = 'pos_programming'
            parseFile(dir_path, pos_programming_file, user, table, upload_time)

        if request.files['back_file'] != '':
            back_file = request.files['back_file']
            table = 'back'
            parseFile(dir_path, back_file, user, table, upload_time)

        if request.files['front_file'] != '':
            front_file = request.files['front_file']
            table = 'front'
            parseFile(dir_path, front_file, user, table, upload_time)

        if request.files['text_file'] != '':
            text_file = request.files['text_file']
            table = 'text'
            parseFile(dir_path, text_file, user, table, upload_time)

        return redirect(url_for('portal.home'))

    return render_template('portal/upload.html')


'''The personal stats page shows only the scores
calculated in the functions above for the logged in
user.'''
@bp.route('/personalStats', methods=('GET',))
@login_required
def personalStats():
    db = get_db()
    logged_in_user = g.user[1]
    user = {"username": logged_in_user}

    scores = calculatePerformanceMetrics(db, [user])
    user_scores = []
    for score in scores:
        upload_date = datetime.strptime(score["upload_time"], '%Y-%m-%d %H:%M:%S.%f')
        user_score = {
            "username": score["username"],
            "upload_time": upload_date.strftime('%Y-%m-%d %H:%M'),
            "max_back": score["max_back"],
            "min_back": score["min_back"],
            "avg_back": score["avg_back"],
            "max_front": score["max_front"],
            "min_front": score["min_front"],
            "avg_front": score["avg_front"]
        }
        user_scores.append(user_score)

    programming_times = calculateProgrammingTimes(db, [user])
    decision_times = calculateDecisionTimes(db, [user])
    command_times = calculateCommandTimes(programming_times, decision_times)
    cycle_times = calculateCycleTimes(db, [user])

    return render_template('portal/personalStats.html', user_scores=user_scores, programming_times=programming_times, decision_times=decision_times, command_times=command_times, cycle_times=cycle_times)
