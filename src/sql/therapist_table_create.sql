CREATE TABLE therapists(
    therapist_id serial PRIMARY KEY,
    first_name VARCHAR (50) NOT NULL,
    last_name VARCHAR (50) NOT NULL,
    address VARCHAR (200) ,
    primary_credential VARCHAR (150) ,
    license_status VARCHAR (100) ,
    website VARCHAR (300) ,
    info_source VARCHAR (200) ,
    verified Boolean NOT NULL DEFAULT FALSE,
    license_num Integer UNIQUE,
    license_state VARCHAR (5),
    years_in_practice Integer,
    school VARCHAR (100),
    year_graduated Integer,
    creation_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
    UNIQUE (first_name, last_name)
);