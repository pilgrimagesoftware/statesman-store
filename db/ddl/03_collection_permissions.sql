CREATE SEQUENCE collection_permissions_id_seq;
ALTER SEQUENCE collection_permissions_id_seq OWNER TO statesman;

CREATE TABLE collection_permissions (
    id INT PRIMARY KEY NOT NULL DEFAULT nextval('collection_permissions_id_seq'),
    created_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT REFERENCES users (id),
    collection_id INT REFERENCES state_collections (id),
    permission VARCHAR(10) DEFAULT 'read'
);
ALTER TABLE collection_permissions OWNER TO statesman;
