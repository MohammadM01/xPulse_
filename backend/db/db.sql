-- connect as postgres system user, then run:

-- 1) create the DB and user (user already named "postgres" in your env; skip user creation if it already exists)
CREATE USER postgres WITH PASSWORD 'password';
CREATE DATABASE xpulse_tribunal OWNER postgres;

-- 2) connect to the DB (from shell: psql -U postgres -d xpulse_tribunal)
\c xpulse_tribunal

-- 3) create table to store these env entries
CREATE TABLE env_vars (
  id SERIAL PRIMARY KEY,
  key TEXT NOT NULL UNIQUE,
  value TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 4) insert the values from your screenshot
INSERT INTO env_vars (key, value) VALUES
('POSTGRES_USER','postgres'),
('POSTGRES_PASSWORD','password'),
('POSTGRES_SERVER','localhost'),
('POSTGRES_PORT','5432'),
('POSTGRES_DB','xpulse_tribunal'),
('REDIS_HOST','localhost'),
('REDIS_PORT','6379');

-- 5) verify
SELECT * FROM env_vars ORDER BY id;
