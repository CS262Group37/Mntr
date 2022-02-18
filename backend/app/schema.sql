DROP TABLE IF EXISTS "account" CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS "message" CASCADE;
DROP TABLE IF EXISTS "relation" CASCADE;

CREATE TABLE account (
    accountID SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL CONSTRAINT unique_email UNIQUE,
    "password" VARCHAR NOT NULL,
    firstName VARCHAR NOT NULL,
    lastName VARCHAR NOT NULL
);

CREATE TABLE "user" (
    userID SERIAL PRIMARY KEY,
    accountID INTEGER REFERENCES account(accountID),
    "role" VARCHAR NOT NULL CONSTRAINT invalid_role CHECK ("role" IN ('mentee', 'mentor', 'admin')),
    CONSTRAINT one_role_per_account UNIQUE (accountID, "role")
);

CREATE TABLE "message" (
    messageID SERIAL PRIMARY KEY,
    recipientID INTEGER NOT NULL REFERENCES "user"(userID),
    senderID INTEGER NOT NULL REFERENCES "user"(userID),
    messageType VARCHAR CHECK (messageType IN ('email', 'feedback', 'report')) NOT NULL,
    sentTime TIMESTAMP NOT NULL, 
    CONSTRAINT distinct_recipient_and_sender CHECK (recipientID <> senderID)
);

CREATE TABLE relation (
    relationID SERIAL PRIMARY KEY, 
    -- We need a way to check that the mentorID and menteeID are actually users with mentor and mentee roles.
    -- I think we might need to use a trigger for this.
    mentorID INTEGER NOT NULL REFERENCES "user"(userID),
    menteeID INTEGER NOT NULL REFERENCES "user"(userID),
    CONSTRAINT unique_relation UNIQUE (mentorID, menteeID)
);
