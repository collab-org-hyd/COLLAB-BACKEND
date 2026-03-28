"""Migration: Add phone_number field to users table

Revision ID: 002_add_phone_number
Depends On: 001_initial
Create Date: 2026-03-23 10:00:00.000000

"""

# This migration adds the phone_number column to the users table
# To apply: update the database.py to run this migration after 001_initial_schema

migration_sql = """
-- Add phone_number column to users table
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);
"""

# Rollback migration (if needed)
rollback_sql = """
-- Remove phone_number column from users table
ALTER TABLE users DROP COLUMN IF EXISTS phone_number;
"""
