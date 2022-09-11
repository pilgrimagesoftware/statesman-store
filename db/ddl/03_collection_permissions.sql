CREATE TABLE collection_permissions (
    id INT PRIMARY KEY NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT REFERENCES users (id),
    collection_id INT REFERENCES state_collections (id),
    permission CHAR(10) DEFAULT 'read'
);
ALTER TABLE collection_permissions OWNER TO statesman;
