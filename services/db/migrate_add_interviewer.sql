-- Migration: Add interviewer column to interviews table
-- Date: 2025-01-17
-- Purpose: Fix database schema issue for interview scheduling

-- Check if column exists and add if missing
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'interviews' AND column_name = 'interviewer'
    ) THEN
        ALTER TABLE interviews ADD COLUMN interviewer VARCHAR(255) DEFAULT 'HR Team';
        
        -- Update existing records
        UPDATE interviews SET interviewer = 'HR Team' WHERE interviewer IS NULL;
        
        -- Add index for performance
        CREATE INDEX IF NOT EXISTS idx_interviews_interviewer ON interviews(interviewer);
        
        RAISE NOTICE 'Interviewer column added successfully';
    ELSE
        RAISE NOTICE 'Interviewer column already exists';
    END IF;
END $$;

-- Verify the migration
SELECT 
    column_name, 
    data_type, 
    is_nullable, 
    column_default
FROM information_schema.columns 
WHERE table_name = 'interviews' 
ORDER BY ordinal_position;