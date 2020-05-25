DELETE FROM therapists;

DELETE FROM issues WHERE issue_id >=245;

DELETE FROM orientations WHERE orientation_id >= 252;

DELETE FROM age_groups;

DELETE FROM professions;

DELETE FROM services;

DELETE FROM therapist_age_groups;

DELETE FROM therapist_issues;

DELETE FROM therapist_orientations;

DELETE FROM therapist_professions;

DELETE FROM therapist_services;


ALTER SEQUENCE therapists_therapist_id_seq RESTART WITH 1;

ALTER SEQUENCE age_groups_age_group_id_seq RESTART WITH 1;

ALTER SEQUENCE issues_issue_id_seq RESTART WITH 1;

ALTER SEQUENCE  professions_profession_id_seq RESTART WITH 1;

ALTER SEQUENCE services_service_id_seq RESTART WITH 1;



