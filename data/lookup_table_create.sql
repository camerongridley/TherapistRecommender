CREATE TABLE therapist_services
(
  therapist_id INT NOT NULL,
  service_id INT NOT NULL,
  --PK is combo of PKs from the 2 tables
  PRIMARY KEY (therapist_id, service_id),
  -- specify role_id as FK referencing account_role table's PK
  CONSTRAINT therapist_services_service_id_fkey FOREIGN KEY (service_id)
      REFERENCES services (service_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
      --
  CONSTRAINT therapist_services_therapist_id_fkey FOREIGN KEY (therapist_id)
      REFERENCES therapists (therapist_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE TABLE therapist_orientations
(
  therapist_id INT NOT NULL,
  orientation_id INT NOT NULL,
  PRIMARY KEY (therapist_id, orientation_id),
  CONSTRAINT therapist_orientations_orientation_id_fkey FOREIGN KEY (orientation_id)
      REFERENCES orientations (orientation_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
      --
  CONSTRAINT therapist_orientations_therapist_id_fkey FOREIGN KEY (therapist_id)
      REFERENCES therapists (therapist_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE TABLE therapist_professions
(
  therapist_id INT NOT NULL,
  profession_id INT NOT NULL,
  PRIMARY KEY (therapist_id, profession_id),
  CONSTRAINT therapist_professions_profession_id_fkey FOREIGN KEY (profession_id)
      REFERENCES professions (profession_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
      --
  CONSTRAINT therapist_professions_therapist_id_fkey FOREIGN KEY (therapist_id)
      REFERENCES therapists (therapist_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE TABLE therapist_age_groups
(
  therapist_id INT NOT NULL,
  age_group_id INT NOT NULL,
  PRIMARY KEY (therapist_id, age_group_id),
  CONSTRAINT therapist_age_groups_age_group_id_fkey FOREIGN KEY (age_group_id)
      REFERENCES age_groups (age_group_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
      --
  CONSTRAINT therapist_age_groups_therapist_id_fkey FOREIGN KEY (therapist_id)
      REFERENCES therapists (therapist_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE TABLE therapist_issues
(
  therapist_id INT NOT NULL,
  issue_id INT NOT NULL,
  PRIMARY KEY (therapist_id, issue_id),
  CONSTRAINT therapist_issues_issue_id_fkey FOREIGN KEY (issue_id)
      REFERENCES issues (issue_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
      --
  CONSTRAINT therapist_issues_therapist_id_fkey FOREIGN KEY (therapist_id)
      REFERENCES therapists (therapist_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
);

CREATE TABLE therapist_writing_samples
(
  therapist_id INT NOT NULL,
  sample_id INT NOT NULL,
  PRIMARY KEY (therapist_id, sample_id),
  CONSTRAINT therapist_writing_samples_sample_id_fkey FOREIGN KEY (sample_id)
      REFERENCES writing_samples (sample_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
      --
  CONSTRAINT therapist_writing_samples_therapist_id_fkey FOREIGN KEY (therapist_id)
      REFERENCES therapists (therapist_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
);








/*****************************************************
EXAMPLE QUERIES
*****************************************************/


CREATE TABLE cascade_test
(
  therapist_id INT NOT NULL,
  test_id INT NOT NULL,
  PRIMARY KEY (therapist_id, test_id),
  CONSTRAINT therapist_tests_test_id_fkey FOREIGN KEY (test_id)
      REFERENCES tests (test_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
      --
  CONSTRAINT therapist_tests_therapist_id_fkey FOREIGN KEY (therapist_id)
      REFERENCES therapists (therapist_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE
);


CREATE TABLE account_role
(
  user_id integer NOT NULL,
  role_id integer NOT NULL,
  grant_date timestamp without time zone,
  PRIMARY KEY (user_id, role_id),
  CONSTRAINT account_role_role_id_fkey FOREIGN KEY (role_id)
      REFERENCES role (role_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT account_role_user_id_fkey FOREIGN KEY (user_id)
      REFERENCES account (user_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);