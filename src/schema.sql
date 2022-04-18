DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS programming;
DROP TABLE IF EXISTS pos_programming;
DROP TABLE IF EXISTS back;
DROP TABLE IF EXISTS front;
DROP TABLE IF EXISTS text;
DROP TABLE IF EXISTS tasklog;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE programming (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	filepath TEXT NOT NULL,
	timestamp REAL,
	Timestamp_Realtime TEXT,
	target_TCP_speed_0 REAL,
	target_TCP_speed_1 REAL,
	target_TCP_speed_2 REAL,
	target_TCP_speed_3 REAL,
	target_TCP_speed_4 REAL,
	target_TCP_speed_5 REAL,
	upload_time TEXT,
	FOREIGN KEY(username) REFERENCES user(username)
);

CREATE TABLE pos_programming (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	filepath TEXT NOT NULL,
	timestamp REAL,
	Timestamp_Realtime TEXT,
	target_q_0 REAL,
	target_q_1 REAL,
	target_q_2 REAL,
	target_q_3 REAL,
	target_q_4 REAL,
	target_q_5 REAL,
	upload_time TEXT,
	FOREIGN KEY(username) REFERENCES user(username)
);

CREATE TABLE back (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	filepath TEXT NOT NULL,
	timestamp REAL,
	Timestamp_Realtime TEXT,
	back_score REAL,
	upload_time TEXT,
	FOREIGN KEY(username) REFERENCES user(username)
);

CREATE TABLE front (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	filepath TEXT NOT NULL,
	timestamp REAL,
	Timestamp_Realtime TEXT,
	front_score REAL,
	upload_time TEXT,
	FOREIGN KEY(username) REFERENCES user(username)
);

CREATE TABLE text (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	filepath TEXT NOT NULL,
	file_text TEXT,
	upload_time TEXT,
	FOREIGN KEY(username) REFERENCES user(username)
);

CREATE TABLE tasklog (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  type TEXT NOT NULL,
  description TEXT NOT NULL
);
