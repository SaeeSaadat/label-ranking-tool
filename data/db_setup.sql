CREATE TABLE users
(
    username TEXT PRIMARY KEY NOT NULL,
    group_id INTEGER NOT NULL,
    real_name TEXT DEFAULT NULL
);


CREATE TABLE methods
(
    method_id          INTEGER PRIMARY KEY NOT NULL,
    method_description TEXT                NOT NULL
);


CREATE TABLE submissions
(
    row_num         INTEGER   NOT NULL,
    username        TEXT      NOT NULL,
    informal_text   TEXT      NOT NULL,
    answers         TEXT      NOT NULL, -- 1,2,4,3 = 1 > 2 > 4 > 3
    submission_time TIMESTAMP NOT NULL,

    PRIMARY KEY (row_num, username),
    FOREIGN KEY (row_num) REFERENCES informals (row_num),
    FOREIGN KEY (username) REFERENCES users (username)
);


CREATE TABLE informals
(
    row_num       INTEGER PRIMARY KEY,
    informal_text TEXT NOT NULL,
    group1_answered INTEGER DEFAULT 0,
    group2_answered INTEGER DEFAULT 0
);

CREATE TABLE formals
(
    row_num     INTEGER,
    formal_text TEXT NOT NULL,
    method_id   INTEGER NOT NULL,

    PRIMARY KEY (row_num, method_id),
    FOREIGN KEY (row_num) REFERENCES informals (row_num),
    FOREIGN KEY (method_id) REFERENCES methods (method_id)
);

INSERT INTO methods (method_id, method_description) VALUES (1, 'GPT2 TRAINED ON HANDMADE DATA');
INSERT INTO methods (method_id, method_description) VALUES (2, 'GPT2 TRAINED ON FULL DATA');
INSERT INTO methods (method_id, method_description) VALUES (3, 'T5 TRAINED ON HANDMADE DATA');
INSERT INTO methods (method_id, method_description) VALUES (4, 'T5 TRAINED ON FULL DATA');
INSERT INTO methods (method_id, method_description) VALUES (5, 'FARSIYAR');
INSERT INTO methods (method_id, method_description) VALUES (6, 'CHAT GPT');


INSERT INTO users (username, group_id) VALUES ('user1', 1);
INSERT INTO users (username, group_id) VALUES ('user2', 2);
INSERT INTO users (username, group_id) VALUES ('user3', 1);
INSERT INTO users (username, group_id) VALUES ('user4', 2);
INSERT INTO users (username, group_id) VALUES ('user5', 1);
INSERT INTO users (username, group_id) VALUES ('user6', 2);
INSERT INTO users (username, group_id) VALUES ('user7', 1);
INSERT INTO users (username, group_id) VALUES ('user8', 2);
INSERT INTO users (username, group_id) VALUES ('user9', 1);
INSERT INTO users (username, group_id) VALUES ('user10', 2);
INSERT INTO users (username, group_id) VALUES ('user11', 1);
INSERT INTO users (username, group_id) VALUES ('user12', 2);