CREATE SEQUENCE item_permissions_id_seq;
ALTER SEQUENCE item_permissions_id_seq OWNER TO statesman;

CREATE TABLE item_permissions (
    id INT PRIMARY KEY NOT NULL DEFAULT nextval('item_permissions_id_seq'),
    created_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT REFERENCES users (id),
    item_id INT REFERENCES state_items (id),
    permission VARCHAR(10) DEFAULT 'read'
);
ALTER TABLE item_permissions OWNER TO statesman;
