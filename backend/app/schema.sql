DROP TABLE IF EXISTS account CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS "message" CASCADE;
DROP TABLE IF EXISTS relation CASCADE;
DROP TABLE IF EXISTS system_business_area CASCADE;
DROP TABLE IF EXISTS system_topic CASCADE;
DROP TABLE IF EXISTS system_skill CASCADE;
DROP TABLE IF EXISTS rating CASCADE;
DROP TABLE IF EXISTS report CASCADE;

-- Constraint functions --
DROP FUNCTION IF EXISTS add_relation_contraints;
DROP TRIGGER IF EXISTS add_relation_contraints ON relation;

CREATE TABLE system_business_area (
    businessAreaID SERIAL PRIMARY KEY,
    "name" VARCHAR NOT NULL CONSTRAINT unique_area_name UNIQUE
);

CREATE TABLE account (
    accountID SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL CONSTRAINT unique_email UNIQUE,
    "password" VARCHAR NOT NULL,
    firstName VARCHAR NOT NULL,
    lastName VARCHAR NOT NULL,
    businessArea VARCHAR NOT NULL CONSTRAINT valid_business_area REFERENCES system_business_area("name")
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
    messageType VARCHAR NOT NULL CONSTRAINT valid_message_type CHECK (messageType IN ('email', 'feedback', 'report')),
    sentTime TIMESTAMP NOT NULL, 
    CONSTRAINT distinct_recipient_and_sender CHECK (recipientID <> senderID)
);

CREATE TABLE relation (
    relationID SERIAL PRIMARY KEY, 
    -- We need a way to check that the mentorID and menteeID are actually users with mentor and mentee roles.
    -- I think we might need to use a trigger for this.
    menteeID INTEGER NOT NULL REFERENCES "user"(userID),
    mentorID INTEGER NOT NULL REFERENCES "user"(userID),
    CONSTRAINT unique_relation UNIQUE (mentorID, menteeID)
);

CREATE TABLE system_topic (
    topicID SERIAL PRIMARY KEY,
    "name" VARCHAR NOT NULL CONSTRAINT unique_topic UNIQUE
);

CREATE TABLE system_skill (
    skillID SERIAL PRIMARY KEY,
    "name" VARCHAR NOT NULL CONSTRAINT unique_skill UNIQUE
);

-- Contains user's ratings for skills
CREATE TABLE rating (
    userID INTEGER NOT NULL REFERENCES "user"(userID),
    skillID INTEGER NOT NULL REFERENCES system_skill(skillID),
    rating INTEGER NOT NULL CONSTRAINT valid_rating CHECK (rating >= 0 AND rating <= 10)
);

CREATE TABLE report (
    reportID SERIAL PRIMARY KEY,
    userID INTEGER NOT NULL REFERENCES "user"(userID),
    content VARCHAR NOT NULL,
    "status" VARCHAR NOT NULL CONSTRAINT valid_status CHECK ("status" IN ('read', 'unread'))
);

-------------------- Relation Trigger --------------------

CREATE OR REPLACE FUNCTION add_relation_contraints()
RETURNS TRIGGER AS
$$
DECLARE
    menteeAccountID INTEGER;
    mentorAccountID INTEGER;
    menteeRole VARCHAR;
    mentorRole VARCHAR;
BEGIN
    -- Get account IDs and roles
    SELECT accountID, "role" INTO menteeAccountID, menteeRole FROM "user" WHERE userID = new.menteeID;
    SELECT accountID, "role" INTO mentorAccountID, mentorRole FROM "user" WHERE userID = new.mentorID;

    IF menteeAccountID = mentorAccountID THEN
        RAISE EXCEPTION 'Cannot add relation. Mentor and mentee have the same account';
    END IF;

    IF menteeRole != 'mentee' THEN
        RAISE EXCEPTION 'User with menteeID % is not a mentee', new.menteeID;
    END IF;

    IF mentorRole != 'mentor' THEN
        RAISE EXCEPTION 'User with mentorID % is not a mentor', new.mentorID;
    END IF;

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER add_relation_contraints BEFORE INSERT OR UPDATE ON relation
    FOR EACH ROW EXECUTE PROCEDURE add_relation_contraints();
