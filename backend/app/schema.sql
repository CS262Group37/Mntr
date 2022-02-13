DROP TABLE IF EXISTS "user" CASCADE;

CREATE TABLE "user" (
    userID SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL UNIQUE,
    "password" VARCHAR NOT NULL,
    firstName VARCHAR NOT NULL,
    lastName VARCHAR NOT NULL,
    "role" VARCHAR NOT NULL CHECK ("role" IN ('mentee', 'mentor', 'admin'))
);
