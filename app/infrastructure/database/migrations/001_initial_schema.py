"""Initial migration: Create users and auth_credentials tables

Revision ID: 001_initial
Create Date: 2026-03-15 00:00:00.000000

"""

# This migration creates the initial schema with Users and AuthCredentials tables
# To apply: update the database.py to call Base.metadata.create_all(engine)

migration_sql = """
-- Create enum type for user roles
CREATE TYPE user_role AS ENUM ('customer', 'influencer', 'admin');

-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    role user_role DEFAULT 'customer' NOT NULL,
    is_influencer BOOLEAN DEFAULT FALSE NOT NULL,
    tags TEXT,
    can_request_service BOOLEAN DEFAULT TRUE NOT NULL,
    can_fulfill_service BOOLEAN DEFAULT FALSE NOT NULL,
    bio TEXT,
    business_link VARCHAR(500),
    yt_link VARCHAR(500),
    x_link VARCHAR(500),
    facebook_link VARCHAR(500),
    other_link VARCHAR(500),
    what_to_expect TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT valid_email CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$')
);

-- Create indexes on users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- Create auth_credentials table
CREATE TABLE auth_credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create indexes on auth_credentials
CREATE INDEX idx_auth_credentials_user_id ON auth_credentials(user_id);
"""
