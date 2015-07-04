DROP TABLE IF EXISTS entries;
CREATE TABLE entries (
    postid INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    title TEXT NOT NULL,
    body TEXT NOT NULL);

DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
    cmtid INTEGER PRIMARY KEY AUTOINCREMENT,
    cmt TEXT NOT NULL,
    user_name TEXT,
    postid INTEGER);
