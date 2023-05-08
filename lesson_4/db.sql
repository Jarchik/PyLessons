CREATE TABLE user(ID INTEGER PRIMARY KEY AUTOINCREMENT, Name varchar(100) NOT NULL, Language varchar(15) NOT NULL, Course varchar(255), Grade INTEGER);
CREATE UNIQUE INDEX uidx_uname ON User (Name);
INSERT INTO user(Name, Language, Course, Grade) VALUES ('John', 'ukr', 'Python Pro', 10);
INSERT INTO user(Name, Language, Course, Grade) VALUES ('Wick', 'eng', 'Python Pro', 12);