INSERT INTO services (service) 
VALUES ('Counseling')
RETURNING service_id;

'''INSERT INTO services (service) 
VALUES (%(service)s)
RETURNING service_id;''',
    {'service': item['service'][0]}

INSERT INTO services  
VALUES ('Coaching',
 'Consultation',
 'Individual Therapy & Counseling',
 'Marriage, Couples, or Relationship Counseling',
 'Mediation',
 'Telehealth')
;
    

SELECT * FROM age_groups;

SELECT * FROM issues;

SELECT * FROM orientations;

SELECT * FROM professions;

SELECT * FROM services;

SELECT * FROM therapist_age_groups;

SELECT * FROM therapist_issues;

SELECT * FROM therapist_orientations;

SELECT * FROM therapist_professions;

SELECT * FROM therapist_services;

SELECT * FROM therapists;

SELECT * FROM 

SELECT * FROM 

SELECT * FROM 