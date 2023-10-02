DROP SCHEMA IF EXISTS badgesystem CASCADE;
CREATE SCHEMA badgesystem;
SET search_path TO 'badgesystem';

DROP TABLE IF EXISTS Badge CASCADE;
DROP TABLE IF EXISTS Student CASCADE;
DROP TABLE IF EXISTS Staff CASCADE;
DROP TABLE IF EXISTS AwardedBadge CASCADE;

CREATE TABLE IF NOT EXISTS Badge (
    id SERIAL PRIMARY KEY NOT NULL,
    title VARCHAR(50) NOT NULL,
    description VARCHAR(500) NOT NULL
);

CREATE TABLE IF NOT EXISTS Student (
	id VARCHAR(64) PRIMARY KEY NOT NULL,
  	name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Staff (
	id SERIAL PRIMARY KEY NOT NULL,
  	name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL,
  	password VARCHAR(200) NOT NULL,
	curricular INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS AwardedBadge (
	id VARCHAR(500) NOT NULL UNIQUE,
  	badge_id INTEGER NOT NULL REFERENCES Badge(id) ON DELETE CASCADE, -- delete this AwardedBadge if the badge is deleted
  	student_id VARCHAR(64) NOT NULL REFERENCES Student(id) ON DELETE CASCADE, -- delete this AwardedBadge if the student is deleted
  	issued_by INTEGER NOT NULL REFERENCES Staff(id),
	date_issued DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
	issued_for VARCHAR(500) NOT NULL,
	image_url VARCHAR(50) DEFAULT 'badge_placeholder.webp'
);

--
--	Adding 'Dummy' Data for demonstrating the system
--
INSERT INTO Student(id, name) VALUES('e9cee71ab932fde863338d08be4de9dfe39ea049bdafb342ce659ec5450b69ae', 'Jason Bourne'); -- unikey is: abcd1234
INSERT INTO Student(id, name) VALUES('a488c73235f23320b3a730ecfb70f0249289561f7436fab597297601291c8213', 'Bob'); -- unikey is: efgh5678

INSERT INTO Badge(title, description) VALUES('Leadership', 'Demonstrated leadership in group work');
INSERT INTO Badge(title, description) VALUES('Teamwork', 'Worked well in a group');
INSERT INTO Badge(title, description) VALUES('Ethics', 'demonstrate an understanding of how to make a positive impact within the business environment and plan for a sustainable and ethical approach to societal challenges.');
INSERT INTO Badge(title, description) VALUES('Communication', 'communicate effectively, both orally and in writing, using a range of modes of communication including presentations and writing effectively to different audiences');
INSERT INTO Badge(title, description) VALUES('Critical thinking and problem solving', 'he questioning of ideas, evidence and assumptions in order to propose and evaluate hypotheses or alternative arguments before formulating a conclusion or a solution to an identified problem.');
INSERT INTO Badge(title, description) VALUES('Perseverance', 'Never gives up!');

INSERT INTO Staff(name, username, password, curricular) VALUES('Professor Barney', 'barney', '$2a$12$QKuhqfVs8ikLU6DZrG8i6.FKRZDaKHyt.//GCLhDiEA8FJbsp/j9y',1);
INSERT INTO Staff(name, username, password, curricular) VALUES('Homer', 'homer', '$2a$12$QKuhqfVs8ikLU6DZrG8i6.FKRZDaKHyt.//GCLhDiEA8FJbsp/j9y',0);
INSERT INTO Staff(name, username, password, curricular) VALUES('Marge', 'marge', '$2a$12$QKuhqfVs8ikLU6DZrG8i6.FKRZDaKHyt.//GCLhDiEA8FJbsp/j9y',0);
INSERT INTO Staff(name, username, password, curricular) VALUES('Bart', 'bart', '$2a$12$QKuhqfVs8ikLU6DZrG8i6.FKRZDaKHyt.//GCLhDiEA8FJbsp/j9y',0);
INSERT INTO Staff(name, username, password, curricular) VALUES('Lisa', 'lisa', '$2a$12$QKuhqfVs8ikLU6DZrG8i6.FKRZDaKHyt.//GCLhDiEA8FJbsp/j9y',0);

INSERT INTO AwardedBadge(id, badge_id, student_id, issued_by, issued_for, image_url) VALUES('86f7e437faa5a7fce15d1ddcb9eaeaea377667b8', 1, 'e9cee71ab932fde863338d08be4de9dfe39ea049bdafb342ce659ec5450b69ae', 1, 'Great leadership in SOFT2201. I can definitely see you have grown both as a student and a professional during your time in this subject! Keep it up!', 'leadership.png');
INSERT INTO AwardedBadge(id, badge_id, student_id, issued_by, issued_for, image_url) VALUES('86f7e437faa5a7fce15d1ddcb9aksjsh377667b81', 4, 'e9cee71ab932fde863338d08be4de9dfe39ea049bdafb342ce659ec5450b69ae', 3, 'this is test data', 'speech-bubble.png');
INSERT INTO AwardedBadge(id, badge_id, student_id, issued_by, issued_for, image_url) VALUES('86f7e437faa5a7fce15d1ddcb9aksjsh377667b82', 3, 'e9cee71ab932fde863338d08be4de9dfe39ea049bdafb342ce659ec5450b69ae', 2, 'teamwork in SOFT2201', 'ethical.png');
INSERT INTO AwardedBadge(id, badge_id, student_id, issued_by, issued_for, image_url) VALUES('86f7e437faa5a7fce15d1ddcb9aksjsh377667b83', 2, 'e9cee71ab932fde863338d08be4de9dfe39ea049bdafb342ce659ec5450b69ae', 2, 'more data becasue I ran out of ideas', 'support.png');
INSERT INTO AwardedBadge(id, badge_id, student_id, issued_by, issued_for, image_url) VALUES('86f7e437faa5a7fce15d1ddcb9eaeaea377667b9', 6, 'e9cee71ab932fde863338d08be4de9dfe39ea049bdafb342ce659ec5450b69ae', 1, 'A great Client demo!', 'struggle.png');
INSERT INTO AwardedBadge(id, badge_id, student_id, issued_by, issued_for, image_url) VALUES('86f7e437faa5aasdflkjh7fce15d1ddcb9eaeaea', 2, 'a488c73235f23320b3a730ecfb70f0249289561f7436fab597297601291c8213', 2, 'Good work in presentation', 'support.png');
