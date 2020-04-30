CREATE TABLE therapists(
    therapist_id serial PRIMARY KEY,
    first_name VARCHAR (50) NOT NULL,
    last_name VARCHAR (50) NOT NULL,
    address VARCHAR (200) ,
    primary_credential VARCHAR (150) ,
    license_status VARCHAR (100) ,
    website VARCHAR (300) ,
    info_source VARCHAR (200) ,
    creation_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);