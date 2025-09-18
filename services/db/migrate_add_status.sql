-- Database Migration: Add status column to candidates table
-- This fixes the "column status does not exist" error

-- Add status column if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'candidates' AND column_name = 'status'
    ) THEN
        ALTER TABLE candidates ADD COLUMN status VARCHAR(50) DEFAULT 'active';
        
        -- Update existing records to have 'active' status
        UPDATE candidates SET status = 'active' WHERE status IS NULL;
        
        -- Add index for performance
        CREATE INDEX IF NOT EXISTS idx_candidates_status ON candidates(status);
        
        RAISE NOTICE 'Added status column to candidates table';
    ELSE
        RAISE NOTICE 'Status column already exists in candidates table';
    END IF;
END $$;