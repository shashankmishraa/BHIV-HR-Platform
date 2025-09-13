-- Fix database schema issues
-- Add missing interviewer column to interviews table

-- Check if interviewer column exists, if not add it
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'interviews' AND column_name = 'interviewer'
    ) THEN
        ALTER TABLE interviews ADD COLUMN interviewer VARCHAR(255);
        RAISE NOTICE 'Added interviewer column to interviews table';
    ELSE
        RAISE NOTICE 'Interviewer column already exists in interviews table';
    END IF;
END $$;

-- Ensure all required columns exist in interviews table
DO $$
BEGIN
    -- Add interview_type if missing
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'interviews' AND column_name = 'interview_type'
    ) THEN
        ALTER TABLE interviews ADD COLUMN interview_type VARCHAR(100);
        RAISE NOTICE 'Added interview_type column to interviews table';
    END IF;
    
    -- Add notes if missing
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'interviews' AND column_name = 'notes'
    ) THEN
        ALTER TABLE interviews ADD COLUMN notes TEXT;
        RAISE NOTICE 'Added notes column to interviews table';
    END IF;
    
    -- Add status if missing
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'interviews' AND column_name = 'status'
    ) THEN
        ALTER TABLE interviews ADD COLUMN status VARCHAR(50) DEFAULT 'scheduled';
        RAISE NOTICE 'Added status column to interviews table';
    END IF;
    
    -- Add created_at if missing
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'interviews' AND column_name = 'created_at'
    ) THEN
        ALTER TABLE interviews ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        RAISE NOTICE 'Added created_at column to interviews table';
    END IF;
END $$;

-- Update any existing interviews without interviewer
UPDATE interviews SET interviewer = 'HR Team' WHERE interviewer IS NULL;

-- Show final table structure
SELECT column_name, data_type, is_nullable, column_default 
FROM information_schema.columns 
WHERE table_name = 'interviews' 
ORDER BY ordinal_position;