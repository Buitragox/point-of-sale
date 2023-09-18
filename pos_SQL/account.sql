CREATE TABLE IF NOT EXISTS account.role_account(
    role_id SERIAL PRIMARY KEY,
    role_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS account.user_account(
    user_id UUID PRIMARY KEY,
    user_name TEXT NOT NULL,
    user_password TEXT NOT NULL,
    user_role INTEGER NOT NULL,
    user_state INTEGER,
    CONSTRAINT fk_user_role FOREIGN KEY (user_role) references account.role_account(role_id)
);