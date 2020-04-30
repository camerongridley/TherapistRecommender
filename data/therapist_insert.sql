/*Chain your insert with data-modifying CTEs:*/

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
