CREATE TABLE services(
	service_id serial PRIMARY KEY,
	service VARCHAR (255) UNIQUE NOT NULL
);

CREATE TABLE orientations(
	orientation_id serial PRIMARY KEY,
	orientation VARCHAR (255) UNIQUE NOT NULL
);

CREATE TABLE professions(
	profession_id serial PRIMARY KEY,
	profession VARCHAR (255) UNIQUE NOT NULL
);

CREATE TABLE age_groups(
	age_group_id serial PRIMARY KEY,
	age_group INT UNIQUE NOT NULL
);

CREATE TABLE issues(
	issue_id serial PRIMARY KEY,
	issue VARCHAR (255) UNIQUE NOT NULL
);

CREATE TABLE writing_samples(
	sample_id serial PRIMARY KEY,
	sample TEXT NOT NULL, 
	source VARCHAR (255) 
);
