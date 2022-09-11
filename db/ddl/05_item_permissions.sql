CREATE TABLE item_permissions (
    id INT PRIMARY KEY NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT REFERENCES users (id),
    item_id INT REFERENCES state_items (id),
    permission CHAR(10) DEFAULT 'read'
);
