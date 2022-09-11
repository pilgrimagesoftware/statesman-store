CREATE TABLE users (
    id INT PRIMARY KEY NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id CHAR(20) NOT NULL,
    team_id CHAR(20) NOT NULL,
    current_state_id INT REFERENCES state_collections (id)
);
