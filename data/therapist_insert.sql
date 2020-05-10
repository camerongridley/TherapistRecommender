/*Chain your insert with data-modifying CTEs:*/
WITH data(firstname, lastname, adddetails, value) AS (
   VALUES                                 -- provide data here
      (text 'fai55', text 'shaggk', text 'ss', text 'ss2')  -- see below
       --  more?                          -- works for multiple input rows
   )
, ins1 AS (
   INSERT INTO sample (firstname, lastname)
   SELECT firstname, lastname FROM data   -- DISTINCT? see below
   ON     CONFLICT DO NOTHING             -- requires UNIQUE constraint
   RETURNING firstname, lastname, id AS sample_id
   )
, ins2 AS (
   INSERT INTO sample1 (sample_id, adddetails)
   SELECT sample_id, adddetails
   FROM   data
   JOIN   ins1 USING (firstname, lastname)
   RETURNING sample_id, user_id
   )
INSERT INTO sample2 (user_id, value)
SELECT user_id, value
FROM   data
JOIN   ins1 USING (firstname, lastname)
JOIN   ins2 USING (sample_id);



-- anohter example
WITH ins0 AS (
   INSERT INTO siteInfo (siteName, siteHost, notes, ... )
   VALUES ('Sample', 'sample.com', 'note', ... );
   RETURNING siteid
   )
INSERT INTO siteLinks (siteID, URL)
SELECT siteid, 'test'
FROM   ins0;

--Or use lastval() or currval():

BEGIN;

INSERT INTO siteInfo (siteName, siteHost, notes, ... )
VALUES ('Sample', 'sample.com', 'note', ... );

INSERT INTO siteLinks (siteID, URL)
VALUES (lastval(), 'test');

COMMIT;


INSERT INTO therapists (first_name, last_name, address, primary_credential, license_status, website, info_source) 
VALUES ('Bob', 'Barker', '123 Main St.', 'LPC', 'active', 'None','GoodTherapy.com');


INSERT INTO therapists (first_name, last_name, address, 
    primary_credential, license_status, website, 
    info_source, verified, license_num, 
    license_state, years_in_practice, school, 
    year_graduated) 
VALUES ('Marty','McFly','123 Main St',
    'LCSW', 'Avtice','www.google.com',
    'GoodTherapy.com',True,'9837461',
    'CO','13','Yale',
    '1998')
RETURNING therapist_id;

INSERT INTO therapists (first_name, last_name, address, 
    primary_credential, license_status, website, 
    info_source, verified, license_num, 
    license_state, years_in_practice, school, 
    year_graduated) 
VALUES ('George','McFly','123 Main St',
    'LCSW', 'Avtice','www.google.com',
    'GoodTherapy.com',True,'9837461',
    'CO','13','Yale',
    '1998')
RETURNING therapist_id;


INSERT INTO professions (profession) 
VALUES ('Psychotherapist');

INSERT INTO therapist_professions (therapist_id, profession_id)
VALUES (1, 1);


INSERT INTO therapists (first_name, last_name, address, primary_credential, license_status, website, info_source) 
VALUES ('Bob', 'Barker', '123 Main St.', 'LPC', 'active', 'None','GoodTherapy.com');

INSERT INTO therapists (first_name, last_name, address, primary_credential, license_status, website, info_source) 
VALUES ('Vanna', 'White', '123 Main St.', 'LCSW', 'active', 'None','GoodTherapy.com');

INSERT INTO professions (profession)                                                                              
VALUES ('Psychotherapist');

INSERT INTO professions (profession)                                                                              
VALUES ('Counselor');

INSERT INTO professions (profession)                                                                              
VALUES ('Psychologist');

INSERT INTO professions (profession)                                                                              
VALUES ('Social Worker');

INSERT INTO therapist_professions (therapist_id, profession_id)
VALUES (1, 1);

INSERT INTO therapist_professions (therapist_id, profession_id)
VALUES (1, 2);

INSERT INTO therapist_professions (therapist_id, profession_id)
VALUES (2, 2);

INSERT INTO therapist_professions (therapist_id, profession_id)
VALUES (2, 3);
