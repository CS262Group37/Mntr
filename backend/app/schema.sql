DROP TABLE IF EXISTS system_business_area CASCADE;
DROP TABLE IF EXISTS system_topic CASCADE;
DROP TABLE IF EXISTS system_skill CASCADE;
DROP TABLE IF EXISTS account CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS user_topic CASCADE;
DROP TABLE IF EXISTS user_rating CASCADE;
DROP TABLE IF EXISTS "message" CASCADE;
DROP TABLE IF EXISTS relation CASCADE;
DROP TABLE IF EXISTS report CASCADE;
DROP TABLE IF EXISTS plan_of_action CASCADE;
DROP TABLE IF EXISTS meeting CASCADE;
DROP TABLE IF EXISTS message_meeting CASCADE;
DROP TABLE IF EXISTS message_email CASCADE;
DROP TABLE IF EXISTS workshop CASCADE;
DROP TABLE IF EXISTS message_workshop_invite CASCADE;
DROP TABLE IF EXISTS user_workshop CASCADE;
DROP TABLE IF EXISTS workshop_demand CASCADE;

-- Constraint functions --
DROP FUNCTION IF EXISTS relation_constraints;
DROP TRIGGER IF EXISTS relation_constraints ON relation;

CREATE TABLE system_business_area (
    businessAreaID SERIAL PRIMARY KEY,
    "name" VARCHAR NOT NULL CONSTRAINT unique_area_name UNIQUE
);

CREATE TABLE system_topic (
    topicID SERIAL PRIMARY KEY,
    "name" VARCHAR NOT NULL CONSTRAINT unique_topic UNIQUE
);

CREATE TABLE system_skill (
    skillID SERIAL PRIMARY KEY,
    "name" VARCHAR NOT NULL CONSTRAINT unique_skill UNIQUE
);

CREATE TABLE account (
    accountID SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL CONSTRAINT unique_email UNIQUE,
    "password" VARCHAR NOT NULL,
    firstName VARCHAR NOT NULL,
    lastName VARCHAR NOT NULL,
    profilePicture VARCHAR
);

CREATE TABLE "user" (
    userID SERIAL PRIMARY KEY,
    accountID INTEGER REFERENCES account(accountID),
    "role" VARCHAR NOT NULL CONSTRAINT invalid_role CHECK ("role" IN ('mentee', 'mentor', 'admin')),
    -- businessArea can be NULL for admin users
    businessArea VARCHAR CONSTRAINT valid_business_area REFERENCES system_business_area("name"),
    CONSTRAINT one_role_per_account UNIQUE (accountID, "role")
);

CREATE TABLE user_topic (
    userID INTEGER NOT NULL REFERENCES "user"(userID),
    topic VARCHAR NOT NULL CONSTRAINT valid_topic REFERENCES system_topic("name"),
    PRIMARY KEY (userID, topic)
);

CREATE TABLE user_rating (
    userID INTEGER NOT NULL REFERENCES "user"(userID),
    skill VARCHAR NOT NULL CONSTRAINT valid_skill REFERENCES system_skill("name"),
    rating INTEGER NOT NULL CONSTRAINT valid_rating CHECK (rating >= 0 AND rating <= 10),
    PRIMARY KEY (userID, skill)
);

CREATE TABLE relation (
    relationID SERIAL PRIMARY KEY, 
    -- We need a way to check that the mentorID and menteeID are actually users with mentor and mentee roles.
    -- I think we might need to use a trigger for this.
    menteeID INTEGER NOT NULL REFERENCES "user"(userID),
    mentorID INTEGER NOT NULL REFERENCES "user"(userID),
    CONSTRAINT unique_relation UNIQUE (mentorID, menteeID)
);

CREATE TABLE meeting (
    meetingID SERIAL PRIMARY KEY,
    relationID INTEGER NOT NULL REFERENCES relation(relationID),
    startTime TIMESTAMP NOT NULL,
    endTime TIMESTAMP NOT NULL,
    title VARCHAR NOT NULL,
    "description" VARCHAR NOT NULL,
    "status" VARCHAR NOT NULL CONSTRAINT acceptable_status CHECK ("status" IN ('going-ahead', 'pending', 'cancelled', 'completed', 'missed', 'running')),
    feedback VARCHAR
);

