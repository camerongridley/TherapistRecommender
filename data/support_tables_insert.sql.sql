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


