CREATE TABLE state_items (
    id INT PRIMARY KEY NOT NULL,
    creator_id CHAR(20) NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    collection_id INT REFERENCES state_collections (id) NOT NULL,
    team_id CHAR(20) NOT NULL,
    name CHAR(50) NOT NULL,
    value CHAR(100),
    default_value CHAR(100),
    label CHAR(50)
);