CREATE TABLE "message" (
    messageID SERIAL PRIMARY KEY,
    recipientID INTEGER NOT NULL REFERENCES "user"(userID),
    senderID INTEGER NOT NULL REFERENCES "user"(userID),
    messageType VARCHAR NOT NULL CONSTRAINT valid_message_type CHECK (messageType IN ('MeetingMessage', 'Email', 'WorkshopInvite', 'Report')),
    sentTime TIMESTAMP NOT NULL,
    CONSTRAINT distinct_recipient_and_sender CHECK (recipientID <> senderID)
);

CREATE TABLE message_meeting(
    messageID INTEGER REFERENCES "message"(messageID),
    meetingMessageType VARCHAR NOT NULL CONSTRAINT valid_meeting_message_type CHECK (meetingMessageType IN ('request', 'complete')),
    meetingID INTEGER REFERENCES meeting(meetingID)
);

CREATE TABLE message_email(
    messageID INTEGER REFERENCES "message"(messageID),
    "subject" VARCHAR NOT NULL,
    content VARCHAR NOT NULL
);

CREATE TABLE message_report(
    messageID INTEGER REFERENCES "message"(messageID),
    reportID INTEGER REFERENCES report(reportID)
);

CREATE TABLE report (
    reportID SERIAL PRIMARY KEY,
    userID INTEGER NOT NULL REFERENCES "user"(userID),
    content VARCHAR NOT NULL,
    "status" VARCHAR NOT NULL CONSTRAINT valid_status CHECK ("status" IN ('read', 'unread'))
);

CREATE TABLE workshop (
    workshopID SERIAL PRIMARY KEY,
    topic VARCHAR NOT NULL CONSTRAINT valid_topic REFERENCES system_topic("name"),
    mentorID INTEGER NOT NULL REFERENCES "user"(userID),
    title VARCHAR NOT NULL,
    "description" VARCHAR NOT NULL,
    startTime TIMESTAMP NOT NULL,
    endTime TIMESTAMP NOT NULL,
    "status" VARCHAR NOT NULL CONSTRAINT valid_status CHECK ("status" IN ('going-ahead', 'cancelled', 'running', 'completed')),
    "location" VARCHAR NOT NULL
);

CREATE TABLE user_workshop (
    menteeID INTEGER NOT NULL REFERENCES "user"(userID),
    workshopID INTEGER NOT NULL REFERENCES workshop
);

CREATE TABLE message_workshop_invite (
    messageID INTEGER NOT NULL REFERENCES "message"(messageID),
    content VARCHAR NOT NULL,
    workshopID INTEGER REFERENCES workshop
);

CREATE TABLE workshop_demand (
    topic VARCHAR PRIMARY KEY REFERENCES system_topic("name"),
    demand NUMERIC NOT NULL
);

CREATE TABLE plan_of_action (
    planOfActionID SERIAL PRIMARY KEY,
    relationID INTEGER NOT NULL REFERENCES relation(relationID),
    title VARCHAR NOT NULL,
    "description" VARCHAR NOT NULL,
    creationDate TIMESTAMP NOT NULL,
    "status" VARCHAR NOT NULL CONSTRAINT valid_status CHECK ("status" IN ('complete', 'incomplete'))
);

-------------------- Relation Trigger --------------------

CREATE OR REPLACE FUNCTION relation_constraints()
RETURNS TRIGGER AS
$$
DECLARE
    menteeAccountID INTEGER;
    mentorAccountID INTEGER;
    menteeRole VARCHAR;
    mentorRole VARCHAR;
    menteeBusinessArea VARCHAR;
    mentorBusinessArea VARCHAR;
BEGIN
    -- Get account IDs and roles
    SELECT accountID, "role", businessArea INTO menteeAccountID, menteeRole, menteeBusinessArea FROM "user" WHERE userID = new.menteeID;
    SELECT accountID, "role", businessArea INTO mentorAccountID, mentorRole, mentorBusinessArea FROM "user" WHERE userID = new.mentorID;

    IF menteeAccountID = mentorAccountID THEN
        RAISE EXCEPTION 'Invalid relation. Mentor and mentee have the same account';
    END IF;

    IF menteeRole != 'mentee' THEN
        RAISE EXCEPTION 'User with menteeID % is not a mentee', new.menteeID;
    END IF;

    IF mentorRole != 'mentor' THEN
        RAISE EXCEPTION 'User with mentorID % is not a mentor', new.mentorID;
    END IF;

    if menteeBusinessArea = mentorBusinessArea THEN
        RAISE EXCEPTION 'Invalid relation. Mentor and mentee have the same business area';
    END IF;

    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER relation_constraints BEFORE INSERT OR UPDATE ON relation
    FOR EACH ROW EXECUTE PROCEDURE relation_constraints();