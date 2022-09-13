CREATE SEQUENCE state_items_id_seq;
ALTER SEQUENCE state_items_id_seq OWNER TO statesman;

CREATE TABLE state_items (
    id INT PRIMARY KEY NOT NULL DEFAULT nextval('state_items_id_seq'),
    creator_id VARCHAR(20) NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    collection_id INT REFERENCES state_collections (id) NOT NULL,
    team_id VARCHAR(20) NOT NULL,
    name VARCHAR(50) NOT NULL,
    value VARCHAR(100),
    default_value VARCHAR(100),
    label VARCHAR(50)
);
ALTER TABLE state_items OWNER TO statesman;
