ALTER TABLE therapists
ADD COLUMN verified Boolean NOT NULL DEFAULT FALSE,
ADD COLUMN license_num Integer,
ADD COLUMN license_state VARCHAR (5),
ADD COLUMN years_in_practice Integer,
ADD COLUMN school VARCHAR (100),
ADD COLUMN year_graduated Integer;