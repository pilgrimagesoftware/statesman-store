
CREATE SEQUENCE state_collection_id_seq;
ALTER SEQUENCE state_collection_id_seq OWNER TO statesman;

CREATE TABLE state_collections (
    id INT PRIMARY KEY NOT NULL DEFAULT nextval('state_collection_id_seq'),
    creator_id VARCHAR(20) NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    team_id VARCHAR(20) NOT NULL,
    name VARCHAR(50) NOT NULL
);
ALTER TABLE state_collections OWNER TO statesman;
