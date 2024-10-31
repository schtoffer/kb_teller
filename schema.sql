-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

-- Roles associated with users
CREATE TABLE IF NOT EXISTS user_roles (
    user_id INTEGER,
    role_name TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_name)
);

-- User details with unique email and optional cellphone
CREATE TABLE IF NOT EXISTS user_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usr_fname TEXT NOT NULL,
    usr_lname TEXT NOT NULL,
    usr_email TEXT NOT NULL UNIQUE,
    usr_cellphone TEXT,
    user_id INTEGER NOT NULL UNIQUE,  -- Ensures each user has only one details entry
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Access control table associating users with businesses
CREATE TABLE IF NOT EXISTS user_business_access (
    user_id INTEGER,
    business_id INTEGER,
    PRIMARY KEY (user_id, business_id),  -- Composite primary key allows unique user-business pair
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);

-- Reporting duties table for users associated with businesses
CREATE TABLE IF NOT EXISTS reporting_duties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    business_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);

-- Businesses table
CREATE TABLE IF NOT EXISTS businesses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE  -- Ensures unique business names
);

-- Additional details for each business
CREATE TABLE IF NOT EXISTS business_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL UNIQUE,  -- Ensures each business has only one details entry
    street TEXT,
    post_code TEXT CHECK (LENGTH(post_code) = 4),  -- Enforce 4-character postal code
    city TEXT,
    website_url TEXT,
    FOREIGN KEY (business_id) REFERENCES businesses(id) ON DELETE CASCADE
);