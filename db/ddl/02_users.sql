CREATE SEQUENCE user_id_seq;
ALTER SEQUENCE user_id_seq OWNER TO statesman;

CREATE TABLE users (
    id INT PRIMARY KEY NOT NULL DEFAULT nextval('user_id_seq'),
    created_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id CHAR(20) NOT NULL,
    team_id CHAR(20) NOT NULL,
    current_state_id INT REFERENCES state_collections (id)
);
ALTER TABLE users OWNER TO statesman;
