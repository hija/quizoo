DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS question;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL COLLATE nocase,
  mail TEXT UNIQUE NOT NULL COLLATE nocase,
  firstname TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE question (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  question_json TEXT NOT NULL, -- I am too lazy to generate the best fitting datastructure, so we are just going to add json here
  FOREIGN KEY (user_id) REFERENCES user (id)
);