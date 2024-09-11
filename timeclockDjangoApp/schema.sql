-- Create the Users table
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email    VARCHAR(100) NOT NULL UNIQUE,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the User_Company table
CREATE TABLE Companies (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    name VARCHAR(50) NOT NULL,
    start_time TIME,
    end_time TIME,
    pay_rate FLOAT CHECK (pay_rate >= 0.0) DEFAULT 0.0,
    start_date DATE NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Company_Shift table
CREATE TABLE Shifts (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES Companies(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    shift_type VARCHAR(50) NOT NULL,
    lunch_break FLOAT CHECK (lunch_break >= 0.0),
    worked_hours FLOAT DEFAULT 0.0,
    notes TEXT,
    work_date DATE NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Time_Off table
CREATE TABLE Time_Off (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES Companies(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    vacation_hours FLOAT CHECK (vacation_hours >= 0.0) DEFAULT 0.0,
    sick_hours FLOAT CHECK (sick_hours >= 0.0) DEFAULT 0.0,
    dayoff_type VARCHAR(50) NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

